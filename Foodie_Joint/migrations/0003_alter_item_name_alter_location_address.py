# Generated by Django 5.0.2 on 2024-05-01 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0002_alter_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
