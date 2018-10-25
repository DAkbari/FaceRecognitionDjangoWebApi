from django.conf.urls import url
from . import views


app_name = 'identify'

urlpatterns = [
    # /identify/
    url(r'^$', views.IndexView.as_view(), {'active_menu': 'List'}, name='index'),

    # /identify/new
    url(r'^new/$', views.PersonCreate.as_view(), name='new'),

    url('login/', views.user_login, name='login'),

    url('register', views.user_register, name='register'),

    url('logout/', views.user_logout, name='logout'),

    # /identify/capture
    url(r'^capture/$', views.capture, name='capture'),

    # /identify/capture_api
    url(r'^capture_api/$', views.capture_api.as_view(), name='capture_api'),

    # /identify/71/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),

    # /person/2/
    url(r'person/(?P<pk>[0-9]+)/$', views.PersonUpdate.as_view(), name="person-update"),

    # /identify/2/delete/
    url(r'identity/(?P<pk>[0-9]+)/delete/$', views.PersonDelete.as_view(), name="person-delete")
]