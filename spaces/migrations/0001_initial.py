# Generated by Django 4.2.6 on 2023-10-20 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('nom', models.CharField(primary_key=True, serialize=False)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
    ]