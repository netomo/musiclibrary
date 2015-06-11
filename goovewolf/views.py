# coding=utf-8
from __future__ import unicode_literals
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.cache import never_cache
from django.contrib.auth.views import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import UserProfile, Artist, Album, Song, PlayList, PlaylistItem


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