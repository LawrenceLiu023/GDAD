# Generated by Django 4.1.7 on 2023-03-14 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="G4",
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
                ("chr", models.CharField(default="", max_length=31)),
                ("start", models.PositiveIntegerField()),
                ("end", models.PositiveIntegerField()),
                ("strand", models.CharField(default="", max_length=1)),
                ("cell_line", models.CharField(default="", max_length=63)),
                ("technology", models.CharField(default="", max_length=63)),
                ("doi", models.CharField(default="", max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Gda",
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
                ("gene_id", models.CharField(default="", max_length=31)),
                ("gene_symbol", models.CharField(default="", max_length=31)),
                ("uniprot_id", models.CharField(default="", max_length=63)),
                ("gene_dsi", models.FloatField()),
                ("gene_dpi", models.FloatField()),
                ("gene_pli", models.FloatField()),
                ("protein_class", models.CharField(default="", max_length=31)),
                ("protein_class_name", models.CharField(default="", max_length=63)),
                ("disease_id", models.CharField(default="", max_length=15)),
                ("disease_name", models.CharField(default="", max_length=255)),
                ("disease_class", models.CharField(default="", max_length=255)),
                ("disease_class_name", models.CharField(default="", max_length=1023)),
                ("disease_type", models.CharField(default="", max_length=15)),
                ("disease_semantic_type", models.CharField(default="", max_length=255)),
                ("gda_score", models.FloatField()),
                ("ei", models.FloatField()),
                ("el", models.CharField(default="", max_length=31)),
                ("year_initial", models.PositiveIntegerField()),
                ("year_final", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="GeneSequence",
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
                ("chr", models.CharField(default="", max_length=31)),
                ("start", models.PositiveIntegerField()),
                ("end", models.PositiveIntegerField()),
                ("gene_symbol", models.CharField(default="", max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name="Tfbs",
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
                ("chr", models.CharField(default="", max_length=31)),
                ("start", models.PositiveIntegerField()),
                ("end", models.PositiveIntegerField()),
                ("tf", models.CharField(default="", max_length=31)),
                ("cell_line", models.CharField(default="", max_length=1023)),
            ],
        ),
    ]