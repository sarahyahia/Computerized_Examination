from django.shortcuts import render, redirect
from .models import Course, Question
from django.contrib import messages
from .forms import CourseForm
from django.contrib.auth.models import User
from django.urls import reverse
from helpers.decorators import auth_user_should_not_access, staff_required
from django.contrib.auth.decorators import login_required


@auth_user_should_not_access
def index(request):
    return render(request, 'landing/index.html')

@login_required(login_url='login')
def afterlogin_view(request):
    if request.user.is_staff:      
        return redirect('admin-home')
    else:
        return redirect('teacher-home')

@staff_required(login_url='home')
def admin_index(request):
    courses = Course.objects.all().count
    questions = Question.objects.all().count
    teachers = User.objects.exclude(is_staff=True).count
    context = {
        'courses': courses,
        'questions': questions,
        'teachers': teachers
    }
    return render(request, 'exam/admin_index.html', context)


@login_required(login_url='login')
def teacher_index(request):
    return render(request, 'exam/teacher_index.html')


@login_required(login_url='login')
def courses(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'exam/courses.html', context)



@login_required(login_url='login')
def course_chapters(request, course_id):
    course = Course.objects.get(id=course_id)
    chapters = course.number_of_chapters
    chapters_list = []
    for i in range(1,chapters+1):
        chapters_list.append(i)
    context = {
        'course': course,
        'chapters': chapters_list,
    }
    return render(request, 'exam/course_chapters.html', context)


@login_required(login_url='login')
def course_chapter_questions(request, course_id, chapter):
    questions = Question.objects.filter(course=course_id, chapter=chapter)
    number_of_questions = questions.count
    course = Course.objects.get(id=course_id)
    context = {
        "questions": questions,
        'course': course,
        'chapter': chapter,
        'number_of_questions':number_of_questions,
    }
    return render(request, 'exam/course_ch_questions.html', context)

@staff_required(login_url='home')
def add_course(request):
    context = {'course':request.POST}
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        number_of_chapters = int( request.POST.get('number_of_chapters'))
        
        if number_of_chapters <= 0:
            messages.add_message(request, messages.ERROR, 'Please enter a positive number')
            return render(request, 'exam/add_course.html', context)
        course = Course.objects.create(course_name=course_name, number_of_chapters= number_of_chapters)
        messages.add_message(request, messages.SUCCESS, 'Course added successfully.')
        return redirect('courses')
    return render(request, 'exam/add_course.html', context)


@staff_required(login_url='home')
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {'course': course}
    if request.method == 'POST':
        course_name = request.POST.get('course_name')
        number_of_chapters = int(request.POST.get('number_of_chapters'))
        if number_of_chapters <= 0 :
            messages.add_message(request, messages.ERROR, 'Please enter a positive number')
            return render(request, 'exam/edit_course.html', context)
        course.course_name = course_name
        course.number_of_chapters = number_of_chapters
        course.save()
        messages.add_message(request, messages.SUCCESS, 'Course edited successfully.')
        return redirect('courses')
    return render(request, 'exam/edit_course.html', context)


@staff_required(login_url='home')
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.delete()
    messages.add_message(request, messages.SUCCESS, 'Course deleted successfully.')
    return redirect('courses')


@staff_required(login_url='home')
def add_question(request, course_id, chapter):
    courses = Course.objects.all()
    course = courses.get(id=course_id)
    context = {
        'courses': courses,
        'question':request.POST,
        'chapter':chapter,
        'course': course,
    }
    if request.method == 'POST':
        question = request.POST.get('question')
        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        answer = request.POST.get('answer')
        difficulty = int(request.POST.get('difficulty'))
        objective = int(request.POST.get('objective'))
        questions_of_chapter = Question.objects.filter(course=course, chapter=chapter)
        if questions_of_chapter.count() <=12 :
            if questions_of_chapter.filter(difficulty = difficulty).count() >= 6:
                messages.add_message(request, messages.ERROR, 'questions with this difficulty level are limited to 6 questions/chapter.')
                return render(request,'exam/add_question.html', context)
            elif questions_of_chapter.filter(objective = objective).count() >=4:
                messages.add_message(request, messages.ERROR, 'questions with this objective are limited to 4 questions/chapter.')
                return render(request,'exam/add_question.html', context)
            elif questions_of_chapter.filter(difficulty=difficulty, objective=objective).count()>=2:
                messages.add_message(request, messages.ERROR, 'questions with this difficulty and objective are limited to 2 questions/chapter.')
                return render(request,'exam/add_question.html', context)
            added_question = Question.objects.create(course=course, chapter=chapter, question=question, option1=option1, option2=option2, option3=option3, answer=answer, objective=objective, difficulty=difficulty)
            messages.add_message(request, messages.SUCCESS, 'Question is created successfully.')
            return render(request,'exam/add_question.html', context)
        else:
            messages.add_message(request, messages.ERROR, 'Something has gone wrong. Please try again.')
    return render(request,'exam/add_question.html', context)
    

# need to add edit_view for questions

@staff_required(login_url='home')
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    chapter= question.chapter
    course_id = question.course.id
    question.delete()
    messages.add_message(request, messages.SUCCESS, 'Question deleted successfully.')
    return redirect(reverse('course-chapter-questions', kwargs={'course_id':course_id,'chapter':chapter}))


