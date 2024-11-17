from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from fitness_app.models import Role, UserRole, Trainer, Member

class Command(BaseCommand):
    help = "Create default users, roles, and assign them to groups"

    def handle(self, **options):
        receptionist_role, _ = Role.objects.get_or_create(name="Receptionist")

        try:
            receptionist_user = User.objects.get(username="receptionist")
        except User.DoesNotExist:
            receptionist_user = User.objects.create_user(
                username="receptionist",
                email="receptionist@example.com",
                password="fuzz"
            )
            receptionist_user.first_name = "Receptionist"
            receptionist_user.last_name = "User"
            receptionist_user.save()

            UserRole.objects.create(user=receptionist_user, role=receptionist_role)

        self.stdout.write(self.style.SUCCESS("username 'receptionist' and password 'fuzz'"))

        try:
            trainer_user = User.objects.get(username='trainer')
        except User.DoesNotExist:
            trainer_user = User.objects.create_user(
                username='trainer',
                email='trainer@example.com',
                password='trainerpassword'
            )
            trainer_user.first_name = 'Trainer'
            trainer_user.last_name = 'User'
            trainer_user.save()

            trainer_role = Role.objects.get(name='Trainer')
            UserRole.objects.create(user=trainer_user, role=trainer_role)

            Trainer.objects.get_or_create(name='Trainer User')
            self.stdout.write(self.style.SUCCESS("Trainer user created"))

        try:
            member_user = User.objects.get(username='member')
        except User.DoesNotExist:
            member_user = User.objects.create_user(
                username='member',
                email='member@example.com',
                password='memberpassword'
            )
            member_user.first_name = 'Member'
            member_user.last_name = 'User'
            member_user.save()

            member_role = Role.objects.get(name='Member')
            UserRole.objects.create(user=member_user, role=member_role)

            Member.objects.get_or_create(name='Member User', address="123 Fitness St", date_of_birth="1990-01-01", goal_description="Lose weight", goal_date="2023-12-31")
            self.stdout.write(self.style.SUCCESS("Member user created"))

        self.stdout.write(self.style.SUCCESS("Default users and roles created successfully"))
