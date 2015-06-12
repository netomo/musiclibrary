# coding=utf-8
from __future__ import unicode_literals
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile, Artist, Album, Song, Playlist, PlaylistItem


@never_cache
def login(request):
    return auth_login(request, 'groovewolf/login.html')


@never_cache
def logout(request):
    return auth_logout(request, template_name='groovewolf/login.html')


@require_GET
def index(request):
    context = {
        'lastest_songs': Song.objects.order_by('-created')[0:100],
        'adds': PlaylistItem.objects.order_by('-added')[0:100]
    }
    return render(request, 'groovewolf/index.html')


@require_GET
def collection(request, username):
    return render(request, 'groovewolf/collection.html')


@login_required
def music_upload(request):
    if request.method == 'GET':
        return render(request, 'groovewolf/musicupload.html')

    if request.method == 'POST':
        file_types = ['audio/mpeg', 'audio/mp3', 'audio/m4a']
        music_file = request.FILES.values()[0]
        profile = UserProfile.objects.get(user=request.user)

        if music_file.content_type not in file_types:
            print(music_file.content_type)
            return JsonResponse({'success': False, 'reason': 'Allowed filetypes: mp3, m4a'})

        songdata = {
            'file': music_file,
            'name': request.POST['name'],
            'created_by': profile
        }

        if request.POST['artist']:
            songdata['artist'] = Artist.objects.get(id=int(request.POST['artist']))

        song = Song.objects.create(**songdata)
        profile.get_collection().add_item(song)

        return JsonResponse({'success': True, 'id': song.id, 'url': song.file.url})