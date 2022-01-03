from django.urls import path
from . import views


urlpatterns = [
    path('', views.index , name='home'),
    path('afterlogin/', views.afterlogin_view, name='afterlogin'),
    path('adminhome/', views.admin_index, name='admin-home'),
    path('teacherhome/', views.teacher_index, name='teacher-home'),
    path('courses/', views.courses, name='courses'),
    path('addcourse/', views.add_course, name='add-course'),
    path('editcourse/<int:course_id>/', views.edit_course, name='edit-course'),
    path('deletecourse/<int:course_id>/', views.delete_course, name='delete-course'),
    path('coursechapters/<int:course_id>/', views.course_chapters, name='course-chapters'),
    path('coursechquestions/<int:course_id>/<int:chapter>/', views.course_chapter_questions, name='course-chapter-questions'),
    path('addquestion/<int:course_id>/<int:chapter>/', views.add_question, name='add-question'),
    path('deletequestion/<int:question_id>/', views.delete_question, name='delete-question'),
    
]