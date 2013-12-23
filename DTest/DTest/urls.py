from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DTest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$','DTest.views.front', name='landing'),
    url(r'^scrape', 'DTest.views.scrape', name='scrape'),
    url(r'^announce', 'DTest.views.announce', name='announce'), 
    url(r'^upload', 'DTest.views.upload'),
    url(r'^admin/', include(admin.site.urls)),
)
