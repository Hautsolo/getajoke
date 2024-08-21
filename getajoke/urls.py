"""jokes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from rest_framework import routers

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from getajokeapi.views import JokeViewSet,check_user, CommentViewSet, generate_joke,UserView,TagView

router = routers.DefaultRouter(trailing_slash=False)


router.register(r'jokes', JokeViewSet, 'jokes')
router.register(r'comments', CommentViewSet, 'comment')
router.register(r'users', UserView, 'user')
router.register(r'tags', TagView, 'tag')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/generate-joke/', generate_joke, name='generate_joke'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('checkuser', check_user),
]
