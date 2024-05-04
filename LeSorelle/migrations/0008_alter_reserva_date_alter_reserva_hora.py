# Generated by Django 4.0.4 on 2024-05-02 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LeSorelle', '0007_alter_reserva_hora_alter_reserva_horario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='date',
            field=models.DateField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='reserva',
            name='hora',
            field=models.CharField(choices=[('08:00', '08:00'), ('09:00', '09:00'), ('10:00', '10:00'), ('20:00', '20:00')], max_length=10, null=True),
        ),
    ]