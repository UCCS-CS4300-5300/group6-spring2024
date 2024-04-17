from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.enums import Choices


class LocationTag(models.Model):
  # When more are added, they are instanciated whenever a new location obj is created
  # Sort these?
  TAG_CHOICES = [
      ("Food", "Food"),
      ("Drink", "Drink"),
      ("Gas Station", "Gas Station"),
      ("Supermarket", "Supermarket"),
      ("Specialty Store", "Specialty Store"),
      ("Vegetarian", "Vegetarian"),
      ("Vegan", "Vegan"),
      ("Gluten Free", "Gluten Free"),
      ("Pizza", "Pizza"),
      ("Chicken", "Chicken"),
      ("Burger", "Burger"),
      ("Bar", "Bar"),
      ("Sandwiches", "Sandwiches"),
      ("Salads", "Salads"),
      ("Breakfast", "Breakfast"),
      ("Brunch", "Brunch"),
      ("Lunch", "Lunch"),
      ("Dinner", "Dinner"),
      ("Dessert", "Dessert"),
      ("Coffee", "Coffee"),
      ("Outside Dining", "Outside Dining"),
      ("Italian", "Italian"),
      ("Mexican", "Mexican"),
      ("Chinese", "Chinese"),
      ("Seafood", "Seafood"),
      ("Pet Friendly", "Pet Friendly"),
      ("Fast Food", "Fast Food"),
      ("Fine Dining", "Fine Dining"),
      ("Locally Owned", "Locally Owned"),
  ]
  name = models.CharField(max_length=50, choices=TAG_CHOICES)

  def __str__(self):
    return f"{self.name}"


# Model to extend the base user model - potentially add more fields such as "about me"
class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.user}"


class Location(models.Model):
  RESTAURANT = "Restaurant"
  STORE = "Store"
  LOCATION_CHOICES = {
      RESTAURANT: "Restaurant",
      STORE: "Store",
  }

  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)
  location_type = models.CharField(max_length=10, choices=LOCATION_CHOICES)
  address = models.CharField(max_length=50)
  tags = models.ManyToManyField(LocationTag)
  image = models.ImageField(upload_to='images/',
                            blank=True,
                            null=True,
                            default='images/foodie-joint-logo.png')
  favorites = models.ManyToManyField(User,
                                     related_name="favorites",
                                     default=None,
                                     blank=True)
  is_recommended = models.BooleanField(default=False)

  def __str__(self):
    return f"{self.name}: {self.description} ({self.location_type}, {self.address})"


#Based on user stories, the item class will have to be updated
class Item(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)
  location = models.ForeignKey(Location,
                               on_delete=models.CASCADE,
                               default=None)
  is_recommended = models.BooleanField(default=False,
                                       verbose_name="Recommended by Admin")
  image = models.ImageField(upload_to='images/',
                            blank=True,
                            null=True,
                            default='images/foodie-joint-logo.png')

  # define return string
  def __str__(self):
    return f"{self.name}: {self.description}"


"""
class Address(models.Model):
  user = models.ForeignKey(TrueUser, on_delete=models.CASCADE,
  address = models.CharField(max_length=50))

  def __init__(self, *args, temp=65, **kwargs):
     self.temp = temp
     return super().__init__(*args, **kwargs)


    
@receiver(post_save, sender=TrueUser)
def create_user_address(sender, instance, created, **kwargs):
  if created:
      my_address = Address()
      my_address.user = instance

@receiver(post_save, sender=TrueUser)
def save_user_profile(sender, instance, **kwargs):
  instance.address.save()

  
  
"""


class Review(models.Model):
  NUM_STARS = {
      1: '1',
      2: '2',
      3: '3',
      4: '4',
      5: '5',
  }

  user = models.CharField(max_length=50)
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField(choices=NUM_STARS)
  date_created = models.DateTimeField(auto_now_add=True)

  #define return string
  def __str__(self):
    return f"{self.user} - {self.review} {self.num_stars} {self.date_created}"
    # Probably shouldnt have the review in the string representation of obj (Tyler)


class ItemReview(models.Model):
  NUM_STARS = {
      1: '1',
      2: '2',
      3: '3',
      4: '4',
      5: '5',
  }
  user = models.CharField(max_length=50)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField(choices=NUM_STARS)
  date_created = models.DateTimeField(auto_now_add=True)

  #define return string
  def __str__(self):
    return f"{self.user} - {self.review} {self.num_stars} {self.date_created}"
    # Probably shouldnt have the review in the string representation of obj (Tyler)


class Tag(models.Model):
  title = models.CharField(max_length=50)
  location = models.ForeignKey(Location, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.title}"


class ItemTag(models.Model):
  title = models.CharField(max_length=50)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.title}"
