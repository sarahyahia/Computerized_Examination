from django.db import models



class Course(models.Model):
    course_name = models.CharField(max_length=50)
    number_of_chapters = models.PositiveIntegerField()
    def __str__(self):
        return self.course_name
    class Meta:
        ordering = ("course_name",)
    

DIFFICULTY_CHOICES=[
    (1,'simple'),
    (2,'difficult')
]

OBJECTIVE_CHOICES=[
    (1,'reminding'),
    (2,'understanding'),
    (3,'creativity')
]

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    chapter = models.IntegerField(default=1)
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'))
    answer=models.CharField(max_length=200,choices=cat)
    difficulty=models.IntegerField(choices=DIFFICULTY_CHOICES)
    objective=models.IntegerField(choices=OBJECTIVE_CHOICES)
    class Meta:
        ordering = ("course__course_name",)

