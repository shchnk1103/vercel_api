from django.db import models

from mongo import client

db = client['MyWebsite']

pokemon_collection = db['Pokemon']
pokemon_character_collection = db['PokemonCharacter']
pokemon_secondary_skill_collection = db['PokemonSecondarySkill']


class Pokemon(models.Model):
    # 全国编号
    id = models.IntegerField(primary_key=True)
    # 宝可梦名字
    name = models.CharField(max_length=200)
    # 图片
    image = models.CharField(max_length=200)
    # 睡眠类型
    sleep_type = models.CharField(max_length=200)
    # 专长
    expertise = models.CharField(max_length=200)
    # 主技能
    main_skill = models.CharField(max_length=200)
    # 主技能效果（Lv.1）
    main_skill_effect = models.CharField(max_length=200)
    # 树果
    tree_fruit = models.CharField(max_length=200)
    # 食材（Lv.1）
    ingredients = models.CharField(max_length=200)
    # 帮忙间隔
    help_interval = models.IntegerField()
    # 持有上限
    holding_cap = models.CharField(max_length=200)
    # 友情点数
    friendship_points = models.IntegerField()
    # 帮忙速度
    help_speed = models.FloatField()
    # 帮忙速度分数
    help_speed_score = models.FloatField()
    # 额外技能分数
    extra_skill_score = models.FloatField()
    # 面板总分
    panel_total_score = models.FloatField()
    # 归一化
    normalized_score = models.FloatField()
    # 进化潜力
    evolution_potential = models.FloatField()
    # 总面板 + 潜力
    total_score = models.FloatField()

    def __str__(self):
        return self.name
