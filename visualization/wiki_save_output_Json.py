import os
import sys
import django
import json
import requests
from bs4 import BeautifulSoup

# 1. 配置 Django 环境
# 添加 Django 项目目录到 sys.path
# 请将 'E:/code/spark_main/djangoProject' 替换为您的 Django 项目根目录路径
sys.path.append('E:/code/spark_main/djangoProject')

# 设置 DJANGO_SETTINGS_MODULE 环境变量
# 请将 'djangoProject.settings' 替换为您的 settings 模块路径
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')

# 初始化 Django
django.setup()

# 2. 导入 Django 模型
from visualization.models import RichPerson  # 请根据实际情况调整导入路径

# 3. 从数据库中获取所有名字
# 更正字段名称，从 'Name' 改为 'name'
names = RichPerson.objects.values_list('name', flat=True)

def get_person_info(name):
    # 定义维基百科 API 端点
    api_url = 'https://en.wikipedia.org/w/api.php'

    # 设置 API 请求参数
    params = {
        'action': 'query',
        'titles': name,
        'prop': 'pageimages|extracts',
        'format': 'json',
        'exintro': True,
        'explaintext': True,
        'piprop': 'original'
    }

    # 设置代理（如果需要）
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    try:
        # 发送 API 请求
        response = requests.get(api_url, params=params, proxies=proxies, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求维基百科 API 时出错 ({name})：{e}")
        return '无简介信息可用', '无头像可用', ['无头衔信息可用']

    # 初始化返回值
    extract = '无简介信息可用'
    image_url = '无头像可用'
    titles = ['无头衔信息可用']

    # 解析 API 返回的数据
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        if page_id == "-1":
            # 页面不存在
            print(f"维基百科中未找到 {name} 的页面。")
            continue
        # 获取简介信息
        extract = page.get('extract', extract)

        # 获取头像 URL
        original = page.get('original', {})
        image_url = original.get('source', image_url)

        # 获取页面全文 URL
        full_url = f"https://en.wikipedia.org/?curid={page_id}"

        try:
            # 发送请求获取页面全文
            page_response = requests.get(full_url, proxies=proxies, timeout=10)
            page_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"请求维基百科页面时出错 ({full_url})：{e}")
            continue

        # 使用 BeautifulSoup 解析页面内容
        soup = BeautifulSoup(page_response.content, 'html.parser')

        # 查找信息框（infobox）
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            # 查找头衔信息
            title_row = infobox.find('th', string=lambda x: x and 'Title' in x)
            if title_row:
                title_data = title_row.find_next_sibling('td')
                if title_data:
                    # 如果头衔是列表形式
                    if title_data.find('ul'):
                        titles = [li.get_text(strip=True) for li in title_data.find_all('li')]
                    else:
                        titles = [title_data.get_text(strip=True)]

    return extract, image_url, titles

def fetch_and_save_info():
    # 定义存储所有人物信息的字典
    people_info = {}

    # 遍历所有名字
    for name in names:
        print(f'正在获取 {name} 的信息...')
        extract, image_url, titles = get_person_info(name)
        # 保存信息
        people_info[name] = {
            'extract': extract,
            'image_url': image_url,
            'titles': titles
        }

    # 保存为 JSON 文件
    output_file = 'people_info.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(people_info, f, ensure_ascii=False, indent=4)
        print(f'所有信息已保存为 {output_file}')
    except IOError as e:
        print(f"保存 JSON 文件时出错：{e}")

if __name__ == '__main__':
    fetch_and_save_info()
