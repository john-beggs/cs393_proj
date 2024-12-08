from django.core.management.base import BaseCommand
from fitness_app.models import Trainer, Food, Member, Payment, Fine, Space
import csv
import os
from datetime import datetime


class Command(BaseCommand):
    help = 'Load payments, fines, and spaces data'

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        trainers_csv = os.path.join(base_dir, 'trainers_famous_actors.csv')
        food_csv = os.path.join(base_dir, 'cleaned_food_will.csv')
        members_csv = os.path.join(base_dir, 'members_data.csv')
        session_csv = os.path.join(base_dir, 'cleaned_sessions.csv')
        payments_csv = os.path.join(base_dir, 'payments_data.csv')
        fines_csv = os.path.join(base_dir, 'fines_data.csv')
        spaces_csv = os.path.join(base_dir, 'spaces_data.csv')

        # Load Payments
        try:
            with open(payments_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Payment.objects.create(
                        member_id=row['member_id'],
                        amount_due=row['amount_due'],
                        due_date=datetime.strptime(row['due_date'], "%Y-%m-%d").date(),
                        payment_date=datetime.strptime(row['payment_date'], "%Y-%m-%d").date() if row['payment_date'] else None,
                        is_paid=row['is_paid'] == 'True',
                        fine_amount=row['fine_amount']
                    )
            self.stdout.write(self.style.SUCCESS('Payments loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading payments: {e}'))


        # Load Fines
        try:
            with open(fines_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if Payment.objects.filter(id=row['payment_id']).exists():
                        Fine.objects.create(
                            payment_id=row['payment_id'],
                            amount=row['amount'],
                            issued_date=datetime.strptime(row['issued_date'], "%Y-%m-%d").date()
                        )
                    else:
                        self.stderr.write(self.style.WARNING(f"Skipping fine with invalid payment_id: {row['payment_id']}"))
            self.stdout.write(self.style.SUCCESS('Fines loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading fines: {e}'))


        # Load Spaces
        try:
            with open(spaces_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Space.objects.create(
                        name=row['name'],
                        is_available=row['is_available'] == 'True'
                    )
            self.stdout.write(self.style.SUCCESS('Spaces loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading spaces: {e}'))


        # trainers_csv = os.path.join(base_dir, 'trainers_famous_actors.csv')
        # food_csv = os.path.join(base_dir, 'cleaned_food_will.csv')
        # members_csv = os.path.join(base_dir, 'members_data.csv')

        # Load trainers
        # try:
        #     with open(trainers_csv, newline='', encoding='utf-8') as csvfile:
        #         reader = csv.DictReader(csvfile)
        #         for row in reader:
        #             if not Trainer.objects.filter(trainer_id=row['trainer_id']).exists():
        #                 Trainer.objects.create(
        #                     trainer_id=row['trainer_id'], 
        #                     first_name=row['first_name'], 
        #                     last_name=row['last_name']
        #                 )
        #     self.stdout.write(self.style.SUCCESS('Trainers loaded successfully'))
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f'Error loading trainers: {e}'))

        # # Load food
        # try:
        #     with open(food_csv, newline='', encoding='utf-8') as csvfile:
        #         reader = csv.DictReader(csvfile)
        #         for row in reader:
        #             try:
        #                 Food.objects.create(
        #                     category=row['category'],
        #                     description=row['description'],
        #                     carbohydrate=row['carbohydrate'],
        #                     protein=row['protein'],
        #                     fat_total_lipid=row['fat_total_lipid'],
        #                     kilocalories=row['kilocalories'],
        #                     serv_grams=row['serv_grams'],  # Include serv_grams
        #                     serv_desc=row['serv_desc'],    # Include serv_desc
        #                 )
        #             except Exception as food_error:
        #                 self.stderr.write(self.style.ERROR(f"Error processing food: {row}. {food_error}"))
        #     self.stdout.write(self.style.SUCCESS('Food loaded successfully'))
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f'Error loading food: {e}'))

        # # Load members
        # try:
        #     with open(members_csv, newline='', encoding='utf-8') as csvfile:
        #         reader = csv.DictReader(csvfile)
        #         for row in reader:
        #             try:
        #                 Member.objects.create(
        #                     first_name=row['first_name'],
        #                     last_name=row['last_name'],
        #                     street_address=row['street_address'],
        #                     city=row['city'],
        #                     state=row['state'],
        #                     zipcode=row['zipcode'],
        #                     date_of_birth=row['date_of_birth'],
        #                     goal_description=row['goal_description'],
        #                     goal_date=row['goal_date'],
        #                     goal_weight=row['goal_weight'],
        #                     date_joined=row['date_joined'],
        #                 )
        #             except Exception as member_error:
        #                 self.stderr.write(self.style.ERROR(f'Error processing member: {row}. {member_error}'))
        #     self.stdout.write(self.style.SUCCESS('Members loaded successfully'))
        # except Exception as e:
        #     self.stderr.write(self.style.ERROR(f'Error loading members: {e}'))

        # Load sessions
        try:
            with open(session_csv, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        TrainingSession.objects.create(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            street_address=row['street_address'],
                            city=row['city'],
                            state=row['state'],
                            zipcode=row['zipcode'],
                            date_of_birth=row['date_of_birth'],
                            goal_description=row['goal_description'],
                            goal_date=row['goal_date'],
                            goal_weight=row['goal_weight'],
                            date_joined=row['date_joined'],
                        )
                    except Exception as session_error:
                        self.stderr.write(self.style.ERROR(f'Error processing session: {row}. {session_error}'))
            self.stdout.write(self.style.SUCCESS('Members loaded successfully'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error loading session: {e}'))