#该文件的作用是检查文件中的国家名在echarts地图中是否存在
import pandas as pd
import re
import json
import requests

def read_csv_country_list(csv_file_path, country_column):
    """
    读取 CSV 文件并提取国家名称列表
    """
    df = pd.read_csv(csv_file_path)
    if country_column not in df.columns:
        raise ValueError(f"列 {country_column} 不存在于 CSV 文件中")
    return df[country_column].dropna().unique().tolist()

def download_world_js(url):
    """
    从 CDN 动态下载 world.js 文件
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"无法下载 world.js 文件，状态码: {response.status_code}")

def extract_countries_from_world_js(js_content):
    """
    从 world.js 文件内容中提取国家名称列表
    """
    # 使用正则表达式匹配国家名称
    pattern = r'"name":"(.*?)"'
    countries = re.findall(pattern, js_content)
    return set(countries)

def create_country_mapping(csv_countries, js_countries):
    """
    比较两个国家列表，创建映射表
    """
    missing_countries = [country for country in csv_countries if country not in js_countries]
    return missing_countries

def save_mapping_to_file(missing_countries, output_file):
    """
    将缺失的国家列表保存到文件中
    """
    mapping = {country: "" for country in missing_countries}  # 手动映射的占位
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # 输入文件路径
    csv_file_path = "top rich2024.csv"  # 替换为你的 CSV 文件路径
    output_mapping_file = "country_mapping.json"

    # world.js 的 CDN 地址
    world_js_url = "https://cdn.jsdelivr.net/npm/echarts/map/js/world.js"  # 替换为你的实际 CDN 地址

    # CSV 文件中的国家名称列名
    country_column = "Country / Region"  # 替换为你的国家列名

    # 读取 CSV 国家列表
    csv_countries = read_csv_country_list(csv_file_path, country_column)
    print(f"CSV 中的国家列表: {csv_countries}")

    # 下载 world.js 文件
    print(f"正在从 {world_js_url} 下载 world.js 文件...")
    world_js_content = download_world_js(world_js_url)

    # 从 world.js 提取国家列表
    js_countries = extract_countries_from_world_js(world_js_content)
    print(f"world.js 中的国家列表: {js_countries}")

    # 创建映射表
    missing_countries = create_country_mapping(csv_countries, js_countries)
    print(f"缺失的国家列表: {missing_countries}")

    # 保存到文件
    save_mapping_to_file(missing_countries, output_mapping_file)
    print(f"国家映射表已保存到 {output_mapping_file}")
