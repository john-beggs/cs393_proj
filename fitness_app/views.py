from django.shortcuts import render, redirect
from .forms import MemberRegistrationForm, TrainingSessionForm, UpdateGoalsForm, FoodLogForm
from .models import Member, TrainingSession, Trainer, FoodLog, Food, MemberJoinsSession, Space
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from fitness_app.models import UserRole, Member, Payment, Fine, User
from datetime import datetime, timedelta
from django.http import JsonResponse
from datetime import date, time
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse

def check_role(user, required_role):
    try:
        user_role = UserRole.objects.get(user=user).role.name
        return user_role == required_role
    except UserRole.DoesNotExist:
        return False


def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            try:
                user_role = UserRole.objects.get(user=user).role.name
                if user_role == "Receptionist":
                    return redirect("receptionist_dashboard")
                elif user_role == "Trainer":
                    return redirect("trainer_dashboard")
                elif user_role == "Member":
                    return redirect("member_dashboard")
                elif user_role == "Manager":
                    return redirect("manager_dashboard")
            except UserRole.DoesNotExist:
                return render(request, "error.html", {"message": "No role assigned. Please contact an administrator."})
        else:
            return render(request, "login.html", {"error": "Invalid username or password"})

    return render(request, "login.html")

@login_required
def dashboard(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role == "Receptionist":
        return redirect("receptionist_dashboard")
    elif user_role == "Trainer":
        return redirect("trainer_dashboard")
    elif user_role == "Member":
        return redirect("member_dashboard")
    elif user_role == "Manager":
        return redirect("manager_dashboard")

    return render(request, "error.html", {"message": "No dashboard available for your role."})

@login_required
def member_dashboard(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
        if user_role != "Member":
            return render(request, "error.html", {"message": "Access Denied"})

        member = Member.objects.get(user=request.user)
        food_logs = FoodLog.objects.filter(member=request.user)
        joined_sessions = MemberJoinsSession.objects.filter(member=member)

        context = {
            "member": member,
            "food_logs": food_logs,
            "joined_sessions": joined_sessions,
        }
        return render(request, "member_dashboard.html", context)

    except Member.DoesNotExist:
        return render(request, "error.html", {"message": "No member profile found."})


##### RECEPTIONIST STUFF

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

def receptionist_dashboard(request):
    user_role = UserRole.objects.get(user=request.user).role.name
    if user_role != "Receptionist":
        return render(request, "error.html", {"message": "Access Denied"})
    return render(request, "receptionist_dashboard.html")

@login_required
def search_member(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role != "Receptionist":
        return render(request, "error.html", {"message": "Access Denied"})

    members = None
    if request.method == "GET":
        first_name = request.GET.get("first_name", "").strip()
        last_name = request.GET.get("last_name", "").strip()

        members = Member.objects.all()
        if first_name:
            members = members.filter(first_name__icontains=first_name)
        if last_name:
            members = members.filter(last_name__icontains=last_name)

    return render(request, "search_member.html", {"members": members})

@login_required
def edit_member(request, member_id):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return redirect("login")

    if user_role != "Receptionist":
        return render(request, "error.html", {"message": "Access Denied"})

    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        form = MemberRegistrationForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("search_member")
    else:
        form = MemberRegistrationForm(instance=member)

    return render(request, "edit_member.html", {"form": form, "member": member})


def schedule_training_session(request):
    if request.method == "POST":
        form = TrainingSessionForm(request.POST)
        if form.is_valid():
            session = form.save()
            return redirect('receptionist_dashboard')
    else:
        form = TrainingSessionForm()

    # Add composite date fields to the context
    date_fields = [form['date_year'], form['date_month'], form['date_day']]

    return render(request, 'schedule_training_session.html', {'form': form, 'date_fields': date_fields})



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

###### MEMBERS GO CRAZY

@login_required
def edit_my_info(request):
    if not check_role(request.user, "Member"):
        return render(request, "error.html", {"message": "Access Denied"})

    member = Member.objects.get(user=request.user)

    if request.method == "POST":
        form = MemberRegistrationForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("member_dashboard")
    else:
        form = MemberRegistrationForm(instance=member)

    return render(request, "edit_my_info.html", {"form": form, "member": member})


@login_required
def log_food_intake(request):
    if not check_role(request.user, "Member"):
        return render(request, "error.html", {"message": "Access Denied"})

    categories = Food.objects.values_list('category', flat=True).distinct()

    # Generate dropdown values for years, months, and days
    current_year = date.today().year
    years = range(current_year - 10, current_year + 1)  # Past 10 years to current year
    months = range(1, 13)  # 1 to 12 for months
    days = range(1, 32)  # 1 to 31 for days

    if request.method == "POST":
        meal = request.POST.get("meal")
        category = request.POST.get("category")
        description = request.POST.get("description")
        servings = request.POST.get("servings")
        year = request.POST.get("date_year")
        month = request.POST.get("date_month")
        day = request.POST.get("date_day")

        # Validate and parse the date
        try:
            selected_date = date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            return render(request, "log_food_intake.html", {
                "categories": categories,
                "years": years,
                "months": months,
                "days": days,
                "error_message": "Invalid date selected. Please provide a valid year, month, and day.",
            })

        # Validate servings
        try:
            servings = float(servings)
            if servings <= 0:
                raise ValueError
        except ValueError:
            return render(request, "log_food_intake.html", {
                "categories": categories,
                "years": years,
                "months": months,
                "days": days,
                "error_message": "Servings must be a positive number.",
            })

        # Validate food selection
        food_item = Food.objects.filter(category=category, description=description).first()
        if not food_item:
            return render(request, "log_food_intake.html", {
                "categories": categories,
                "years": years,
                "months": months,
                "days": days,
                "error_message": "Invalid food selection.",
            })

        # Create food log with the selected date
        FoodLog.objects.create(
            member=request.user,
            date=selected_date,  # Use the selected date
            meal=meal,
            category=category,
            description=description,
            servings=servings,
            carbohydrate=food_item.carbohydrate * servings,
            protein=food_item.protein * servings,
            fat=food_item.fat_total_lipid * servings,
            kilocalories=food_item.kilocalories * servings,
        )
        return redirect("member_dashboard")

    return render(request, "log_food_intake.html", {
        "categories": categories,
        "years": years,
        "months": months,
        "days": days,
    })


def get_food_details(request):
    if request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        category = request.GET.get('category')
        description = request.GET.get('description')

        food_item = Food.objects.filter(category=category, description=description).first()
        if food_item:
            return JsonResponse({
                'serv_desc': food_item.serv_desc,
                'serv_grams': food_item.serv_grams,
            })
        else:
            return JsonResponse({'error': 'Food item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)



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
        search_query = request.GET.get('search', '').strip()
        members = Member.objects.all()

        if search_query:
            members = members.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )

        return render(request, "member_list.html", {
            "members": members,
            "search_query": search_query,
        })

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
                user = User.objects.filter(first_name=member.first_name, last_name=member.last_name).first()
                if user:
                    food_logs = FoodLog.objects.filter(member=user)
                training_sessions = MemberJoinsSession.objects.filter(member=member)

    return render(request, "member_report.html", {
        "member": member,
        "food_logs": food_logs,
        "training_sessions": training_sessions,
    })


# EVERYTHING HAVING TO DO WITH PAYMENT AND FINES

@login_required
def track_payment(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return render(request, "error.html", {"message": "Access Denied"})

    if user_role not in ["Receptionist", "Manager"]:
        return render(request, "error.html", {"message": "Access Denied"})

    if user_role == "Receptionist":
        dashboard_url = reverse("receptionist_dashboard")
    elif user_role == "Manager":
        dashboard_url = reverse("manager_dashboard")
    else:
        dashboard_url = reverse("login")

    search_query = request.GET.get("search", "").strip()

    if search_query:
        name_parts = search_query.split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        if last_name:
            members = Member.objects.filter(
                first_name__icontains=first_name,
                last_name__icontains=last_name,
            ).prefetch_related("payments")
        else:
            members = Member.objects.filter(
                Q(first_name__icontains=first_name) | Q(last_name__icontains=first_name)
            ).prefetch_related("payments")
    else:
        members = Member.objects.prefetch_related("payments").all()

    return render(
        request, "track_payment.html", {"members": members, "dashboard_url": dashboard_url}
    )


@login_required
def update_payment(request, payment_id):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return render(request, "error.html", {"message": "Access Denied"})

    if user_role not in ["Receptionist", "Manager"]:
        return render(request, "error.html", {"message": "Access Denied"})

    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        payment.payment_date = date.today()
        payment.is_paid = True
        payment.save()
        return redirect("track_payment")

    return render(request, "update_payment.html", {"payment": payment})


@login_required
def view_fines(request, member_id):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
    except UserRole.DoesNotExist:
        return render(request, "error.html", {"message": "Access Denied"})

    if user_role not in ["Receptionist", "Manager", "Member"]:
        return render(request, "error.html", {"message": "Access Denied"})

    member = get_object_or_404(Member, id=member_id)
    fines = Payment.objects.filter(member=member, fine__isnull=False)

    if not fines.exists():
        return render(request, "view_fines.html", {"member": member, "fines": None, "message": "No fines to display."})

    return render(request, "view_fines.html", {"member": member, "fines": fines})

# USERS INTERACTING WITH A SESSION

@login_required
def available_dates(request):
    selected_duration = request.GET.get('duration', '')
    selected_space = request.GET.get('space', '')

    session_filter = Q()
    if selected_duration:
        session_filter &= Q(duration=selected_duration)
    if selected_space:
        session_filter &= Q(space__name=selected_space)

    filtered_sessions = TrainingSession.objects.filter(session_filter).distinct()

    dates = filtered_sessions.values_list('date', flat=True).distinct()

    durations = TrainingSession.objects.values_list('duration', flat=True).distinct()
    spaces = Space.objects.values_list('name', flat=True).distinct()

    context = {
        'dates': sorted(set(dates)),
        'durations': sorted(set(durations)),
        'spaces': sorted(set(spaces)),
    }
    return render(request, 'available_dates.html', context)


@login_required
def sessions_by_date(request, selected_date):
    selected_duration = request.GET.get('duration', '')
    selected_space = request.GET.get('space', '')

    session_filter = Q(date=selected_date)
    if selected_duration:
        session_filter &= Q(duration=selected_duration)
    if selected_space:
        session_filter &= Q(space__name=selected_space)

    sessions = TrainingSession.objects.filter(session_filter)

    context = {
        'selected_date': selected_date,
        'sessions': sessions,
    }
    return render(request, 'sessions_by_date.html', context)


@login_required
def joined_sessions(request):
    if not check_role(request.user, "Member"):
        return render(request, "error.html", {"message": "Access Denied"})

    member = Member.objects.get(user=request.user)
    joined_sessions = MemberJoinsSession.objects.filter(member=member)

    return render(request, "joined_sessions.html", {"joined_sessions": joined_sessions})

@login_required
def joined_sessions(request):
    member = Member.objects.get(id=request.user.id)
    joined_sessions = MemberJoinsSession.objects.filter(member=member)
    return render(request, "joined_sessions.html", {"joined_sessions": joined_sessions})

@login_required
def join_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)
    member = Member.objects.get(id=request.user.id)

    if MemberJoinsSession.objects.filter(member=member, session=session).exists():
        return render(request, "error.html", {"message": "You have already joined this session."})

    MemberJoinsSession.objects.create(member=member, session=session)
    return redirect("joined_sessions")

#### TRAINER INTERACTING WITH A SESSION

@login_required
def trainer_dashboard(request):
    try:
        user_role = UserRole.objects.get(user=request.user).role.name
        if user_role != "Trainer":
            return render(request, "error.html", {"message": "Access Denied"})

        trainer = Trainer.objects.get(user=request.user)
        training_sessions = TrainingSession.objects.filter(trainer=trainer)

        context = {
            "trainer": trainer,
            "training_sessions": training_sessions,
        }
        return render(request, "trainer_dashboard.html", context)

    except Trainer.DoesNotExist:
        return render(request, "error.html", {"message": "No trainer profile found."})
    
@login_required
def mark_attendance(request):
    if not check_role(request.user, "Trainer"):
        return render(request, "error.html", {"message": "Access Denied"})

    trainer = Trainer.objects.get(user=request.user)
    sessions = TrainingSession.objects.filter(trainer=trainer)

    if request.method == "POST":
        session_id = request.POST.get("session_id")
        member_ids = request.POST.getlist("attendance")

        for member_id in member_ids:
            MemberJoinsSession.objects.filter(session_id=session_id, member_id=member_id).update(attended=True)

        return redirect("mark_attendance")

    return render(request, "mark_attendance.html", {"sessions": sessions})

@login_required
def view_all_classes(request):
    if not check_role(request.user, "Trainer"):
        return render(request, "error.html", {"message": "Access Denied"})

    trainer = Trainer.objects.get(user=request.user)
    classes = TrainingSession.objects.filter(trainer=trainer)

    return render(request, "view_all_classes.html", {"classes": classes})

@login_required
def delete_class(request):
    if not check_role(request.user, "Trainer"):
        return render(request, "error.html", {"message": "Access Denied"})

    trainer = Trainer.objects.get(user=request.user)
    classes = TrainingSession.objects.filter(trainer=trainer)

    if request.method == "POST":
        session_id = request.POST.get("session_id")
        TrainingSession.objects.filter(id=session_id, trainer=trainer).delete()
        return redirect("delete_class")

    return render(request, "delete_class.html", {"classes": classes})
