from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from fitness_app.models import Role, UserRole, Trainer, Member

class Command(BaseCommand):
    help = "Create default users, roles, and assign them to groups"

    def handle(self, **options):
        # Create roles
        Role.create_roles()

        # Create Receptionist user
        receptionist_role = Role.objects.get(name="Receptionist")
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

        self.stdout.write(self.style.SUCCESS("Created receptionist with username 'receptionist' and password 'fuzz'"))

        # Create Trainer user
        trainer_role = Role.objects.get(name="Trainer")
        try:
            trainer_user = User.objects.get(username="trainer")
        except User.DoesNotExist:
            trainer_user = User.objects.create_user(
                username="trainer",
                email="trainer@example.com",
                password="trainerpassword"
            )
            trainer_user.first_name = "Trainer"
            trainer_user.last_name = "User"
            trainer_user.save()

            UserRole.objects.create(user=trainer_user, role=trainer_role)
            Trainer.objects.get_or_create(
                first_name="Trainer",
                last_name="User"
            )

        self.stdout.write(self.style.SUCCESS("Created trainer with username 'trainer' and password 'trainerpassword'"))

        # Create Member user
        member_role = Role.objects.get(name="Member")
        try:
            member_user = User.objects.get(username="member")
        except User.DoesNotExist:
            member_user = User.objects.create_user(
                username="member",
                email="member@example.com",
                password="memberpassword"
            )
            member_user.first_name = "Member"
            member_user.last_name = "User"
            member_user.save()

            UserRole.objects.create(user=member_user, role=member_role)
            Member.objects.get_or_create(
                first_name="Member",
                last_name="User",
                street_address="123 Fitness St",
                city="Fitness City",
                state="Fitness State",
                zipcode="12345",
                date_of_birth="1990-01-01",
                goal_description="Lose weight",
                goal_date="2023-12-31",
                goal_weight=150,
            )

        self.stdout.write(self.style.SUCCESS("Created member with username 'member' and password 'memberpassword'"))

        # Create Manager (Owner) user
        manager_role = Role.objects.get(name="Manager")
        try:
            manager_user = User.objects.get(username="owner")
        except User.DoesNotExist:
            manager_user = User.objects.create_user(
                username="owner",
                email="owner@example.com",
                password="ownerpassword"
            )
            manager_user.first_name = "Owner"
            manager_user.last_name = "User"
            manager_user.save()

            UserRole.objects.create(user=manager_user, role=manager_role)

        self.stdout.write(self.style.SUCCESS("Created owner with username 'owner' and password 'ownerpassword'"))

        self.stdout.write(self.style.SUCCESS("Default users and roles created successfully"))