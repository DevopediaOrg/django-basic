from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.ListView.as_view(), name='post_list'),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.UpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='post_detail'),
    url(r'^post/new/$', views.CreateView.as_view(), name='post_new'),
    url(r'^authors$', views.ListView.as_view(), name='post_list'),
    url(r'^topics/?$', RedirectView.as_view(url='/topics/general', permanent=True)),
    url(r'^topics/(?P<category>[\w-]+)/?$', views.ListView.as_view(), name='post_list'),
]
