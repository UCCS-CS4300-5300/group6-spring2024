# Generated by Django 5.0.2 on 2024-03-08 21:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0004_tag_user_remove_review_location_review_date_created_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='type',
        ),
        migrations.AddField(
            model_name='review',
            name='location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.location'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ItemReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('review', models.TextField()),
                ('num_stars', models.IntegerField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.item')),
            ],
        ),
    ]