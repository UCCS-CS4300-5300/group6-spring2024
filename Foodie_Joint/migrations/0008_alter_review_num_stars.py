from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Foodie_Joint', '0007_remove_location_type_remove_user_zipcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='num_stars',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], max_length=10),
        ),
    ]
