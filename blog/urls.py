from django.conf.urls import include, url
from django.views import generic
from .models import Post
from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.UpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreateView.as_view(), name='post_new'),
    url(r'^authors$', views.ListView.as_view(), name='post_list'),
    url(r'^about$', views.ListView.as_view(), name='post_list'),
    url(r'^topics', views.ListView.as_view(), name='post_list'),
]
