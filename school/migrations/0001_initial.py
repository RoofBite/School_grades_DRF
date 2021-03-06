# Generated by Django 3.2.5 on 2021-07-25 13:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="School",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="SchoolClass",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="school.school",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SchoolSubject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Teacher",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("school", models.ManyToManyField(to="school.School")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                (
                    "school",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="school.school",
                    ),
                ),
                (
                    "school_class",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="school.schoolclass",
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="school.schoolsubject",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="schoolsubject",
            name="teacher",
            field=models.ManyToManyField(to="school.Teacher"),
        ),
        migrations.AddField(
            model_name="schoolclass",
            name="subject",
            field=models.ManyToManyField(to="school.SchoolSubject"),
        ),
        migrations.AddField(
            model_name="schoolclass",
            name="supervising_teacher",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="school.teacher",
            ),
        ),
    ]
