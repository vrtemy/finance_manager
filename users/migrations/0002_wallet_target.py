# Generated by Django 4.2 on 2024-05-16 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='target',
            field=models.BooleanField(default=True),
        ),
    ]
