import requests
from bs4 import BeautifulSoup

def get_person_info(name):
    # 将人物姓名转换为维基百科页面的 URL 格式
    url_name = name.replace(' ', '_')
    url = f'https://en.wikipedia.org/wiki/{url_name}'

    # 设置请求头，模拟浏览器访问
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # 发送 GET 请求获取页面内容
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None, None

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.content, 'html.parser')

    # 提取简介信息
    # 通常，简介位于页面的第一个段落中
    summary_paragraph = soup.find('p')
    summary = summary_paragraph.get_text(strip=True) if summary_paragraph else '无简介信息可用'

    # 提取头像 URL
    # 头像通常位于 infobox 中的第一个图像标签内
    infobox = soup.find('table', {'class': 'infobox'})
    image_url = None
    if infobox:
        image = infobox.find('img')
        if image and image.has_attr('src'):
            image_url = 'https:' + image['src']
    if not image_url:
        image_url = '无头像可用'

    # 提取头衔信息
    # 头衔通常在 infobox 中的 "Title" 行
    titles = []
    if infobox:
        title_row = infobox.find('th', string='Title')
        if title_row:
            title_data = title_row.find_next_sibling('td')
            if title_data:
                # 如果头衔是列表形式
                if title_data.find('ul'):
                    titles = [li.get_text(strip=True) for li in title_data.find_all('li')]
                else:
                    titles = [title_data.get_text(strip=True)]
    if not titles:
        titles = ['无头衔信息可用']

    return summary, image_url, titles

# 示例调用
name = 'Elon Musk'
summary, image_url, titles = get_person_info(name)
print(f'简介：{summary}')
print(f'头像 URL：{image_url}')
print(f'头衔：{titles}')
