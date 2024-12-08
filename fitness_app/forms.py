from django import forms
from .models import Member, Trainer, Space, TrainingSession, FoodLog, Food, Fine, Payment
from datetime import datetime, timedelta, date, time
from django.db.models import Q, F  # Import Q and F
# RECEPTIONIST TASKS ?????


class MemberRegistrationForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(1930, date.today().year + 5)]
    MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    DAY_CHOICES = [(day, day) for day in range(1, 32)]

    date_of_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year of Birth")
    date_of_birth_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month of Birth")
    date_of_birth_day = forms.ChoiceField(choices=DAY_CHOICES, label="Day of Birth")
    goal_date_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Goal Year")
    goal_date_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Goal Month")
    goal_date_day = forms.ChoiceField(choices=DAY_CHOICES, label="Goal Day")
    goal_weight = forms.IntegerField(label="Goal Weight (lbs)", min_value=1)

    class Meta:
        model = Member
        fields = [
            'first_name',
            'last_name',
            'street_address',
            'city',
            'state',
            'zipcode',
            'goal_description',
        ]

    def clean(self):
        cleaned_data = super().clean()

        birth_year = int(cleaned_data.get('date_of_birth_year'))
        birth_month = int(cleaned_data.get('date_of_birth_month'))
        birth_day = int(cleaned_data.get('date_of_birth_day'))
        date_of_birth = date(birth_year, birth_month, birth_day)

        if date_of_birth >= date.today():
            self.add_error('date_of_birth_year', "Date of birth must be in the past.")

        goal_year = int(cleaned_data.get('goal_date_year'))
        goal_month = int(cleaned_data.get('goal_date_month'))
        goal_day = int(cleaned_data.get('goal_date_day'))
        goal_date = date(goal_year, goal_month, goal_day)

        if goal_date <= date.today():
            self.add_error('goal_date_year', "Goal date must be in the future.")

        return cleaned_data

    def save(self, commit=True):
        member = super().save(commit=False)

        birth_year = int(self.cleaned_data['date_of_birth_year'])
        birth_month = int(self.cleaned_data['date_of_birth_month'])
        birth_day = int(self.cleaned_data['date_of_birth_day'])
        member.date_of_birth = date(birth_year, birth_month, birth_day)

        goal_year = int(self.cleaned_data['goal_date_year'])
        goal_month = int(self.cleaned_data['goal_date_month'])
        goal_day = int(self.cleaned_data['goal_date_day'])
        member.goal_date = date(goal_year, goal_month, goal_day)

        member.goal_weight = self.cleaned_data['goal_weight']

        if commit:
            member.save()
        return member



class TrainingSessionForm(forms.ModelForm):
    date_year = forms.ChoiceField(choices=[(y, y) for y in range(2023, 2030)], required=True)
    date_month = forms.ChoiceField(choices=[(m, m) for m in range(1, 13)], required=True)
    date_day = forms.ChoiceField(choices=[(d, d) for d in range(1, 32)], required=True)
    time_hour = forms.ChoiceField(choices=[(h, f"{h:02}") for h in range(24)], required=True)
    time_minute = forms.ChoiceField(choices=[(m, f"{m:02}") for m in range(0, 60, 15)], required=True)
    duration = forms.ChoiceField(
        choices=[(30, "30 Minutes"), (45, "45 Minutes"), (60, "1 Hour"), (90, "1 Hour 30 Minutes")],
        required=True,
        label="Duration"
    )
    
    class Meta:
        model = TrainingSession
        fields = ['trainer', 'space', 'duration']

    def clean(self):
        cleaned_data = super().clean()

        # Combine year, month, and day into a single date field
        try:
            year = int(cleaned_data.get('date_year'))
            month = int(cleaned_data.get('date_month'))
            day = int(cleaned_data.get('date_day'))
            session_date = date(year, month, day)
            cleaned_data['date'] = session_date
        except (ValueError, TypeError):
            self.add_error('date_year', "Invalid date. Please provide a valid year, month, and day.")
            return cleaned_data

        # Combine hour and minute into a single time field
        try:
            hour = int(cleaned_data.get('time_hour'))
            minute = int(cleaned_data.get('time_minute'))
            session_time = time(hour, minute)
            cleaned_data['time'] = session_time
        except (ValueError, TypeError):
            self.add_error('time_hour', "Invalid time. Please provide a valid hour and minute.")
            return cleaned_data

        # Get duration and calculate end time
        try:
            duration = int(cleaned_data.get('duration'))
        except (ValueError, TypeError):
            self.add_error('duration', "Invalid duration. Please select a valid option.")
            return cleaned_data

        start_datetime = datetime.combine(session_date, session_time)
        end_datetime = start_datetime + timedelta(minutes=duration)

        # Check for trainer and room conflicts
        trainer = cleaned_data.get('trainer')
        room = cleaned_data.get('space')

        if trainer:
            trainer_overlap = TrainingSession.objects.filter(
                trainer=trainer,
                date=session_date,
            ).filter(
                Q(time__lt=end_datetime.time(), time__gte=start_datetime.time())
                | Q(time__lte=start_datetime.time(), time__gte=end_datetime.time())
            ).exists()

            if trainer_overlap:
                self.add_error('trainer', "This trainer is already booked during the selected time.")

        if room:
            room_overlap = TrainingSession.objects.filter(
                space=room,
                date=session_date,
            ).filter(
                Q(time__lt=end_datetime.time(), time__gte=start_datetime.time())
                | Q(time__lte=start_datetime.time(), time__gte=end_datetime.time())
            ).exists()

            if room_overlap:
                self.add_error('space', "This space is already booked during the selected time.")

        return cleaned_data

    def save(self, commit=True):
        session = super().save(commit=False)  # Do not save yet
        session.date = date(
            int(self.cleaned_data['date_year']),
            int(self.cleaned_data['date_month']),
            int(self.cleaned_data['date_day']),
        )
        session.time = f"{int(self.cleaned_data['time_hour']):02}:{int(self.cleaned_data['time_minute']):02}:00"
        if commit:
            session.save()
        return session


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['amount']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount_due', 'due_date', 'payment_date', 'is_paid']

# MEMBERS AND PERSONAL TRAINERS

class UpdateGoalsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['goal_description', 'goal_date']

    def clean_goal_date(self):
        goal_date = self.cleaned_data.get('goal_date')
        if goal_date <= date.today():
            raise forms.ValidationError("Goal date must be in the future.")
        return goal_date

# ONLY PERSONAL TRAINERS

class FoodLogForm(forms.ModelForm):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]

    meal = forms.ChoiceField(choices=MEAL_CHOICES, label="Meal")
    category = forms.ChoiceField(
        choices=[(food["category"], food["category"]) for food in Food.objects.values("category").distinct()],
        label="Category",
    )
    description = forms.ChoiceField(
        choices=[(food["description"], food["description"]) for food in Food.objects.values("description").distinct()],
        label="Description",
    )
    grams = forms.FloatField(label="Weight (grams)", required=True)
    year = forms.ChoiceField(choices=[(y, y) for y in range(2023, 2035)], label="Year")
    month = forms.ChoiceField(choices=[(m, m) for m in range(1, 13)], label="Month")
    day = forms.ChoiceField(choices=[(d, d) for d in range(1, 32)], label="Day")

    class Meta:
        model = FoodLog
        fields = ['meal', 'category', 'description', 'grams']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(food['category'], food['category']) for food in Food.objects.values('category').distinct()]
        self.fields['description'].choices = []
