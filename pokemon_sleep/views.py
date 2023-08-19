from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from pokemon_sleep.Serializers import PokemonSerializer, PokemonCharactorSerializer, PokemonSecondarySkillSerializer
from pokemon_sleep.Utils.pandas import parse_secondary_skill
from pokemon_sleep.Utils.spiders import start_spider
from pokemon_sleep.models import pokemon_collection, pokemon_character_collection, pokemon_secondary_skill_collection


class PokemonSleepViewSet(viewsets.ViewSet):
    pagination_class = PageNumberPagination

    def list(self, request):
        paginator = self.pagination_class()

        page_size = paginator.page_size
        page_number = request.query_params.get('page', 1)  # ?page=1
        skip = (int(page_number) - 1) * page_size

        pokemons = pokemon_collection.find().skip(skip).limit(page_size)

        serializer = PokemonSerializer(pokemons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def update_pokemon(self, request):
        pokemon_list = start_spider()
        for pokemon in pokemon_list:
            pokemon_id = pokemon['id']

            existing_pokemon = pokemon_collection.find_one({'id': pokemon_id})
            if existing_pokemon:
                pokemon_collection.update_one({'id': pokemon_id}, {'$set': pokemon})
            else:
                pokemon_collection.insert_one(pokemon)
        return HttpResponse("Success!")

    @action(detail=False, methods=['get'])
    def get_info_from_excel(self, request):
        parse_excel()
        parse_character()
        parse_secondary_skill()
        return HttpResponse("Success!")


class PokemonChacatorViewSet(viewsets.ViewSet):
    def list(self, request):
        chacators = list(pokemon_character_collection.find())
        serializer = PokemonCharactorSerializer(chacators, many=True)

        return Response(serializer.data)


class PokemonSecondarySkillViewSet(viewsets.ViewSet):
    def list(self, request):
        secondary_skills = list(pokemon_secondary_skill_collection.find())
        serializer = PokemonSecondarySkillSerializer(secondary_skills, many=True)

        return Response(serializer.data)
