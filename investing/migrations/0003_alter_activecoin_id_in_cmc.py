# Generated by Django 4.2 on 2024-05-21 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investing', '0002_alter_activecoin_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activecoin',
            name='id_in_cmc',
            field=models.PositiveIntegerField(),
        ),
    ]