# Generated by Django 5.0.4 on 2024-04-21 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_answer_user_alter_test_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='user',
        ),
        migrations.AddField(
            model_name='test',
            name='user',
            field=models.ManyToManyField(blank=True, null=True, to='app.customuser'),
        ),
    ]
