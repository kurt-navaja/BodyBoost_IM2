# Generated by Django 5.1.1 on 2024-12-03 23:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Signup", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="intensity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Gentle", "Gentle (0.3kg / week)"),
                    ("Light", "Light (0.6kg / week)"),
                    ("Moderate", "Moderate (0.75kg / week)"),
                    ("Aggressive", "Aggressive (1kg / week)"),
                    ("High Intensity", "High Intensity (1.25kg / week)"),
                ],
                max_length=20,
                null=True,
            ),
        ),
    ]
