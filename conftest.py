import pytest
import django_project.settings

@pytest.fixture(scope='session')
def django_db_setup():
  django_project.settings.DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    "ATOMIC_REQUESTS": True,
    'NAME': 'db.sqlite3',
  }
