# Generated by Django 4.2.6 on 2024-01-08 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='space',
            name='nom',
            field=models.CharField(blank=True, default='', unique=True),
        ),
    ]
