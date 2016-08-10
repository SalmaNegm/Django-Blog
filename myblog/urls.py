from django.conf.urls import url

from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^articale/(?P<pk>[0-9]+)/show',views.PostView.as_view(),name='single_post'),
    url(r'^login/$',views.log_in,name='login'), #login page
    url(r'^signin/$',views.signin,name='signin'),
    url(r'^logout/',views.log_out,name='logout'),
    url(r'^articale/create',views.create_post,name='create_post'),
    url(r'^articale/list',views.show_posts,name='show_posts'),
    url(r'^articale/(?P<pk>[0-9]+)/delete',views.delete_post,name='delete_post'),
    url(r'^articale/(?P<pk>[0-9]+)/update',views.update_post,name='update_post'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)