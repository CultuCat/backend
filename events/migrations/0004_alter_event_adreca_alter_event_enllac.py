# Generated by Django 4.2.6 on 2023-10-20 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_alter_event_datafi_alter_event_dataini_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='adreca',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='enllac',
            field=models.CharField(blank=True, null=True),
        ),
    ]
