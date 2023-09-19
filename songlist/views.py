from django.shortcuts import render, redirect
from postsong.models import Song
from django.contrib import messages
from django.http import HttpResponseNotFound

def songlist(request):
    return render(request, "songlist.html", context={
        "songs" : Song.objects.all()
    })

def songdetail(request, song_id):

    try:
        song = Song.objects.get(id=song_id)
        return render(request, "songdetail.html", context={
            "song" : song
        })
    except:
        messages.error(request, "Cifra não encontrada")
        return redirect('songlist')



def delete_song(request, song_id):


    try:
        song = Song.objects.get(id=song_id)
    except:
        messages.error(request, "Não é possivel deletar essa Cifra!!")
        return redirect('songlist')

    actual_user = request.user

    if song.author == actual_user or actual_user.is_staff:
        Song.objects.get(id=song_id).delete()

    else:
        messages.error(request, "Você não ter permissão para arquivas essa cifra!")

    return redirect('songlist')



def update_song(request, song_id):

    song = Song.objects.get(id=song_id)

    if request.method == 'GET':
        return render(request, 'updatesong.html', context={
            'song' : song
        })

    else:

        song = Song.objects.get(id=song_id)

        new_chords = request.POST.get('chords')
        new_key = request.POST.get('key')
        new_tuning = request.POST.get('tuning')
        new_description = request.POST.get('description')

        Song.objects.filter(id=song_id).update(chords=new_chords, key=new_key, tuning=new_tuning, description=new_description)

        return redirect('songdetail', song_id=song.id)




