from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Promo)
admin.site.register(Chapter)
admin.site.register(BookStatus)
admin.site.register(Price)