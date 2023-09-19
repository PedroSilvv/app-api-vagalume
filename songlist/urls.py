from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.songlist, name='songlist'),
    path('song/<int:song_id>', views.songdetail, name='songdetail'),
    path('song/delete/<int:song_id>', views.delete_song, name='delete_song'),
    path('song/update/<int:song_id>', views.update_song, name='update_song'),
]