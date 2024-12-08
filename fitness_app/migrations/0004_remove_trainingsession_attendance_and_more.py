# Generated by Django 5.1.2 on 2024-12-08 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0003_food_serv_desc_food_serv_grams'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainingsession',
            name='attendance',
        ),
        migrations.RemoveField(
            model_name='trainingsession',
            name='member',
        ),
        migrations.RemoveField(
            model_name='trainingsession',
            name='progress_notes',
        ),
        migrations.AlterField(
            model_name='trainingsession',
            name='duration',
            field=models.PositiveIntegerField(),
        ),
    ]
