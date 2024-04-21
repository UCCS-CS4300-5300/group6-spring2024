# Generated by Django 5.0.2 on 2024-04-01 00:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('is_recommended', models.BooleanField(default=False, verbose_name='Recommended by Admin')),
                ('image', models.ImageField(blank=True, default='images/foodie-joint-logo.png', null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=500)),
                ('location_type', models.CharField(choices=[('Restaurant', 'Restaurant'), ('Store', 'Store')], max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, default='images/foodie-joint-logo.png', null=True, upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='LocationTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('Food', 'Food'), ('Drink', 'Drink'), ('Gas Station', 'Gas Station'), ('Supermarket', 'Supermarket'), ('Specialty Store', 'Specialty Store'), ('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Gluten Free', 'Gluten Free'), ('Pizza', 'Pizza'), ('Chicken', 'Chicken'), ('Burger', 'Burger'), ('Bar', 'Bar'), ('Sandwiches', 'Sandwiches'), ('Salads', 'Salads'), ('Breakfast', 'Breakfast'), ('Brunch', 'Brunch'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Dessert', 'Dessert'), ('Coffee', 'Coffee'), ('Outside Dining', 'Outside Dining'), ('Italian', 'Italian'), ('Mexican', 'Mexican'), ('Chinese', 'Chinese'), ('Seafood', 'Seafood'), ('Pet Friendly', 'Pet Friendly'), ('Fast Food', 'Fast Food'), ('Fine Dining', 'Fine Dining'), ('Locally Owned', 'Locally Owned')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ItemReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('review', models.TextField()),
                ('num_stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.item')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.item')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='location',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.location'),
        ),
        migrations.AddField(
            model_name='location',
            name='tags',
            field=models.ManyToManyField(to='Foodie_Joint.locationtag'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('review', models.TextField()),
                ('num_stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.location')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Foodie_Joint.location')),
            ],
        ),
    ]
