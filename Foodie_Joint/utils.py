from .models import LocationTag

# Created a function to create tag objects (trying tags as seperate model)
def instantiate_tags():
  for tag_name, _ in LocationTag.TAG_CHOICES:
    if not LocationTag.objects.filter(name=tag_name).exists():
      LocationTag.objects.create(name=tag_name)