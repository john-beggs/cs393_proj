from django.core.management.base import BaseCommand
from fitness_app.models import Trainer, Food
import csv
import os

class Command(BaseCommand):
    help = 'Load necessary data'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        trainers_csv = os.path.join(base_dir, 'trainers.csv')
        food_csv = os.path.join(base_dir, 'cleaned_food.csv')

        try:
            with open(trainers_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Trainer.objects.create(trainer_id=row['trainer_id'], name=row['name'])
            self.stdout.write(self.style.SUCCESS('Trainers loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading trainers: {e}'))

        try:
            with open(food_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Food.objects.create(
                        description=row['description'],
                        carbohydrate=row['carbohydrate'],
                        protein=row['protein'],
                        fat_total_lipid=row['fat_total_lipid'],
                        kilocalories=row['kilocalories']
                    )
            self.stdout.write(self.style.SUCCESS('Food loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading food: {e}'))

