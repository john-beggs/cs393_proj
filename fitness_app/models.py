from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class Member(models.Model):
    name = models.CharField(max_length=100)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    goal_description = models.TextField(default="No Goal Specified")
    date_joined = models.DateField(auto_now_add=True)
    goal_date = models.DateField()

    def __str__(self):
        return self.name


class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Food(models.Model):
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat_total_lipid = models.FloatField()
    kilocalories = models.FloatField()


class Space(models.Model):
    YOGA_STUDIO = "Yoga Studio"
    TREADMILL_ROOM = "Treadmill Room"
    WEIGHT_ROOM_1 = "Weight Room 1"
    WEIGHT_ROOM_2 = "Weight Room 2"
    WEIGHT_ROOM_3 = "Weight Room 3"
    BOXING_GYM = "Boxing Gym"
    CROSSFIT_GYM = "CrossFit Gym"
    WIND_TUNNEL = "Wind Tunnel"
    DANCE_STUDIO = "Dance Studio"

    SPACE_CHOICES = [
        (YOGA_STUDIO, "Yoga Studio"),
        (TREADMILL_ROOM, "Treadmill Room"),
        (WEIGHT_ROOM_1, "Weight Room 1"),
        (WEIGHT_ROOM_2, "Weight Room 2"),
        (WEIGHT_ROOM_3, "Weight Room 3"),
        (BOXING_GYM, "Boxing Gym"),
        (CROSSFIT_GYM, "CrossFit Gym"),
        (WIND_TUNNEL, "Wind Tunnel"),
        (DANCE_STUDIO, "Dance Studio"),
    ]

    name = models.CharField(max_length=50, choices=SPACE_CHOICES, unique=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TrainingSession(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    attendance = models.BooleanField(default=False)
    progress_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Session with {self.member.name} and {self.trainer.name} on {self.date}"
    
class FoodLog(models.Model):
    MEAL_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("snack", "Snack"),
    ]

    member = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal = models.CharField(max_length=10, choices=MEAL_CHOICES)
    category = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    kilocalories = models.FloatField()

    def __str__(self):
        return f"{self.member.username} - {self.date} - {self.meal}"

