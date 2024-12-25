import json
from django.shortcuts import render
from collections import defaultdict
from .models import RichPerson

def home_view(request):
    """
    从数据库中读取国家/地区的富豪数量数据，并准备可视化地图所需的格式。
    """
    # 初始化国家计数字典
    country_counts = defaultdict(int)

    # 国家名称映射（根据 check.py 中定义的映射）
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
        # 从数据库中获取所有国家/地区字段
        countries = RichPerson.objects.values_list('country_region', flat=True)

        # 去除空值并去除首尾空白
        countries = [country.strip() for country in countries if country]

        # 应用国家名称映射规则
        mapped_countries = [country_mapping.get(country, country) for country in countries]

        # 统计每个国家的富豪数量
        for country in mapped_countries:
            country_counts[country] += 1

    except Exception as e:
        # 记录错误日志，返回空数据
        print(f"Error reading from the database: {e}")
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

    # 将数据序列化为 JSON 格式
    data_json = json.dumps(data, ensure_ascii=False)

    # 渲染 home.html 模板
    return render(request, 'home.html', {'data': data_json})
