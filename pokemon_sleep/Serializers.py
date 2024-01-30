from rest_framework import serializers


class PokemonSerializer(serializers.Serializer):
    id = serializers.CharField()
    img_url = serializers.CharField()
    name_eng = serializers.CharField()
    name = serializers.CharField()
    sleep_type = serializers.CharField()
    expertise = serializers.CharField()
    main_skill = serializers.CharField()
    main_skill_effect = serializers.CharField()
    tree_fruit = serializers.CharField()
    ingredients = serializers.CharField()
    help_interval = serializers.CharField()
    holding_cap = serializers.CharField()
    friendship_points = serializers.CharField()
    help_speed = serializers.FloatField()
    help_speed_score = serializers.FloatField()
    extra_skill_score = serializers.IntegerField()
    panel_total_score = serializers.FloatField()
    normalized_score = serializers.IntegerField()
    evolution_potential = serializers.IntegerField()
    total_score = serializers.IntegerField()

    class Meta:
        collection = 'Pokemon'


class PokemonCharacterSerializer(serializers.Serializer):
    _id = serializers.CharField()
    title = serializers.CharField()
    plus = serializers.CharField()
    minus = serializers.CharField()

    class Meta:
        collection = 'PokemonCharacter'


class PokemonSecondarySkillSerializer(serializers.Serializer):
    _id = serializers.CharField()
    secondary_skill_name = serializers.CharField()
    self_consistent = serializers.CharField()
    color = serializers.CharField()

    class Meta:
        collection = 'PokemonSecondarySkill'
