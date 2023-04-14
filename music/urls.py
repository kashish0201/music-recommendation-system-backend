from .views import *
from django.urls import path

urlpatterns = [
    path('genre/<str:music_genre>', getSongByGenre.as_view(),name= 'songs-genre'),
    path('search', getSongBySearch.as_view(),name= 'songs-search'),
    path('like', LikeSong.as_view(), name = 'like-song'),
    path('genres', getAllGenre.as_view(), name = 'all-genres')
]
