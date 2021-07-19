from django.db.models import query
from django.http import request
from rest_framework import generics, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from core.models import User, Book, Chapter
from .serializers import *
from app.settings import BASE_URL
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GetUserDataView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            data = UserSerializer(user).data
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserDataView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GetPricesView(generics.ListAPIView):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]


class GetDetailedBookView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            book = Book.objects.get(pk=request.GET['book'])
            data = BookSerializer(book).data
            try:
                data['is_in_favourites'] = book in request.user.favourite_books.all()
            except Exception:
                data['is_in_favourites'] = False
            try:
                data['image'] = BASE_URL + data['image']
            except Exception:
                pass
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class TopUpBalance(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            _sum = int(request.GET['sum'])
            user.balance += _sum
            user.save()
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetBooksView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['rating', 'genre', 'category']
    search_fields = ['title']


class GetChaptersListView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # try:
            user = request.GET['user']
            book = request.GET['book']
            queryset = Chapter.objects.filter(book=Book.objects.get(pk=book))
            data = []
            for chapter in queryset:
                data.append({
                    'id': chapter.pk,
                    'name': chapter.name,
                    'book': chapter.book.pk,
                    'cost': chapter.cost,
                    'index': chapter.index,
                    'is_unlocked': chapter in User.objects.get(pk=user).unlocked_chapters.all(),
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetChapterView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            chapter = request.GET['chapter']
            user = request.GET['user']
            chapter = Chapter.objects.get(pk=chapter)
            data = {
                'id': chapter.pk,
                'name': chapter.name,
                'book': chapter.book.pk,
                'cost': chapter.cost,
                'number_in_book': chapter.number_in_book,
                'is_unlocked': chapter in User.objects.get(pk=user).unlocked_chapters.all(),
                'text': chapter.text
            }
            return Response({'data': data}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetBalanceView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = BalanceSerializer
    permission_classes = [IsAuthenticated]


class CreateReviewView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class GetGenresView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAuthenticated]


class GetUsersReadingSettingsView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]


class UpdateUsersReadingSettingsView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSettingsSerializer
    permission_classes = [IsAuthenticated]


class GetPromoView(generics.ListAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    permission_classes = [IsAuthenticated]


class GetCategoryView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
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
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetFavouriteBooksView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return User.objects.get(pk=self.request.GET['user']).favourite_books.all()


class AddFavouriteBooksView(views.APIView):
    permission_classes = [IsAuthenticated]
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


class GetMainPageDataView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # try:
            promo = PromoSerializer(Promo.objects.all(), many=True).data
            genres = GenreSerializer(Genre.objects.all(), many=True).data

            queryset = Category.objects.all()
            categories = []
            for category in queryset:
                first_books = BookSerializer(Book.objects.filter(category=category)[:10], many=True).data
                for b in first_books:
                    if b['image'] is not None:
                        b['image'] = BASE_URL + b['image']
                categories.append({
                    'id': category.pk,
                    'name': category.name,
                    'first_books': first_books,
                })

            data = {
                'promo': promo,
                'genres': genres,
                'categories': categories,
            }
            return Response({'data': data}, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetGenrePageDataView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # try:
            promo = PromoSerializer(Promo.objects.all(), many=True).data
            for p in promo:
                p['image'] = BASE_URL + p['image']

            genre = Genre.objects.get(pk=request.GET['genre'])

            queryset = Category.objects.all()
            categories = []
            for category in queryset:
                first_books = BookSerializer(Book.objects.filter(category=category, genre=genre)[:10], many=True).data
                for b in first_books:
                    if b['image'] is not None:
                        b['image'] = BASE_URL + b['image']
                categories.append({
                    'id': category.pk,
                    'name': category.name,
                    'first_books': first_books,
                })

            data = {
                'promo': promo,
                'categories': categories,
            }
            return Response({'data': data}, status=status.HTTP_200_OK)
        # except Exception:
        #     return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UnlockChapterView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            chapter = Chapter.objects.get(pk=request.GET['chapter'])
            user = User.objects.get(pk=request.GET['user'])
            if chapter not in user.unlocked_chapters.all():
                if user.balance >= chapter.cost:
                    user.unlocked_chapters.add(chapter)
                    user.balance = user.balance - chapter.cost
                    user.save()
                else:
                    return Response({'status': 'Insufficient funds'}, status=status.HTTP_200_OK)
                return Response({'status': 'OK'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'Chapter already unlocked'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UnlockAllChaptersView(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            book = Book.objects.get(pk=request.GET['book'])
            user = User.objects.get(pk=request.GET['user'])
            for chapter in Chapter.objects.filter(book=book):
                if chapter not in user.unlocked_chapters.all():
                    if user.balance >= chapter.cost:
                        user.unlocked_chapters.add(chapter)
                        user.balance = user.balance - chapter.cost
                        user.save()
                    else:
                        return Response({'status': 'Insufficient funds'}, status=status.HTTP_200_OK)
            return Response({'status': 'OK'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class GetBookFile(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            book = Book.objects.get(pk=request.GET['book'])
            try:
                file = BASE_URL+book.file.url
            except Exception:
                return Response({'status': 'File not found'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'file': file}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'status': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)