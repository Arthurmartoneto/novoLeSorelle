# Generated by Django 5.0 on 2024-04-29 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeSorelle', '0002_food_reserva_delete_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='user',
        ),
        migrations.AddField(
            model_name='reserva',
            name='peso',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
