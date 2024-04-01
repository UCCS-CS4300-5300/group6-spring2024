# Generated by Django 5.0.2 on 2024-03-30 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0014_alter_locationtag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationtag',
            name='name',
            field=models.CharField(choices=[('Food', 'Food'), ('Drink', 'Drink'), ('Vegetarian', 'Vegetarian'), ('Vegan', 'Vegan'), ('Gluten Free', 'Gluten Free'), ('Pizza', 'Pizza'), ('Burger', 'Burger'), ('Bar', 'Bar'), ('Sandwiches', 'Sandwiches'), ('Salads', 'Salads'), ('Breakfast', 'Breakfast'), ('Brunch', 'Brunch'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner'), ('Dessert', 'Dessert'), ('Coffee', 'Coffee'), ('Outside Dining', 'Outside Dining'), ('Italian', 'Italian'), ('Mexican', 'Mexican'), ('Chinese', 'Chinese'), ('Seafood', 'Seafood'), ('Pet Friendly', 'Pet Friendly'), ('Fast Food', 'Fast Food'), ('Fine Dining', 'Fine Dining')], max_length=50),
        ),
    ]