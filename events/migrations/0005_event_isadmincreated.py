# Generated by Django 4.2.6 on 2023-10-24 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_event_adreca_alter_event_enllac'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='isAdminCreated',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]