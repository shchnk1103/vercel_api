from django.http import HttpResponse
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from pokemon_sleep.Serializers import PokemonSerializer, PokemonCharactorSerializer, PokemonSecondarySkillSerializer
from pokemon_sleep.Utils.pandas import parse_secondary_skill, parse_excel, parse_character
from pokemon_sleep.Utils.spiders import start_spider
from pokemon_sleep.models import pokemon_collection, pokemon_character_collection, pokemon_secondary_skill_collection


class PokemonSleepViewSet(viewsets.ViewSet):
    pagination_class = PageNumberPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def list(self, request):
        paginator = self.pagination_class()

        page_size = paginator.page_size
        page_number = request.query_params.get('page', 1)  # ?page=1
        skip = (int(page_number) - 1) * page_size

        # 获取过滤参数
        name_filter = request.query_params.get('name')

        # 构建查询条件
        query = {}
        if name_filter:
            query['name'] = {'$regex': name_filter,
                             '$options': 'i'}  # i 代表忽略大小写

        pokemons = pokemon_collection.find(query).skip(skip).limit(page_size)

        serializer = PokemonSerializer(pokemons, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def update_pokemon(self, request):
        pokemon_list = start_spider()
        for pokemon in pokemon_list:
            pokemon_id = pokemon['id']

            existing_pokemon = pokemon_collection.find_one({'id': pokemon_id})
            if existing_pokemon:
                pokemon_collection.update_one(
                    {'id': pokemon_id}, {'$set': pokemon})
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
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def list(self, request):
        # 获取过滤参数
        name_filter = request.query_params.get('title')

        # 构建查询条件
        query = {}
        if name_filter:
            query['title'] = {'$regex': name_filter,
                              '$options': 'i'}  # i 代表忽略大小写

        chacators = list(pokemon_character_collection.find(query))
        serializer = PokemonCharactorSerializer(chacators, many=True)

        return Response(serializer.data)


class PokemonSecondarySkillViewSet(viewsets.ViewSet):
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    def list(self, request):
        # 获取过滤参数
        name_filter = request.query_params.get('secondary_skill_name')

        # 构建查询条件
        query = {}
        if name_filter:
            query['secondary_skill_name'] = {
                '$regex': name_filter, '$options': 'i'}  # i 代表忽略大小写

        secondary_skills = list(pokemon_secondary_skill_collection.find(query))
        serializer = PokemonSecondarySkillSerializer(
            secondary_skills, many=True)

        return Response(serializer.data)


# class PokemonImageUploadViewSet(viewsets.ViewSet):
#     def create(self, request, *args, **kwargs):
#         try:
#             uploaded_image = request.FILES.get('image')
#             if uploaded_image:
#                 # Save the uploaded image to a temporary file
#                 with tempfile.TemporaryDirectory() as temp_dir:
#                     temp_file_path = os.path.join(temp_dir, 'temp_image.jpg')
#                     try:
#                         with open(temp_file_path, 'wb') as temp_file:
#                             temp_file.write(uploaded_image.read())
#                     except Exception as e:
#                         logging.error(f"Failed to write image to temporary file. Error: {str(e)}")

#                     if os.path.exists(temp_file_path):
#                         logging.info(f"Temporary file exists. Path: {temp_file_path}")
#                     else:
#                         logging.info("Temporary file does not exist.")

#                     # Perform processing on the temporary image file
#                     cn_ocr = CnOcr()
#                     img = cn_ocr.ocr(temp_file_path)

#                     pokemon_names = [pokemon['name'] for pokemon in list(pokemon_collection.find())]
#                     pokemon_characters = [pokemon['title'] for pokemon in list(pokemon_character_collection.find())]
#                     pokemon_secondary_skills = [pokemon['secondary_skill_name'] for pokemon in
#                                                 list(pokemon_secondary_skill_collection.find())]
#                     closest_match_name = ''
#                     closest_match_character = ''
#                     closest_match_secondary_skills = []
#                     name_matched = False
#                     character_matched = False
#                     secondary_skill_matched = False
#                     for line in img:
#                         if not name_matched:
#                             closest_match_name = get_cloest(line['text'], pokemon_names)
#                             if closest_match_name:
#                                 name_matched = True

#                         if not character_matched:
#                             if len(line['text']) <= 4:
#                                 closest_match_character = get_cloest(line['text'], pokemon_characters)
#                                 if closest_match_character:
#                                     character_matched = True

#                         if not secondary_skill_matched:
#                             closest_match_secondary_skill = get_cloest(line['text'], pokemon_secondary_skills,
#                                                                        threshold=98)
#                             if closest_match_secondary_skill:
#                                 closest_match_secondary_skills.append(closest_match_secondary_skill)
#                                 if len(closest_match_secondary_skills) == 5:
#                                     secondary_skill_matched = True

#                         if name_matched and character_matched and secondary_skill_matched:
#                             break

#                     return Response({
#                         'message': 'Image uploaded and processed successfully.',
#                         'pokemon_name': closest_match_name,
#                         'pokemon_character': closest_match_character,
#                         'pokemon_secondary_skills': closest_match_secondary_skills
#                     },
#                         status=status.HTTP_201_CREATED)
#             else:
#                 return Response({'error': 'No image provided.'}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def get_cloest(recognized_text, list_old, threshold=95):
#     highest_similarity = 0
#     closest_match = None

#     for need_to_recongnized_item in list_old:
#         similarity = fuzz.partial_ratio(need_to_recongnized_item, recognized_text)
#         if similarity > highest_similarity and similarity >= 60:
#             highest_similarity = similarity
#             closest_match = need_to_recongnized_item

#             # 剪枝策略：如果相似度达到一定阈值，认为找到了最佳匹配
#             if similarity >= threshold:
#                 break

#     return closest_match
