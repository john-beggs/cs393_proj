from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fitness_app.models import Member, Trainer, Role, UserRole

class Command(BaseCommand):
    help = "Create user accounts for members and trainers with aligned primary keys"

    def handle(self, *args, **kwargs):
        # Create default roles if they don't exist
        Role.create_roles()
        member_role = Role.objects.get(name="Member")
        trainer_role = Role.objects.get(name="Trainer")

        # Create accounts for members
        for member in Member.objects.all():
            username = f"{member.first_name.lower()}.{member.last_name.lower()}"
            if not User.objects.filter(username=username).exists():
                # Create the user with an explicit ID matching the member's PK
                user = User(
                    id=member.pk,  # Set the ID explicitly
                    username=username,
                    first_name=member.first_name,
                    last_name=member.last_name,
                )
                user.set_password('password')  # Set the password
                user.save()

                # Link the user to the member and assign role
                member.user = user
                member.save()
                UserRole.objects.create(user=user, role=member_role)
                self.stdout.write(self.style.SUCCESS(f"Created account for member {username}"))

        # Create accounts for trainers
        for trainer in Trainer.objects.all():
            username = f"{trainer.first_name.lower()}.{trainer.last_name.lower()}"
            if not User.objects.filter(username=username).exists():
                # Create the user without aligning PK for trainers (if not needed)
                user = User.objects.create_user(
                    username=username,
                    password='password',
                    first_name=trainer.first_name,
                    last_name=trainer.last_name,
                )
                trainer.user = user
                trainer.save()
                UserRole.objects.create(user=user, role=trainer_role)
                self.stdout.write(self.style.SUCCESS(f"Created account for trainer {username}"))
