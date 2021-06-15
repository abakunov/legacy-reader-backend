from django.db.models import fields
from rest_framework import serializers

from core.models import User, Book, Review, Genre, Category, Promo, Chapter, Author


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['balance']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genre = GenreSerializer()
    category = CategorySerializer()
    class Meta:
        model = Book
        fields = '__all__'

    
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['font_size', 'distance_between_lines', 'side_padding', 'brightness', 'theme', 'background_color', 'text_color']
        