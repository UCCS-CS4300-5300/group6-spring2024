import django_filters
from .models import Review, ItemReview


class ReviewFilter(django_filters.FilterSet):
  NUM_STARS = {
      1: '1',
      2: '2',
      3: '3',
      4: '4',
      5: '5',
  }
  num_stars = django_filters.ChoiceFilter(choices=NUM_STARS, label="Stars")
  
  class Meta:
    model = Review
    fields = ['num_stars']
    


class ItemReviewFilter(django_filters.FilterSet):
  NUM_STARS = {
    1: '1',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
  }
  num_stars = django_filters.ChoiceFilter(choices=NUM_STARS, label="Stars")
  
  class Meta:
    model = ItemReview
    fields = ['num_stars']
    
