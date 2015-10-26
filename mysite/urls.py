from django.conf.urls import include, patterns, url
from django.conf import settings
from django.contrib import admin
from django.views import generic

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^about$', generic.TemplateView.as_view(template_name='about.html'), name="about"),
    
    url(r'', include('blog.urls', namespace='blog')),
]

if settings.DEBUG:
  urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})) 
