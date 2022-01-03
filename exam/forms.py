from django import forms
from .models import Course, Question


class CourseForm(forms.ModelForm):
    number_of_chapters = forms.IntegerField(min_value=1)
    class Meta:
        model = Course
        fields = ['course_name', 'number_of_chapters']