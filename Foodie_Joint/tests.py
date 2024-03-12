from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import User


class UsersTests(TestCase):
  
    new_user1 = User.objects.create_user(username = 'new_user1', password = 'adfjkfjk;fds2342', email = 'new1@user.com')

    new_user2 = User.objects.create_user(username = 'new_user2', password = 'adfjkfjk;fds2342', email = 'new2@user.com')

    new_user1.save()
    new_user2.save()
  
    assert(new_user1.username == 'new_user1')
    assert(new_user2.password == "adfjkfjk;fds2342")