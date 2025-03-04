from django.urls import path
from . import views

app_name = 'bibliothecaire'
urlpatterns = [
    path('', views.index, name='index'),
    path('borrowers/', views.borrower_list, name='borrower_list'),
    path('borrowers/new/', views.borrower_create, name='borrower_create'),
    path('borrowers/<int:pk>/edit/', views.borrower_update, name='borrower_update'),
    path('media/', views.media_list, name='media_list'),
    path('media/new/', views.media_create, name='media_create'),
    path('borrow/<int:media_id>/', views.borrow_media, name='borrow_media'),
    path('return/<int:media_id>/', views.return_media, name='return_media'),
    path('media/book/<int:pk>/edit/', views.book_update, name='book_update'),
    path('media/dvd/<int:pk>/edit/', views.dvd_update, name='dvd_update'),
    path('media/cd/<int:pk>/edit/', views.cd_update, name='cd_update'),
    path('media/boardgame/<int:pk>/edit/', views.boardgame_update, name='boardgame_update'),
    path('media/book/<int:pk>/delete/', views.book_delete, name='book_delete'),
    path('media/dvd/<int:pk>/delete/', views.dvd_delete, name='dvd_delete'),
    path('media/cd/<int:pk>/delete/', views.cd_delete, name='cd_delete'),
    path('media/boardgame/<int:pk>/delete/', views.boardgame_delete, name='boardgame_delete'),
    path('borrowers/<int:pk>/delete/', views.borrower_delete, name='borrower_delete'),
]