# Generated by Django 5.1.2 on 2024-11-03 13:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(choices=[('TB2', 'TB2'), ('TB3', 'TB3'), ('AKINCI', 'AKINCI'), ('KIZILELMA', 'KIZILELMA')], max_length=50, unique=True)),
                ('assembled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Personel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('KANAT_TAKIMI', 'Kanat Takımı'), ('GÖVDE_TAKIMI', 'Gövde Takımı'), ('KUYRUK_TAKIMI', 'Kuyruk Takımı'), ('AVİYONİK_TAKIMI', 'Aviyonik Takımı'), ('MONTAJ_TAKIMI', 'Montaj Takımı')], max_length=50, unique=True)),
                ('part_type', models.CharField(blank=True, choices=[('KANAT', 'Kanat'), ('GÖVDE', 'Gövde'), ('KUYRUK', 'Kuyruk'), ('AVİYONİK', 'Aviyonik')], max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('type', models.CharField(choices=[('KANAT', 'Kanat'), ('GÖVDE', 'Gövde'), ('KUYRUK', 'Kuyruk'), ('AVİYONİK', 'Aviyonik')], max_length=20)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specific_parts', to='aircraft.aircraft')),
            ],
        ),
        migrations.CreateModel(
            name='AircraftPart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aircraft.aircraft')),
                ('part', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aircraft.part')),
            ],
        ),
        migrations.AddField(
            model_name='aircraft',
            name='parts',
            field=models.ManyToManyField(related_name='aircrafts', through='aircraft.AircraftPart', to='aircraft.part'),
        ),
    ]
