from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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

    # required
    username = models.CharField(max_length=30, unique=True, blank=True)
    email = models.EmailField(verbose_name="email", max_length=60, blank=True)

    # optional

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
	name = models.CharField(max_length=64, verbose_name='Жанры')

	def __str__(self):
		return self.name
        

class Book(models.Model):
	genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name='Жанр')
	title = models.CharField(max_length=100, blank=True)
	paper_count = models.IntegerField(blank=True)
	rating = models.CharField(max_length=50, blank=True)
	rating_count = models.IntegerField(blank=True)
	status = models.CharField(max_length=50, blank=True)
	category = models.IntegerField(blank=True)
	photo = models.ImageField(blank=True)
	short_description = models.TextField(blank=True)

	def __str__(self):
		return self.title