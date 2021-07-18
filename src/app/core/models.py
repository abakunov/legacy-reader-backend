from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.fields import proxy
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import ebooklib
from ebooklib import epub
from app.settings import BASE_URL
from .book_helpers import epub2text, epub2thtml
from .chapters_parser import create_chapters
import time
import sys,os
import epub_meta

def parse_chapters(path):
    data = epub_meta.get_epub_metadata(path, read_toc=True)
    chapters = data['toc']
    result = []
    for c in chapters:
        result.append({
            'index': c['index'],
            'title': c['title']
        })
    return result

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender='core.Book')
def create_chapters(sender, instance=None, created=False, **kwargs):
    if created:
        path = instance.file.path
        data = parse_chapters(path)
        create = True
        for c in data:
            if c['title'] == 'Примечания':
                break
            else:
                Chapter.objects.create(name=c['title'], index=int(c['index']), book=instance) 


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    name = models.CharField(max_length=30, blank=True, null=True)
    username = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, blank=True)
    balance = models.PositiveIntegerField(blank=True, null=True)
    SEX_CATEGORIES = [
        ('Male', 'Мужской'),
        ('Female', 'Женский'),
    ]
    sex = models.CharField(max_length=30, blank=True, null=True, choices=SEX_CATEGORIES)
    favourite_books = models.ManyToManyField('core.Book', blank=True)
    unlocked_chapters = models.ManyToManyField('core.Chapter', blank=True)

    #settings
    FONT_SIZE_CATEGORIES = [
        ('Standart', 'Стандартный'),
        ('Big', 'Большой'),
        ('Very big', 'Очень большой'),
    ]
    font_size = models.CharField(max_length=30, blank=True, null=True, choices=FONT_SIZE_CATEGORIES)
    distance_between_lines = models.PositiveIntegerField(blank=True, null=True)
    side_padding = models.PositiveIntegerField(blank=True, null=True)
    brightness = models.PositiveIntegerField(blank=True, null=True)
    THEME_CHOICES = [
        ('White', 'Белая'),
        ('Sepia', 'Сепия'),
        ('Night', 'Ночная'),
        ('Custom', 'Пользовательская'),
    ]
    theme = models.CharField(max_length=30, blank=True, null=True, choices=THEME_CHOICES)
    COLOR_CHOICES = [
        ('White', 'Белый'),
        ('Black', 'Черный'),
        ('Red', 'Красный'),
        ('Blue', 'Синий'),
        ('Green', 'Зеленый'),
        ('Brown', 'Коричневый'),
    ]
    background_color = models.CharField(max_length=50, blank=True, null=True, choices=COLOR_CHOICES)
    text_color = models.CharField(max_length=50, blank=True, null=True, choices=COLOR_CHOICES)

    # system
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser



class Genre(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, null=True)

    @property
    def image_url(self):
        return BASE_URL + '/media/' + str(self.image)

    def __str__(self):
        return self.name


class Promo(models.Model):
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    @property
    def image_url(self):
        return BASE_URL + '/media/' + str(self.image)


class BookStatus(models.Model):
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE, blank=True, null=True)
    chapter = models.ForeignKey('core.Chapter', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(blank=True, null=True)

    @property
    def image_url(self):
        return BASE_URL + '/media/' + str(self.image)

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE, blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)


class Chapter(models.Model):
    name = models.CharField(max_length=64)
    cost = models.PositiveIntegerField(blank=True, null=True, default=50)
    index = models.PositiveIntegerField(blank=True, null=True)
    book = models.ForeignKey('core.Book', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    @property
    def image_url(self):
        return BASE_URL + '/media/' + str(self.image)

    def __str__(self):
	    return str(self.first_name) + ' '  + str(self.last_name)


class Price(models.Model):
    fiat_price = models.PositiveIntegerField(blank=True, null=True, default=0)
    coins = models.PositiveIntegerField(blank=True, null=True, default=0)
    bonus = models.PositiveIntegerField(blank=True, null=True, default=0)
        

class Book(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True, default='')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True)
    AGE_CATEGORIES = [
        ('0+', '0+'),
        ('6+', '6+'),
        ('12+', '12+'),
        ('16+', '16+'),
        ('18+', '18+')
    ]
    age_category = models.CharField(blank=True, null=True, max_length=10, choices=AGE_CATEGORIES, default='0+')
    paper_count = models.IntegerField(blank=True, null=True, default=0)
    rating = models.FloatField(blank=True, null=True, default=0.0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(blank=True, null=True)


    @property
    def image_url(self):
        return BASE_URL + '/media/' + str(self.image)

    @property
    def reviews_amount(self):
        return len(Review.objects.filter(book=self))

    @property
    def chapters_amount(self):
        return len(Chapter.objects.filter(book=self))

    @property
    def chapters(self):
        return Chapter.objects.filter(book=self)

    def __str__(self):
        return self.title