from django.db import models

# Create your models here.
class Location(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)
  #Possibly subject to change, if we keep type then we only need 2 classes, 
  #but otherwise we'll need 4 classes. (Store or Restaurant)
  type = models.CharField(max_length=10)
  address = models.CharField(max_length=50)

  def __str__(self):
    return f"{self.name}: {self.description} ({self.type}, {self.address})"


#Based on user stories, the item class will have to be updated
class Item(models.Model):
  name = models.CharField(max_length=50)
  description = models.CharField(max_length=500)
  location = models.ForeignKey(Location, on_delete=models.CASCADE, default=None)
  is_recommended = models.BooleanField(default=False, verbose_name="Recommended by Admin")
  # define return string
  def __str__(self):
    return f"{self.name}: {self.description}"

class User(models.Model):
  username = models.CharField(max_length=50)
  firstName = models.CharField(max_length=50)
  lastName = models.CharField(max_length=50)
  password = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  zipcode = models.CharField(max_length=10)

  def __str__(self):
    return f"{self.username}"

class Review(models.Model):
  user = models.CharField(max_length=50)
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField()
  date_created = models.DateTimeField(auto_now_add=True)
  #define return string
  def __str__(self):
    return f"{self.user} - {self.review} {self.num_stars} {self.date_created}"
    # Probably shouldnt have the review in the string representation of obj (Tyler)

class ItemReview(models.Model):
  user = models.CharField(max_length=50)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  #review = models.CharField(max_length=200)
  review = models.TextField()  # Changed this to not limit length (Tyler)
  num_stars = models.IntegerField()
  date_created = models.DateTimeField(auto_now_add=True)
  #define return string
  def __str__(self):
    return f"{self.user} - {self.review} {self.num_stars} {self.date_created}"
    # Probably shouldnt have the review in the string representation of obj (Tyler)

class Tag(models.Model):
  title = models.CharField(max_length=50)
  if (type=="Location"):
    object = models.ForeignKey(Location, on_delete=models.CASCADE)
  elif (type=="Item"):
    object = models.ForeignKey(Item, on_delete=models.CASCADE)
  def __str__(self):
    return f"{self.title}"