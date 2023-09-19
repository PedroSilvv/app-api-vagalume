from django.shortcuts import render
from postsong.models import Song, Artist
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'home.html', context={
        "user": request.user,
    })

def filter_song(request):

    
    song = request.GET.get("song").strip()
    artist_name = request.GET.get("artist").strip()

    

    if artist_name:
        try:
            artist = Artist.objects.get(name__iexact=artist_name)
        except Artist.DoesNotExist:
            raise Http404("Artista não encontrado.")


        songs_filter = Song.objects.all()

    if len(song) > 0 and len(artist_name) > 0:
        songs_filter = Song.objects.filter(title__iexact=song, artist__exact=artist)

    if len(song) > 0 and len(artist_name) == 0:
        songs_filter = Song.objects.filter(title__iexact=song)

    if len(artist_name) > 0 and len(song) == 0:
        songs_filter = Song.objects.filter(artist__exact=artist)

    list_descriptions = []

    if not songs_filter:
        raise Http404("Versão não encontrada.")

    
    for x in songs_filter:
        resume_description = x.description[0:150] + "..."
        list_descriptions.append(resume_description)
    
    context = []

    for song, description in zip(songs_filter, list_descriptions):
        context.append({
            'song' : song,
            'description' : description}
        )



    return render(request, "songsfilter.html", context={
        'context' : context
    })