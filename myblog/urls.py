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
    url(r'^comment/add',views.create_comment,name='create_comment'),
    url(r'^comment/delete',views.delete_comment,name='delete_comment'),
    url(r'^comment/like',views.like_comment,name='like_comment'),
    url(r'^comment/unlike',views.unlike_comment,name='unlike_comment'),
    url(r'^tags/',views.get_tags,name='stored_tags'),
    url(r'^posts/(?P<tag_id>[0-9]+)/tag',views.similar_posts,name='similar_posts'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)