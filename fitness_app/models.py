from django.db import models

# Create your models here.

from django.db import models

class Member(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    goal_description = models.TextField(default = "No Goal Specified")
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
    description = models.CharField(max_length=255)
    carbohydrate = models.FloatField()
    protein = models.FloatField()
    fat_total_lipid = models.FloatField()
    kilocalories = models.FloatField()

class Space(models.Model):
    name = models.CharField(max_length=100)
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
