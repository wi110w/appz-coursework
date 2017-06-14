from django.conf.urls import url
from . import views

app_name = 'netart'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^user/(?P<user_id>[0-9]+)/$', views.profile, name='profile'),
    url(r'^catalog/$', views.catalog, name='catalog'),
    url(r'^profile/(?P<user_id>[0-9]+)/edit/$', views.profile_edit, name='profile_edit'),
    url(r'^upload/$', views.upload_picture, name='upload'),
    url(r'^profile/(?P<user_id>[0-9]+)/change_avatar/$', views.upload_new_avatar, name='upload_new_avatar'),
    url(r'^messages/$', views.msg_box, name='msg_box'),
    url(r'^messages/new/$', views.send_msg, name='send_msg'),
    url(r'^news/add/$', views.add_news, name='add_news'),
    url(r'^news/(?P<new_id>[0-9]+)/$', views.new_detail, name='new_detail')
]