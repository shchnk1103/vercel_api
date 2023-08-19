import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def start_spider():
    # 创建 ChromeOptions 对象
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 以无界面模式运行

    # 创建 Chrome 浏览器实例
    driver = webdriver.Chrome(options=chrome_options)

    url = 'https://bbs.nga.cn/read.php?tid=37121346'

    # 打开网页
    driver.get(url)
    # 通过网页的跳转
    time.sleep(5)

    container01 = driver.find_element(By.ID, "postcontent0")
    tbody = container01.find_element(By.TAG_NAME, 'tbody')
    trs = tbody.find_elements(By.TAG_NAME, 'tr')

    # 定义最终返回的列表
    pokemon_list = []
    # 定义字段名称的列表
    fields = [
        'id', 'img_url', 'name_eng', 'name', 'sleep_type', 'expertise', 'main_skill',
        'main_skill_effect', 'tree_fruit', 'ingredients', 'help_interval',
        'holding_cap', 'friendship_points'
    ]

    # 找到每一行的数据
    for tr in trs:
        # 找出每一列的数据
        tds = tr.find_elements(By.TAG_NAME, 'td')

        pokemon = {}

        for index, td in enumerate(tds):
            text = td.text.replace('\n', '')

            # 根据索引将值添加到对应的字段
            field_name = fields[index]
            if index == 0:
                if not text.startswith('#'):
                    break
                pokemon[field_name] = text
            elif index in [1, 8, 9]:
                pokemon[field_name] = find_img(td)
            else:
                pokemon[field_name] = text

        # 如果不是#开头，则说明不是宝可梦数据，而是表头
        # if not pokemon['id'].startswith('#'):
        #     continue

        if pokemon:
            pokemon_list.append(pokemon)

    driver.quit()
    return pokemon_list


def find_img(td):
    try:
        img_element = td.find_element(By.TAG_NAME, 'img')
        img_src = img_element.get_attribute('data-srcorg')
        return img_src
    except Exception as e:
        print(f'no img found, error: {e}')
        return ''
