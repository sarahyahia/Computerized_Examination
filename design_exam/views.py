from django.shortcuts import render
from exam.models import Course, Question
from pyeasyga import pyeasyga
from django.contrib import messages
import random
from django.utils.timezone import now



def design_home(request):
    courses = Course.objects.all()
    context={
        'courses': courses,
    }
    return render(request, 'design_exam/design_home.html', context)


def apply_genetic_algorithms(request_values, questions_list):
    ga = pyeasyga.GeneticAlgorithm(questions_list)        # initialise the GA with data
    ga.population_size = 200                              # increase population size to 200 (default value is 50)

    # define a fitness function
    def fitness(individual, questions_list):
        chapter, difficulty, objective = 0, 0, 0
        for (selected, item) in zip(individual, questions_list):
            if selected:
                chapter += item[0]
                difficulty += item[1]
                objective += item[2]
        # if difficult_questions > request_values['difficult_questions'] or simple_questions > request_values['simple_questions'] or reminding_questions > request_values['reminding_questions']or understanding_questions > request_values['understanding_questions']:
        #     creativity_questions = 0
        return objective
    ga.fitness_function = fitness               # set the GA's fitness function
    ga.run()                                    # run the GA
    print(ga.best_individual())                 # print the GA's best solution



def manually_design(request_values, AllAvailableQuestionsList, total_requested_questions):
    ExamQuestionsList=[]
    ExcludedQuestions=[]
    # import pdb ; pdb.set_trace()
    AllAvailableQuestionsList=list(AllAvailableQuestionsList)
    random.shuffle(AllAvailableQuestionsList)

    for question in AllAvailableQuestionsList:
        if len(ExamQuestionsList)<total_requested_questions:
            if request_values['ch'+str(question.chapter)]> 0 and (request_values[str(question.difficulty)+'_questions']>0) and (request_values[str(question.objective)+'objective_questions']>0):
                ExamQuestionsList.append(question)
                request_values['ch'+str(question.chapter)] -= 1
                request_values[str(question.difficulty)+'_questions'] -= 1
                request_values[str(question.objective)+'objective_questions'] -= 1
            else:
                ExcludedQuestions.append(question)
        else:
            break

    while len(ExamQuestionsList)<total_requested_questions:
        for question in ExcludedQuestions:
            if request_values['ch'+str(question.chapter)]> 0 and (request_values[str(question.difficulty)+'_questions']>0):
                ExamQuestionsList.append(question)
                ExcludedQuestions.remove(question)
                request_values['ch'+str(question.chapter)] -= 1
                request_values[str(question.difficulty)+'_questions'] -= 1
        for question in ExcludedQuestions:
            if request_values['ch'+str(question.chapter)]> 0 and (request_values[str(question.objective)+'objective_questions']>0):
                ExamQuestionsList.append(question)
                ExcludedQuestions.remove(question)
                request_values['ch'+str(question.chapter)] -= 1
                request_values[str(question.objective)+'objective_questions'] -= 1
        for question in ExcludedQuestions:
            if request_values['ch'+str(question.chapter)]> 0:
                ExamQuestionsList.append(question)
                ExcludedQuestions.remove(question)
                request_values['ch'+str(question.chapter)] -= 1
                
    return ExamQuestionsList


def design_exam(request, course_id):
    course = Course.objects.get(id=course_id)
    chapters = course.number_of_chapters
    chapters_list = []
    for i in range(1,chapters+1):
        chapters_list.append(i)
    total_questions_of_course = Question.objects.filter(course=course).count()
    context = {
        'course': course,
        'chapters': chapters_list,
        'total_questions': total_questions_of_course,
        'values':request.POST
    }
    if request.method == 'POST':
        request_values = {
        '2_questions' : int(request.POST.get('difficult')),
        '1_questions' : int(request.POST.get('simple')),
        '1objective_questions': int(request.POST.get('reminding')),
        '2objective_questions' : int(request.POST.get('understanding')),
        '3objective_questions' : int(request.POST.get('creativity')),
        }
        if request_values['2_questions']  > 6*chapters:
            messages.add_message(request, messages.ERROR, f'difficult questions are limited to {6*chapters} questions.')
            return render(request, 'design_exam/design_form.html', context)
        if request_values['1_questions'] > 6*chapters:
            messages.add_message(request, messages.ERROR, f'simple questions are limited to {6*chapters} questions.')
            return render(request, 'design_exam/design_form.html', context)
        if request_values['1objective_questions'] > 4*chapters:
            messages.add_message(request, messages.ERROR, f'reminding questions are limited to {4*chapters} questions.')
            return render(request, 'design_exam/design_form.html', context)
        if request_values['2objective_questions'] > 4*chapters:
            messages.add_message(request, messages.ERROR, f'understanding questions are limited to {4*chapters} questions.')
            return render(request, 'design_exam/design_form.html', context)
        if request_values['3objective_questions'] > 4*chapters:
            messages.add_message(request, messages.ERROR, f'creativity questions are limited to {4*chapters} questions.')
            return render(request, 'design_exam/design_form.html', context)
        
        total_requested_questions = 0
        
        for i in chapters_list:
            request_values['ch'+str(i)] =  int(request.POST.get(str(i)))
            total_requested_questions += request_values['ch'+str(i)]
            
        if total_questions_of_course < total_requested_questions:
            messages.add_message(request, messages.ERROR, f'total questions are limited to {total_questions_of_course}.') 
            return render(request, 'design_exam/design_form.html', context)
            
        if not (total_requested_questions == request_values['2_questions'] + request_values['1_questions'] == request_values['1objective_questions'] + request_values['2objective_questions'] + request_values['3objective_questions']):
            messages.add_message(request, messages.ERROR, 'total questions in every category doesn\'t match.')
            return render(request, 'design_exam/design_form.html', context)
            
        questions_list = []
        for question in Question.objects.filter(course=course):
            questions_list.append((question.chapter,question.difficulty, question.objective))
        
        # apply_genetic_algorithms(request_values, questions_list)
        
        AllAvailableQuestionsList = Question.objects.filter(course=course)
        ExamQuestionsList = manually_design(request_values, AllAvailableQuestionsList, total_requested_questions)
        
        messages.add_message(request, messages.SUCCESS, 'you exam is ready to download.')
        return render(request, 'design_exam/exam.html', {'questions':ExamQuestionsList})
    return render(request, 'design_exam/design_form.html', context)




def export_pdf(request, exam_questions):
    response = HttpResponse(content_type='text/pdf',
        headers={'Content-Disposition': "attachment; filename=exam "+str(datetime.datetime.now())+".pdf"},)
    response['Content-Transfer-Encoding'] = 'binary'
    
    exam = exam_questions
    context = {'exam':exam}
    
    #rendered
    html_string = render_to_string('design_exam/pdf-output.html',context)
    html = HTML(string=html_string)
    result = html.write_pdf()
    
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        # import pdb ; pdb.set_trace()
        output=open(output.name, 'rb')
        response.write(output.read())
    
    return response

