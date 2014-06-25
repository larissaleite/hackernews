from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hackernews.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^$', include('stories.urls')), this way, itlooks for an empty string in the url
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('stories.urls')),
    url(r'^login/$', 'django.contrib.auth.views.login', { 'template_name' : 'auth/login.html' }),
    url(r'^logout/$', 'django.contrib.auth.views.logout', { 'next_page' : '/' }),
)
