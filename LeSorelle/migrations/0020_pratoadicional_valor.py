# Generated by Django 5.0 on 2024-05-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeSorelle', '0019_alter_pratoadicional_peso'),
    ]

    operations = [
        migrations.AddField(
            model_name='pratoadicional',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
