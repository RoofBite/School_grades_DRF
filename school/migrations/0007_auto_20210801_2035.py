# Generated by Django 3.2.5 on 2021-08-01 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("school", "0006_auto_20210729_2226"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schoolsubject",
            name="teacher",
        ),
        migrations.AddField(
            model_name="schoolsubject",
            name="teacher",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="student",
            name="subject",
            field=models.ManyToManyField(to="school.SchoolSubject"),
        ),
    ]
