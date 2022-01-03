from django.contrib import admin
from .models import Course, Question


class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name','number_of_chapters']
    search_fields = ( 'course_name','number_of_chapters',)
    list_per_page = 20


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['course','question']
    search_fields = ( 'course','question',)
    list_per_page = 20

admin.site.register(Course,CourseAdmin)
admin.site.register(Question,QuestionAdmin)