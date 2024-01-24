# Generated by Django 4.2.3 on 2023-08-12 22:16

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
            name="Author",
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
                ("fullname", models.CharField(max_length=255)),
                ("born_date", models.CharField(max_length=100)),
                ("born_location", models.CharField(max_length=255)),
                ("description", models.TextField()),
                (
                    "user",
                    models.ForeignKey(
                        help_text="The user who created the quote",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_related",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Quote",
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
                ("quote", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quotes",
                        to="quotes.author",
                    ),
                ),
                ("tags", models.ManyToManyField(to="quotes.tag")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quote_related",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="quote",
            constraint=models.UniqueConstraint(
                fields=("user", "quote"), name="unique_quote_constraint"
            ),
        ),
        migrations.AddConstraint(
            model_name="author",
            constraint=models.UniqueConstraint(
                fields=("user", "fullname"), name="unique_author_constraint"
            ),
        ),
    ]