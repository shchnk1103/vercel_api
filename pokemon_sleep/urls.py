from django.urls import path

from pokemon_sleep import views

urlpatterns = [
    path('pokemon/', views.PokemonSleep.as_view())
]
