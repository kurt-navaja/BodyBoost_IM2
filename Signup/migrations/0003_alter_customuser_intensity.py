# Generated by Django 5.1.1 on 2024-12-04 00:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Signup", "0002_alter_customuser_intensity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="intensity",
            field=models.CharField(
                blank=True,
                choices=[
                    ("0.3", "Gentle (0.3kg / week)"),
                    ("0.6", "Light (0.6kg / week)"),
                    ("0.7", "Moderate (0.75kg / week)"),
                    ("0.8", "Aggressive (1kg / week)"),
                    ("0.9", "High Intensity (1.25kg / week)"),
                ],
                max_length=10,
                null=True,
            ),
        ),
    ]