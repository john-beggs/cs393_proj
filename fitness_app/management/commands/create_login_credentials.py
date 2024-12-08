from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fitness_app.models import Member, Trainer

class Command(BaseCommand):
    help = "Create or update login credentials for members and trainers."

    def handle(self, *args, **kwargs):
        # self.create_member_users()
        self.create_trainer_users()

    # def create_member_users(self):
    #     members = Member.objects.all()
    #     for member in members:
    #         # Generate username and password
    #         username = f"{member.first_name.lower()}{member.state.lower()}"
    #         password = f"{member.last_name.lower()}{member.state.lower()}"

    #         # Create or update user
    #         user, created = User.objects.update_or_create(
    #             username=username,
    #             defaults={"first_name": member.first_name, "last_name": member.last_name},
    #         )
    #         user.set_password(password)  # Set the password securely
    #         user.save()

    #         if created:
    #             self.stdout.write(self.style.SUCCESS(f"Created user for member: {username}"))
    #         else:
    #             self.stdout.write(self.style.SUCCESS(f"Updated user for member: {username}"))

    def create_trainer_users(self):
        trainers = Trainer.objects.all()
        for trainer in trainers:
            # Generate username and password
            username = f"{trainer.first_name.lower()}{trainer.last_name.lower()}"
            password = f"{trainer.last_name.lower()}"

            # Create or update user
            user, created = User.objects.update_or_create(
                username=username,
                defaults={"first_name": trainer.first_name, "last_name": trainer.last_name},
            )
            user.set_password(password)  # Set the password securely
            user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user for trainer: {username}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated user for trainer: {username}"))



