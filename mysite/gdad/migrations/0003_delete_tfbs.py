# Generated by Django 4.1.7 on 2023-06-02 08:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("gdad", "0002_alter_gda_gene_pli"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Tfbs",
        ),
    ]