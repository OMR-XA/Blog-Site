# Generated by Django 5.0.2 on 2024-05-24 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reg', '0002_alter_blogpost_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
