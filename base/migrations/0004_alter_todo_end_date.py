# Generated by Django 3.2.7 on 2021-09-13 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_todo_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='end_date',
            field=models.DateField(null=True, verbose_name='End Date'),
        ),
    ]