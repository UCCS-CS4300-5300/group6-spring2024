# Generated by Django 5.0.2 on 2024-03-13 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0010_alter_review_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.CharField(max_length=20),
        ),
    ]
