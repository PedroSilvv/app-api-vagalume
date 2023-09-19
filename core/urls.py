from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


import home.views
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('post/', include('postsong.urls')),
    path('register/', include('register.urls')),
    path('login/', include('login.urls')),
    path('songlist/', include('songlist.urls')),
    path('songsfilter/', home.views.filter_song, name='songsfilter'),
]  + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


