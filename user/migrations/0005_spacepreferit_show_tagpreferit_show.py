# Generated by Django 4.2.6 on 2023-12-06 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_perfil_espais_preferits_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='spacepreferit',
            name='show',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='tagpreferit',
            name='show',
            field=models.BooleanField(default=True),
        ),
    ]