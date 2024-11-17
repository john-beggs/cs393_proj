from django.shortcuts import render, redirect
from .forms import MemberRegistrationForm, TrainingSessionForm, UpdateGoalsForm, LogSessionForm, FoodLogForm
from .models import Member, TrainingSession, Trainer, FoodLog, Food
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from fitness_app.models import UserRole
from datetime import datetime, timedelta
from django.http import JsonResponse
from datetime import date

# def index(request):
#     return render(request, 'index.html')

@login_required
def dashboard(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role == "Receptionist":
        return render(request, "receptionist_dashboard.html")
    elif user_role == "Trainer":
        return render(request, "trainer_dashboard.html")
    elif user_role == "Member":
        return render(request, "member_dashboard.html")

    return render(request, "error.html", {"message": "No dashboard available for your role."})

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


# FOOOOOOD

def log_food_intake(request):
    categories = Food.objects.values_list('category', flat=True).distinct()
    descriptions = Food.objects.values_list('description', flat=True).distinct()
    current_year = date.today().year
    years = range(current_year - 10, current_year + 1)
    months = range(1, 13)
    days = range(1, 32)

    if request.method == "POST":
        if 'continue' in request.POST:
            if request.POST['continue'] == 'yes':
                return render(request, 'log_food_intake.html', {
                    'categories': categories,
                    'descriptions': descriptions,
                    'years': years,
                    'months': months,
                    'days': days,
                    'submitted': False,
                })
            else:
                return redirect('food_summary')

        meal = request.POST.get('meal')
        category = request.POST.get('category')
        description = request.POST.get('description')
        weight = float(request.POST.get('weight', 0))

        return render(request, 'log_food_intake.html', {
            'submitted': True,
        })

    return render(request, 'log_food_intake.html', {
        'categories': categories,
        'descriptions': descriptions,
        'years': years,
        'months': months,
        'days': days,
        'submitted': False,
    })



@login_required
def food_summary(request):
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    week_logs = FoodLog.objects.filter(member=request.user, date__range=[week_start, week_end])
    month_logs = FoodLog.objects.filter(member=request.user, date__year=today.year, date__month=today.month)

    def calculate_totals(logs):
        totals = {"carbohydrate": 0, "protein": 0, "fat": 0, "kilocalories": 0}
        for log in logs:
            totals["carbohydrate"] += log.carbohydrate
            totals["protein"] += log.protein
            totals["fat"] += log.fat
            totals["kilocalories"] += log.kilocalories
        return totals

    weekly_totals = calculate_totals(week_logs)
    monthly_totals = calculate_totals(month_logs)

    return render(request, "food_summary.html", {
        "weekly_totals": weekly_totals,
        "monthly_totals": monthly_totals
    })
