# Generated by Django 4.2.6 on 2023-12-18 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_from', to='user.perfil')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_to', to='user.perfil')),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
