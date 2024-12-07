from django.db import models
from django.contrib.auth.models import User
from datetime import date, timedelta

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def create_roles():
        roles = ["Receptionist", "Trainer", "Member", "Manager"]
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

class Member(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    goal_description = models.TextField(default="No Goal Specified")
    goal_date = models.DateField()
    goal_weight = models.IntegerField(default=0)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Trainer(models.Model):
    trainer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

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
        return f"Session with {self.member.first_name} {self.member.last_name} and {self.trainer.first_name} {self.trainer.last_name} on {self.date}"
    
from django.db import models
from django.contrib.auth.models import User

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
    servings = models.FloatField(default=1)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    kilocalories = models.FloatField()

    def __str__(self):
        return f"{self.member.username} - {self.date} - {self.meal}"


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="payments")
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_date = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def is_overdue(self):
        return not self.is_paid and self.due_date < date.today()

    def calculate_fine(self):
        if self.is_overdue():
            overdue_days = (date.today() - self.due_date).days
            return round(overdue_days * 20, 2)
        return 0.00

    def save(self, *args, **kwargs):
        if self.is_overdue():
            self.fine_amount = self.calculate_fine()
        else:
            self.fine_amount = 0.00
        super().save(*args, **kwargs)


class Fine(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    issued_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Fine for Payment {self.payment.id}: ${self.amount}"