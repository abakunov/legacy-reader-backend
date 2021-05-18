from django.contrib import admin

from .models import *


# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'pk',)

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(Book)
