# Generated by Django 5.0.2 on 2024-04-16 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0025_remove_account_first_name_remove_account_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='address',
            field=models.CharField(max_length=255),
        ),
    ]