from django import forms


class EnrollmentForm(forms.Form):
    student_id = forms.IntegerField(label="Student ID")
    course_id = forms.IntegerField(label="Course ID")