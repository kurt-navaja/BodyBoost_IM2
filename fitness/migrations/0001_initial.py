# Generated by Django 5.1.1 on 2024-10-27 06:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('video_url', models.URLField()),
                ('category', models.CharField(choices=[('strength', 'Strength Training'), ('cardio', 'Cardio'), ('flexibility', 'Flexibility')], max_length=20)),
                ('thumbnail', models.ImageField(upload_to='exercise_thumbnails/')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(choices=[('slim', 'Slim'), ('muscular', 'Muscular'), ('large', 'Large')], max_length=20)),
                ('fitness_level', models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], max_length=20)),
                ('fitness_goal', models.CharField(choices=[('build_muscle', 'Build Muscle'), ('lose_weight', 'Lose Weight'), ('maintain_fitness', 'Maintain Fitness')], max_length=20)),
                ('preferred_style', models.CharField(choices=[('strength', 'Strength Training'), ('cardio', 'Cardio'), ('flexibility', 'Flexibility/Yoga')], max_length=20)),
                ('health_concerns', models.TextField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
