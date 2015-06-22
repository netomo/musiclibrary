# coding=utf-8
from __future__ import unicode_literals
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import User, UserProfile, Artist, Album, Song, Playlist, PlaylistItem, Feed
from .forms import SignUpForm


@never_cache
def login(request):
    return auth_login(request, 'groovewolf/login.html')


@never_cache
def logout(request):
    return auth_logout(request, template_name='groovewolf/login.html')


@never_cache
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['username'],
                data['email'],
                data['password'],
                first_name=data['first_name'],
                last_name=data['last_name']
            )
            UserProfile.objects.create(user=user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'groovewolf/signup.html', {'form': form})


@require_GET
def index(request):
    context = {
        'lastest_songs': Song.objects.order_by('-created')[0:10],
        'adds': PlaylistItem.objects.order_by('-added')[0:10],
        'feed': Feed.objects.all()[0:10]
    }
    return render(request, 'groovewolf/index.html', context)


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