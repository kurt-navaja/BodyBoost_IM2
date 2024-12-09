# Generated by Django 5.1.1 on 2024-12-03 02:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Signup", "0006_customuser_intensity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_photo",
            field=models.ImageField(
                blank=True,
                default="static/images/profile_photo.png",
                null=True,
                upload_to="profile_photos/",
            ),
        ),
    ]