from django.http import HttpResponse
from rest_framework.views import APIView


class PokemonSleep(APIView):
    def get(self, request):
        return HttpResponse('Hello World')
