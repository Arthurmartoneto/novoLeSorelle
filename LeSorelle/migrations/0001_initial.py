# Generated by Django 4.0.4 on 2024-05-29 18:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_food', models.CharField(max_length=100)),
                ('img', models.ImageField(upload_to='foods/')),
                ('descricao', models.TextField()),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('ativo', 'Ativo'), ('inativo', 'Inativo')], default='ativo', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=20)),
                ('peso', models.CharField(max_length=10, null=True)),
                ('modo', models.CharField(choices=[('fresco', 'Fresco'), ('congelado', 'Congelado'), ('Aquecido', 'Aquecido')], max_length=10, null=True)),
                ('date', models.DateField(null=True)),
                ('hora', models.CharField(max_length=10, null=True)),
                ('status', models.CharField(choices=[('pendente', 'Pendente'), ('em_preparo', 'Em Preparo'), ('pronto', 'Pronto'), ('finalizado', 'Finalizado'), ('cancelado', 'Cancelado')], default='pendente', max_length=20)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservas_principal', to='LeSorelle.food')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PratoAdicional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.CharField(max_length=10, null=True)),
                ('modo', models.CharField(choices=[('fresco', 'Fresco'), ('congelado', 'Congelado'), ('aquecido', 'Aquecido')], max_length=10, null=True)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pratos_adicionais_food', to='LeSorelle.food')),
                ('reserva', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pratos_adicionais_reserva', to='LeSorelle.reserva')),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('img', models.ImageField(upload_to='blog/')),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
