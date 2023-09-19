from django.urls import path
from . import views

urlpatterns = [
    #path("postsong/", views.postsong, name='postsong'),
    path("postsong/", views.postsong, name='postsong'),
    #path("postchord/<int:song_id>/", views.postchord, name='postchord'),
    path("postchord/", views.postchord, name='postchord'),
    #path("chord-posted/<int:song_id>/", views.finally_post_chord, name='song-posted')
    path("chord-posted/", views.finally_post_chord, name='song-posted')
]