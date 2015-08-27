from django.conf.urls import patterns, include, url
from django.contrib import admin
import settings
from codetables import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'codetable.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name="index"),
    url(r'^compile/$', views.compile_code, name="compile"),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_view,name='logout'),
    url(r'^save_file/$', views.save_file,name='savefile'),
    url(r'^get_file/(?P<file_id>\w+)$', views.get_file,name='getfile'),    
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

)
