# Generated by Django 5.0.2 on 2024-02-27 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0002_item_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='is_recommended',
            field=models.BooleanField(default=False, verbose_name='Recommended by Admin'),
        ),
    ]
