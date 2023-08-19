import pandas as pd

from pokemon_sleep.models import pokemon_collection, pokemon_character_collection, pokemon_secondary_skill_collection

excel_file = 'pokemon_sleep/Utils/pokemon.xlsx'

field_mapping = {
    "全国编号": "id",
    "帮忙速度": "help_speed",
    "帮忙速度分": "help_speed_score",
    "额外技能分": "extra_skill_score",
    "面板总分": "panel_total_score",
    "归一化": "normalized_score",
    "进化潜力": "evolution_potential",
    "总面板+潜力": "total_score"
}

charactor_fix = {
    "EXP": "EXP获得量",
    "食材发现": "食材发现率",
    "活力回复": "活力回复量",
    "主技能": "主技能发动概率"
}

secondary_skill_fix = {
    "树果S": "树果数量S",
    "食材几率S": "食材几率提升S",
    "食材几率M": "食材几率提升M",
    "持有上限S": "持有上限提升S",
    "持有上限M": "持有上限提升M",
    "持有上限L": "持有上限提升L",
    "技能等级S": "技能等级提升S",
    "技能等级M": "技能等级提升M",
    "技能几率S": "技能几率提升S",
    "技能几率M": "技能几率提升M",
    "活力回复": "活力回复奖励",
    "睡眠exp": "睡眠EXP奖励",
    "研究exp": "研究EXP奖励",
}


# 补充Pokemon的分数信息
def parse_excel():
    df = pd.read_excel(excel_file, sheet_name='PM表', header=0)
    data_list = []

    for _, row in df.iterrows():
        # 将每一行的数据存储为一个字典，并添加到 data_list 中
        row_data = row.to_dict()
        data_list.append(row_data)

    for row in data_list:
        record_id = row['全国编号']

        update = {"$set": {field_mapping[field]: row[field] for field in field_mapping}}

        # TODO: 先检查数据库中是否与要更新的内容有差别，如果没有差别则不更新
        result = pokemon_collection.update_one({"id": record_id}, update, upsert=True)

        if result.modified_count > 0:
            print(f"Record with ID {record_id} updated successfully.")
        else:
            print(f"No record with ID {record_id} found.")


def parse_character():
    df = pd.read_excel(excel_file, sheet_name='性格', header=0)
    data_list = []

    for _, row in df.iterrows():
        title = row[0]
        plus = row[1]
        minus = row[2]

        plus = charactor_fix.get(plus, plus)
        minus = charactor_fix.get(minus, minus)

        formatted_data = {
            "title": title,
            "plus": plus,
            "minus": minus
        }
        data_list.append(formatted_data)

    pokemon_character_collection.insert_many(data_list)


def parse_secondary_skill():
    df = pd.read_excel(excel_file, sheet_name='副技能', header=None)

    for _, row in df.iterrows():
        secondary_skill_name = row.iloc[0]
        self_consistent = row.iloc[1]
        color = row.iloc[3]

        secondary_skill_name = secondary_skill_fix.get(secondary_skill_name, secondary_skill_name)

        if pd.isna(secondary_skill_name) or pd.isna(self_consistent) or pd.isna(color):
            continue

        formatted_data = {
            "secondary_skill_name": secondary_skill_name,
            "self_consistent": self_consistent,
            "color": color
        }

        existing_record = pokemon_secondary_skill_collection.find_one({"secondary_skill_name": secondary_skill_name})

        if existing_record:
            # Update existing record
            result = pokemon_secondary_skill_collection.update_one(
                {"secondary_skill_name": secondary_skill_name},
                {"$set": formatted_data}
            )
            if result.modified_count > 0:
                print(f"Record updated for {secondary_skill_name}.")
        else:
            # Insert new record
            result = pokemon_secondary_skill_collection.insert_one(formatted_data)
            if result.inserted_id:
                print(f"Record with ID {result.inserted_id} inserted successfully.")
