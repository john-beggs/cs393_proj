from django.shortcuts import render, redirect
from .forms import MemberRegistrationForm, TrainingSessionForm, UpdateGoalsForm, LogSessionForm
from .models import Member, TrainingSession, Trainer, Food
from django.shortcuts import get_object_or_404

def index(request):
    return render(request, 'index.html')

def register_member(request):
    if request.method == "POST":
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MemberRegistrationForm()
    return render(request, 'register_member.html', {'form': form})

def schedule_training_session(request):
    if request.method == "POST":
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)

            if session.space.is_available:
                session.save()
                return redirect('index')
            else:
                return render(request, 'schedule_training_session.html', {
                    'form': form,
                    'error': 'The selected space is not available.',
                })
    else:
        form = TrainingSessionForm()
    return render(request, 'schedule_training_session.html', {'form': form})

def update_goals(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == "POST":
        form = UpdateGoalsForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UpdateGoalsForm(instance=member)
    return render(request, 'update_goals.html', {'form': form, 'member': member})

def log_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)
    if request.method == "POST":
        form = LogSessionForm(request.POST, instance=session)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LogSessionForm(instance=session)
    return render(request, 'log_session.html', {'form': form, 'session': session})



