import json
from django.shortcuts import render
from collections import defaultdict
from django.conf import settings
from .models import RichPerson

def map_view(request):
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
        # 从数据库中获取所有国家/地区
        countries = RichPerson.objects.values_list('country_region', flat=True)

        # 去除空值并去除首尾空白
        countries = [country.strip() for country in countries if country]

        # 应用国家名称映射
        mapped_countries = [country_mapping.get(country, country) for country in countries]

        # 统计每个国家的富豪数量
        for country in mapped_countries:
            country_counts[country] += 1

        # 确保 'Hong Kong (China)' 存在于统计中
        if 'Hong Kong (China)' not in country_counts:
            country_counts['Hong Kong (China)'] = 0

    except Exception as e:
        print("Error reading from the database:", e)
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
