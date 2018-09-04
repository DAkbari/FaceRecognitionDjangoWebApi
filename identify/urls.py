from django.conf.urls import url
from . import views

app_name = 'identify'

urlpatterns = [
    # /identify/
    url(r'^$', views.IndexView.as_view(), name='index'),

    # /identify/new
    url(r'^new/$', views.PersonCreate.as_view(), name='new'),

    # /identify/71/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),

    # /music/album/2/
    url(r'album/(?P<pk>[0-9]+)/$', views.PersonUpdate.as_view(), name="album-update"),

    # /music/album/2/delete/
    url(r'album/(?P<pk>[0-9]+)/delete/$', views.PersonDelete.as_view(), name="person-delete")

    #

]