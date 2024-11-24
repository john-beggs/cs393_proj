from django.shortcuts import render, redirect
from .forms import MemberRegistrationForm, TrainingSessionForm, UpdateGoalsForm, LogSessionForm, FoodLogForm
from .models import Member, TrainingSession, Trainer, FoodLog, Food
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from fitness_app.models import UserRole
from datetime import datetime, timedelta
from django.http import JsonResponse
from datetime import date
from django.db.models import Q


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
    elif user_role == "Manager":
        return render(request, "manager_dashboard.html")

    return render(request, "error.html", {"message": "No dashboard available for your role."})


def register_member(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user_role = UserRole.objects.get(user=request.user).role.name
    if user_role not in ["Receptionist", "Manager"]:
        return render(request, "error.html", {"message": "Access Denied"})

    if request.method == "POST":
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = MemberRegistrationForm()
    return render(request, "register_member.html", {"form": form})


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
    return render(request, 'log_session.html', {
        'form': form,
        'session': session,
    })


def log_food_intake(request):
    categories = Food.objects.values_list('category', flat=True).distinct()
    current_year = date.today().year
    years = range(current_year - 10, current_year + 1)
    months = range(1, 13)
    days = range(1, 32)

    if request.method == "POST":
        meal = request.POST.get('meal')
        category = request.POST.get('category')
        description = request.POST.get('description')
        servings = request.POST.get('servings')

        try:
            servings = float(servings)
            if servings <= 0:
                raise ValueError
        except ValueError:
            return render(request, 'log_food_intake.html', {
                'categories': categories,
                'years': years,
                'months': months,
                'days': days,
                'error_message': 'Servings must be a positive number.',
            })

        food_item = Food.objects.filter(category=category, description=description).first()
        if not food_item:
            return render(request, 'log_food_intake.html', {
                'categories': categories,
                'years': years,
                'months': months,
                'days': days,
                'error_message': 'Invalid food selection.',
            })

        carbohydrate = food_item.carbohydrate * servings
        protein = food_item.protein * servings
        fat = food_item.fat_total_lipid * servings
        kilocalories = food_item.kilocalories * servings

        FoodLog.objects.create(
            member=request.user,
            date=date.today(),
            meal=meal,
            category=category,
            description=description,
            servings=servings,
            carbohydrate=carbohydrate,
            protein=protein,
            fat=fat,
            kilocalories=kilocalories,
        )
        return redirect('food_summary')

    return render(request, 'log_food_intake.html', {
        'categories': categories,
        'years': years,
        'months': months,
        'days': days,
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

def get_descriptions(request):
    category = request.GET.get('category', '')
    if category:
        descriptions = list(Food.objects.filter(category=category).values_list('description', flat=True))
    else:
        descriptions = []
    return JsonResponse({'descriptions': descriptions})


@login_required
def manager_dashboard(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role == "Manager":
        members = Member.objects.all()
        return render(request, "manager_dashboard.html", {"members": members})

    return render(request, "error.html", {"message": "You do not have access to this page."})


@login_required
def member_list(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role == "Manager":
        members = Member.objects.all()
        return render(request, "member_list.html", {"members": members})

    return render(request, "error.html", {"message": "You do not have access to this page."})


@login_required
def member_report(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role != "Manager":
        return render(request, "error.html", {"message": "You do not have access to this page."})

    member = None
    food_logs = []
    training_sessions = []

    if request.method == "GET" and 'search' in request.GET:
        search_query = request.GET.get('search', '').strip()
        if search_query:
            name_parts = search_query.split(" ", 1)
            first_name = name_parts[0]
            last_name = name_parts[1] if len(name_parts) > 1 else ""

            if last_name:
                member = Member.objects.filter(first_name__icontains=first_name, last_name__icontains=last_name).first()
            else:
                member = Member.objects.filter(Q(first_name__icontains=first_name) | Q(last_name__icontains=first_name)).first()

            if member:
                food_logs = FoodLog.objects.filter(member__username=f"{member.first_name.lower()}.{member.last_name.lower()}")
                training_sessions = TrainingSession.objects.filter(member=member)

    return render(request, "member_report.html", {
        "member": member,
        "food_logs": food_logs,
        "training_sessions": training_sessions,
    })


