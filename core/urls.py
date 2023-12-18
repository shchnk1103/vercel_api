"""core URL Configuration

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
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from file_upload.views import FileUploadViewSet
from pokemon_sleep.views import PokemonSleepViewSet, PokemonChacatorViewSet, PokemonSecondarySkillViewSet

router = DefaultRouter()
router.register(r'files-upload', FileUploadViewSet, basename='file-upload')
router.register(r'pokemons', PokemonSleepViewSet, basename='pokemon-sleep')
router.register(r'pokemon-chacators', PokemonChacatorViewSet,
                basename='pokemon-chacator')
router.register(r'pokemon-secondary-skills',
                PokemonSecondarySkillViewSet, basename='pokemon-secondary-skill')
# router.register(r'pokemon-image-uploads',
#                 PokemonImageUploadViewSet, basename='pokemon-image-upload')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
]
