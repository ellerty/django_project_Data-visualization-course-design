import requests
from bs4 import BeautifulSoup

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

    # 发送 API 请求
    response = requests.get(api_url, params=params, proxies=proxies)
    data = response.json()

    # 初始化返回值
    extract = '无简介信息可用'
    image_url = '无头像可用'
    titles = ['无头衔信息可用']

    # 解析 API 返回的数据
    pages = data.get('query', {}).get('pages', {})
    for page_id, page in pages.items():
        # 获取简介信息
        extract = page.get('extract', extract)

        # 获取头像 URL
        original = page.get('original', {})
        image_url = original.get('source', image_url)

        # 获取页面全文 URL
        full_url = f"https://en.wikipedia.org/?curid={page_id}"

        # 发送请求获取页面全文
        page_response = requests.get(full_url, proxies=proxies)
        if page_response.status_code == 200:
            # 使用 BeautifulSoup 解析页面内容
            soup = BeautifulSoup(page_response.content, 'html.parser')

            # 查找信息框（infobox）
            infobox = soup.find('table', {'class': 'infobox'})
            if infobox:
                # 查找头衔信息
                title_row = infobox.find('th', string='Title')
                if title_row:
                    title_data = title_row.find_next_sibling('td')
                    if title_data:
                        # 如果头衔是列表形式
                        if title_data.find('ul'):
                            titles = [li.get_text(strip=True) for li in title_data.find_all('li')]
                        else:
                            titles = [title_data.get_text(strip=True)]

    return extract, image_url, titles

# 示例调用
name = 'Elon Musk'
extract, image_url, titles = get_person_info(name)
print(f'简介：{extract}')
print(f'头像 URL：{image_url}')
print(f'头衔：{titles}')
