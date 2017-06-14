from django.conf.urls import url, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'pictures', views.PictureViewSet)
router.register(r'news', views.NewsViewSet)
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]