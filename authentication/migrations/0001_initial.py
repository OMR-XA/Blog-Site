# Generated by Django 5.0.2 on 2024-06-08 07:30

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
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(max_length=10000)),
                ('publish', models.BooleanField(default=False)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('date', models.DateField(null=True)),
                ('time', models.TimeField(null=True)),
                ('slug', models.SlugField(unique=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk', 'date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=10000)),
                ('date', models.DateField(blank=True, null=True)),
                ('time', models.TimeField(blank=True, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('bp', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.blogpost')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk', 'date'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.SlugField(max_length=255, unique=True)),
                ('birthday', models.DateField(null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='image/')),
                ('friends', models.ManyToManyField(blank=True, related_name='friends_of', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_notifications', models.BooleanField(default=False)),
                ('notifications', models.BooleanField(default=False)),
                ('posts_visibility', models.CharField(choices=[('public', 'Public'), ('private', 'Private'), ('friends', 'Friends Only')], default='public', max_length=100)),
                ('account_privacy', models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='public', max_length=100)),
                ('theme', models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('blue', 'Blue')], default='dark', max_length=100)),
                ('language', models.CharField(choices=[('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('de', 'German'), ('ar', 'Arabic')], default='en', max_length=100)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]