# Generated by Django 3.2.7 on 2021-09-17 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_todo_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='date',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Start Date'),
        ),
    ]
