from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.enums import Choices

# Model to associate various locations with 'tags' to help categorize/filter them
# Tags are instanciated whenever a new location object is created ('Add Location' button)
class LocationTag(models.Model):
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


# Model to extend the base user model
class Account(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  address = models.CharField(max_length=255)
  bio = models.TextField(blank=True, null=True) # Optional bio field
  state = models.CharField(max_length=50, blank=False, null=True) # Used to verify location API request
  city = models.CharField(max_length=50, blank=False, null=True)
  profile_picture = models.ImageField(upload_to='images/',
                              blank=True,
                              null=True,
                              default='images/foodie-joint-logo.png')

  def __str__(self):
    return f"{self.user}"

# Model to represent a Location object
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
  # Now has relationship with user who created the Location (Tyler)
  # Accessed in templates via location.created_by (e.g. location.created_by.profile_picture)
  created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return f"{self.name}: {self.description} ({self.location_type}, {self.address})"


# Model to represent a Location's item
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
  # Now has relationship with user who created the item (Tyler)
  created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

  # define return string
  def __str__(self):
    return f"{self.name} ({self.location}): {self.description}"


# Model to represent a review of Location
class Review(models.Model):
  NUM_STARS = {
      1: '1',
      2: '2',
      3: '3',
      4: '4',
      5: '5',
  }
  # Now has relationship with user who created the review (Tyler)
  user = models.ForeignKey(Account, on_delete=models.CASCADE) 
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField(choices=NUM_STARS)
  date_created = models.DateTimeField(auto_now_add=True)

  #define return string
  def __str__(self):
    return f"{self.user}: Created on {self.date_created} ({self.num_stars} stars)"


# Model to represent a review of Location's item
class ItemReview(models.Model):
  NUM_STARS = {
      1: '1',
      2: '2',
      3: '3',
      4: '4',
      5: '5',
  }
  # Now has relationship with user who created the review (Tyler)
  user = models.ForeignKey(Account, on_delete=models.CASCADE) 
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField(choices=NUM_STARS)
  date_created = models.DateTimeField(auto_now_add=True)

  #define return string
  def __str__(self):
    return f"{self.user}: Created on {self.date_created} ({self.num_stars} stars)"



# IF NO PURPOSE REMOVE THESE!!!!
'''
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
'''
