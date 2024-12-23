# visualization/views.py

import pandas as pd
import os
import json
from django.shortcuts import render
from collections import defaultdict
from django.conf import settings

def map_view(request):
    csv_file_path = os.path.join(settings.BASE_DIR, 'top rich2024.csv')
    country_counts = defaultdict(int)

    # 下面是check.py中生成的缺失的国家名
    country_mapping = {
        "Hong Kong": "China",
        "Russian Federation": "Russia",
        "Monaco": "Monaco",
        "Czech Republic": "Czech Rep.",
        "Taiwan": "China",
        "Cayman Islands": "Cayman Is.",
        "Korea, Republic of": "Korea"
    }


    try:
        # 使用 pandas 读取 CSV 文件，指定分隔符为逗号
        df = pd.read_csv(csv_file_path, delimiter=',', encoding='utf-8')

        # 检查是否存在 'Country / Region' 列
        if 'Country / Region' in df.columns:
            countries = df['Country / Region'].dropna().str.strip()
        else:
            print("Available columns:", df.columns)
            countries = pd.Series([])

        # 应用国家名称映射
        mapped_countries = countries.apply(lambda x: country_mapping.get(x, x))

        # 找出未映射的国家名称（用于调试）
        unmapped_countries = set(countries.unique()) - set(country_mapping.keys())
        print("Unmapped countries in data:", unmapped_countries)

        # 统计每个国家的富豪数量
        country_counts = mapped_countries.value_counts().to_dict()

        # 确保 'Hong Kong (China)' 存在于统计中
        if 'Hong Kong (China)' not in country_counts:
            country_counts['Hong Kong (China)'] = 0

    except FileNotFoundError:
        print(f"File not found: {csv_file_path}")
        country_counts = {}
    except Exception as e:
        print("Error reading CSV with pandas:", e)
        country_counts = {}

    # 准备 ECharts 所需的数据格式
    data = []
    for country, count in country_counts.items():
        if country == 'Hong Kong (China)':
            data.append({
                'name': country,
                'value': count,
                'itemStyle': {
                    'color': '#FF0000'  # 为香港设置独特的颜色，例如红色
                }
            })
        else:
            data.append({'name': country, 'value': count})

    # 序列化为 JSON
    data_json = json.dumps(data, ensure_ascii=False)

    return render(request, 'map.html', {'data': data_json})
