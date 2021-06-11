from django.db.models import query
from django.http import request
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from core.models import User, Book
from .serializers import *
from app.settings import BASE_URL


class GetUserDataView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UpdateUserDataView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class GetDetailedBookView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class GetBalanceView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [AllowAny]


class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]


class GetGenresView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [AllowAny]


class GetPromoView(generics.ListAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = [AllowAny]


class GetCategoryView(views.APIView):
    def get(self, request):
        # try:
            queryset = Category.objects.all()
            data = []
            for category in queryset:
                first_books = BookSerializer(Book.objects.filter(category=category)[:10], many=True).data
                for b in first_books:
                    b['image'] = BASE_URL + b['image']
                data.append({
                    'id': category.pk,
                    'name': category.name,
                    'first_books': first_books,
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetFavouriteBooksView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.get(pk=self.request.GET['user']).favourite_books.all()


class AddFavouriteBooksView(views.APIView):
    def post(self, request):
        try:
            action = request.data['action']
            user = User.objects.get(pk=request.data['user'])
            book = Book.objects.get(pk=request.data['book'])
            
            if action == 'add':
                user.favourite_books.add(book)
            if action == 'remove':
                user.favourite_books.remove(book)
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)