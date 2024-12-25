import requests

def get_person_info(name):
    # 定义维基百科 API 端点
    api_url = 'https://en.wikipedia.org/w/api.php'

    # 设置请求参数
    params = {
        'action': 'query',
        'titles': name,
        'prop': 'pageimages|extracts',
        'format': 'json',
        'exintro': True,
        'explaintext': True,
        'piprop': 'original'
    }

    # 设置代理
    proxies = {
        'http': 'http://127.0.0.1:7890',
        'https': 'http://127.0.0.1:7890'
    }

    # 发送请求
    response = requests.get(api_url, params=params, proxies=proxies)
    data = response.json()

    # 解析返回数据
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        # 获取简介信息
        extract = page.get('extract', '无简介信息可用')

        # 获取头像 URL
        original = page.get('original', {})
        image_url = original.get('source', '无头像可用')

        return extract, image_url

# 示例调用
name = 'Elon Musk'
extract, image_url = get_person_info(name)
print(f'简介：{extract}')
print(f'头像 URL：{image_url}')
