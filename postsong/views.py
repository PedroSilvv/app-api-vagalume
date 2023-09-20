from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from . import models
from django.http import HttpResponse, HttpResponseRedirect
import requests
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import User

"""
@login_required(login_url='/')
def postsong(request):

    if request.method == "GET":
        return render(request, "postsong.html", context={
            'artists': models.Artist.objects.all(),
        })
    else:

        title = request.POST.get('title')
        artist = request.POST.get('artist')
        key = request.POST.get('key')
        tuning = request.POST.get('tuning')
        author = request.user

        artist_api_form = artist.lower().replace(" ", "-")

        try:
            response = requests.get(f"https://www.vagalume.com.br/{artist_api_form}/index.js")
            artist_data = response.json()
            response_artist = artist_data["artist"]["desc"]

            try:
                get_artist = models.Artist.objects.get(name=response_artist)
            except ObjectDoesNotExist:
                get_artist = models.Artist.objects.create(name=response_artist)
                get_artist.save()

        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro ao buscar artista.")
            return redirect("postsong")

        try:
            request_song = requests.get("https://api.vagalume.com.br/search.php"
                                   + "?art=" + artist
                                   + "&mus=" + title
                                   + "&apikey={key}")

            song_data = request_song.json()
            response_song = (song_data["mus"][0]['name'])

            try:
                get_song = models.Song.objects.create(author=author, title=response_song, artist=get_artist, key=key, tuning=tuning)
                get_song.save()
            except:
                messages.error(request, f"Não é possivel criar cifra dessa música!")
                return redirect("postsong")

        except:
            messages.error(request, f"Erro ao buscar música.")
            return redirect("postsong")


        return redirect('postchord', song_id=get_song.id)

@login_required(login_url='/')
def postchord(request, song_id):

    song = models.Song.objects.get(id=song_id)

    if song.chords is not None:
        raise PermissionDenied("Acesso negado: Cifra já foi postada para esta música.")


    try:
        requisicao = requests.get("https://api.vagalume.com.br/search.php"
                                  + "?art=" + song.artist.name
                                  + "&mus=" + song.title
                                  + "&apikey={key}")


        address_data = requisicao.json()

        lyric = address_data["mus"][0]["text"]
    except:
        return HttpResponse("Musica ou Artista nao encontrado")

    return render(request, 'postchord.html', context={
        'song': song,
        'lyric': lyric,
    })

@login_required(login_url='/')
def finally_post_chord(request, song_id):

    song = models.Song.objects.get(id=song_id)

    chords = request.GET.get('chords')
    description = request.GET.get('description')

    print(chords)
    print(description)

    models.Song.objects.filter(id=song_id).update(chords=chords, description=description)


    #except:
    #   return HttpResponse("ERRO NAO ESPERADO")

    return redirect('homepage')

"""



@login_required(login_url='/')
def postsong(request):

    if request.method == "GET":
        return render(request, "postsong.html", context={
            'artists': models.Artist.objects.all(),
        })
    else:

        title = request.POST.get('title')
        artist = request.POST.get('artist')
        key = request.POST.get('key')
        tuning = request.POST.get('tuning')

        artist_api_form = artist.lower().replace(" ", "-")

        try:
            response = requests.get(f"https://www.vagalume.com.br/{artist_api_form}/index.js")
            artist_data = response.json()
            response_artist = artist_data["artist"]["desc"]

 
        except requests.exceptions.RequestException as e:
            messages.error(request, f"Erro ao buscar artista.")
            return redirect("postsong")

        try:
            request_song = requests.get("https://api.vagalume.com.br/search.php"
                                   + "?art=" + artist
                                   + "&mus=" + title
                                   + "&apikey={key}")

            song_data = request_song.json()
            response_song = (song_data["mus"][0]['name'])
            


        except:
            messages.error(request, f"Erro ao buscar música.")
            return redirect("postsong")

        request.session['title'] = response_song
        request.session['artist'] = response_artist
        request.session['key'] = key
        request.session['tuning'] = tuning
        request.session['user_id'] = request.user.id
        request.session['liberar_postchord'] = True


        return redirect('postchord')



@login_required(login_url='/')
def postchord(request):

    if request.session['liberar_postchord'] != True:
        raise PermissionDenied("Need choose a song to access this endpoint (Access /post/postsong first) ")

 
    try:
        requisicao = requests.get("https://api.vagalume.com.br/search.php"
                                  + "?art=" + request.session['artist']
                                  + "&mus=" + request.session['title']
                                  + "&apikey={key}")


        address_data = requisicao.json()

        lyric = address_data["mus"][0]["text"]
        request.session['lyric'] = lyric
    except:
        return HttpResponse("Musica ou Artista nao encontrado")

    return render(request, 'postchord.html', context={
        'song': {
            'title' : request.session['title'],
            'artist' : request.session['artist']
        },
        'lyric': lyric,
    })

@login_required(login_url='/')
def finally_post_chord(request):

    user_id = request.session.get('user_id')
    author = User.objects.get(pk=user_id)

    if request.method == 'POST':

        chords = request.POST.get('chords')
        description = request.POST.get('description')

        request.session['chords'] = chords
        request.session['description'] = description

        print(chords)
        print(description)

        try:
            saving_artist = models.Artist.objects.get(name=request.session['artist'])
        except ObjectDoesNotExist:
            saving_artist = models.Artist.objects.create(name=request.session['artist'])
            saving_artist.save()
        
        saving_song = models.Song.objects.create(author = author, title = request.session['title'], artist = saving_artist,
                                                    key = request.session['key'], tuning = request.session['tuning'], chords = request.session['chords'],
                                                    description = request.session['description'], lyric= request.session['lyric'])
        saving_song.save()

        variables_to_remove = ['title', 'key', 'artist', 'tuning', 'chords', 'description', 'lyric']

        request.session['liberar_postchord'] = False

        for x in variables_to_remove:
            if x in request.session:
                del request.session[x]


        #except:
        #   return HttpResponse("ERRO NAO ESPERADO")

        return redirect('homepage')

    
