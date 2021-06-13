from django.urls import path, include
from django.conf.urls import url
from rest_framework.generics import CreateAPIView
from .views import *
from rest_auth.views import PasswordResetConfirmView

api_urls = [
    path('user/data/<int:pk>/', GetUserDataView.as_view(), name='get_users_data'),
    path('user/data/update/<int:pk>/', UpdateUserDataView.as_view(), name='update_users_data'),
    path('user/settings/get/<int:pk>/', GetUsersReadingSettingsView.as_view(), name='get_user_settings'),
    path('user/settings/update/<int:pk>/', UpdateUsersReadingSettingsView.as_view(), name='get_user_settings'),
    path('user/balance/get/<int:pk>/', GetBalanceView.as_view(), name='get_balance'),
    path('book/detailed/<int:pk>/', GetDetailedBookView.as_view(), name='get_detailed_book'),
    path('book/review/create/', CreateReviewView.as_view(), name='create_review'),
    path('book/favourites/get/', GetFavouriteBooksView.as_view(), name='get_favourites'),
    path('book/favourites/add/', AddFavouriteBooksView.as_view(), name='add_favourites'),
    path('book/promo/get/', GetPromoView.as_view(), name='get_promo'),
    path('book/genres/get/', GetGenresView.as_view(), name='get_genres'),
    path('book/categories/get/', GetCategoryView.as_view(), name='get_categories'),
    path('book/get/', GetBooksView.as_view(), name='get_books'),
    path('book/main_page/get/', GetMainPageDataView.as_view(), name='get_main_page'),
    path('book/chapters_list/get/', GetChaptersListView.as_view(), name='get_chapters_list'),
    path('book/chapter/get/', GetChapterView.as_view(), name='get_chapter'),
    path('book/chapter/unlock/', UnlockChapterView.as_view(), name='unlock_chapter'),
    path('book/chapter/unlock/all/', UnlockAllChaptersView.as_view(), name='unlock_all_chapters'),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    path('password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]