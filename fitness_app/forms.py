from django import forms
from .models import Member, Trainer, Space, TrainingSession, FoodLog, Food


# RECEPTIONIST TASKS ?????

class MemberRegistrationForm(forms.ModelForm):
    YEAR_CHOICES = [(year, year) for year in range(1930, 2025)]
    MONTH_CHOICES = [(month, month) for month in range(1, 13)]
    DAY_CHOICES = [(day, day) for day in range(1, 32)]

    date_of_birth_year = forms.ChoiceField(choices=YEAR_CHOICES, label="Year of Birth")
    date_of_birth_month = forms.ChoiceField(choices=MONTH_CHOICES, label="Month of Birth")
    date_of_birth_day = forms.ChoiceField(choices=DAY_CHOICES, label="Day of Birth")

    class Meta:
        model = Member
        fields = [
            'name',
            'street_address',
            'city',
            'state',
            'zipcode',
            'goal_description',
            'goal_date'
        ]


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

class LogSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['attendance', 'progress_notes']

# MEMBERS AND PERSONAL TRAINERS

class UpdateGoalsForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['goal_description', 'goal_date']

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



