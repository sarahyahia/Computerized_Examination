from django.urls import path
from . import views



urlpatterns = [
    path('', views.design_home, name='design_home'),
    path('exam/<int:course_id>/', views.design_exam, name='design_exam'),
    path('export-pdf', views.export_pdf, name='export-pdf'),
    
]