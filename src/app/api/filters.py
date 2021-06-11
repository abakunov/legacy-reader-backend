from rest_framework import filters
from core.models import User

# class FavouriteBooksFilterBackend(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset):
#         users_favourites = User.objects.get(pk=request.GET['user']).favoutite_books.all()
#         return  