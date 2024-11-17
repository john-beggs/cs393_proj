# Generated by Django 4.2.16 on 2024-11-17 05:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fitness_app', '0002_space_rename_goal_weight_date_member_goal_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingsession',
            name='attendance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='trainingsession',
            name='progress_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='goal_description',
            field=models.TextField(default='No Goal Specified'),
        ),
    ]
