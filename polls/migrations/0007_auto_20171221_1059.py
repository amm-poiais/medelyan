# Generated by Django 2.0 on 2017-12-21 07:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_auto_20171221_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userquestionanswer',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
