# Generated by Django 4.2.6 on 2023-11-20 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(null=True, unique=True)),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
            ],
        ),
    ]
