# Generated by Django 3.2.5 on 2021-07-25 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("school", "0002_schoolsubject_school"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="student",
            name="subject",
        ),
        migrations.AddField(
            model_name="student",
            name="subject",
            field=models.ManyToManyField(to="school.SchoolSubject"),
        ),
    ]
