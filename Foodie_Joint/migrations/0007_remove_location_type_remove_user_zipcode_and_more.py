# Generated by Django 5.0.2 on 2024-03-11 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0006_tag_location_itemtag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='type',
        ),
        migrations.RemoveField(
            model_name='user',
            name='zipcode',
        ),
        migrations.AddField(
            model_name='location',
            name='location_type',
            field=models.CharField(choices=[('Restaurant', 'Restaurant'), ('Store', 'Store')], default='Store', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default='1420 Austin Bluffs Pkwy', max_length=50),
            preserve_default=False,
        ),
    ]
