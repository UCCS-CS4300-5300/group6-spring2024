import django_filters
from .models import Review, ItemReview


class ReviewFilter(django_filters.FilterSet):
  
  class Meta:
    model = Review
    fields = ['num_stars']


class ItemReviewFilter(django_filters.FilterSet):
  
  class Meta:
    model = ItemReview
    fields = ['num_stars']
