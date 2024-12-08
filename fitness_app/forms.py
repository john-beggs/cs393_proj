from django import forms
from .models import Member, Trainer, Space, TrainingSession, FoodLog, Food, Fine, Payment


# RECEPTIONIST TASKS ?????

from datetime import date

class MemberRegistrationForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(1930, date.today().year + 1)]
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
    YEAR_CHOICES = [(year, year) for year in range(2023, 2029)]
    MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    DAY_CHOICES = [(day, day) for day in range(1, 32)]

    date_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year")
    date_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month")
    date_day = forms.ChoiceField(choices=DAY_CHOICES, label="Day")

    HOUR_CHOICES = [(hour, f"{hour:02d}") for hour in range(24)]
    MINUTE_CHOICES = [(minute, f"{minute:02d}") for minute in range(60)]
    time_hour = forms.ChoiceField(choices=HOUR_CHOICES, label="Hour")
    time_minute = forms.ChoiceField(choices=MINUTE_CHOICES, label="Minute")

    DURATION_CHOICES = [
        ("00:30:00", "30 Minutes"),
        ("00:45:00", "45 Minutes"),
        ("01:00:00", "1 Hour"),
        ("01:30:00", "1 Hour 30 Minutes"),
    ]
    duration = forms.ChoiceField(choices=DURATION_CHOICES, label="Duration")

    class Meta:
        model = TrainingSession
        fields = ['member', 'trainer', 'space']

    def save(self, commit=True):
        session = super().save(commit=False)

        session.date = date(
            int(self.cleaned_data['date_year']),
            int(self.cleaned_data['date_month']),
            int(self.cleaned_data['date_day']),
        )
        session.time = f"{self.cleaned_data['time_hour']}:{self.cleaned_data['time_minute']}:00"

        if commit:
            session.save()
        return session

class LogSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['attendance', 'progress_notes']


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
