from django.conf.urls import patterns, url

urlpatterns = patterns('goovewolf.views',
    url(r'^$', 'index', name='home'),
    url(r'^collection/(?P<username>\w+)/$', 'collection', name='collection'),
    url(r'^login/', 'login', name='login'),
    url(r'^logout/', 'logout', name='logout'),
    url(r'^upload/', 'music_upload', name='music_upload')
)