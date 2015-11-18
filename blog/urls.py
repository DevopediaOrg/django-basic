from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^post/(?P<pk>[0-9]+)/edit/?$', views.UpdateView.as_view(), name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/?$', views.DetailView.as_view(), name='post_detail'),
    url(r'^post/new/?$', views.CreateView.as_view(), name='post_new'),
    url(r'^post/(?P<pk>[0-9]+)/delete/?$', views.DeleteView.as_view(), name='post_delete'),

    url(r'^about$', views.AboutView.as_view(), name='about'),

    url(r'^authors/?$', views.AuthorListView.as_view(), name='author_list'),

    url(r'^topics/?$', views.ListView.as_view(), name='all_topic_list'),
    url(r'^topics/(?P<topic>[\w-]+)/?$', views.ListView.as_view(), name='topic_list'),

    url(r'^tags/?$', RedirectView.as_view(url='/topics', permanent=False)),
    url(r'^tags/(?P<tag>[\w-]+)/?$', views.ListView.as_view(), name='tag_list'),

    url(r'^states/?$', RedirectView.as_view(url='/topics', permanent=False)),
    url(r'^states/(?P<state>[\w-]+)/?$', views.ListView.as_view(), name='state_list'),

    url(r'^search$', views.SearchResultsView.as_view(), name='search_results'),
]
