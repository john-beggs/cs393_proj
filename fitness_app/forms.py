from django import forms
from .models import Member, Trainer, Space, TrainingSession


# RECEPTIONIST TASKS ?????

class MemberRegistrationForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'address', 'date_of_birth', 'goal_description', 'goal_date']

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['member', 'trainer', 'space', 'date', 'time', 'duration']

# MEMBERS AND PERSONAL TRAINERS

class UpdateGoalsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['goal_description', 'goal_date']

# ONLY PERSONAL TRAINERS

class LogSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['attendance', 'progress_notes']

