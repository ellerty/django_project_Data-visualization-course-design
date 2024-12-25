import json
from django.shortcuts import render
from collections import defaultdict

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


def data_analysis_view(request):
    # 数据分析页面的视图逻辑
    analysis_data = {
        'total_rich': 5000,
        'average_wealth': 1000000,
        # 其他分析数据...
    }
    return render(request, 'data_analysis.html', {'analysis_data': analysis_data})



# visualization/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RichPerson
from .serializers import RichPersonSerializer
import re
from django.db.models import Count

def parse_money(money_str):
    """
    将类似于 "+$62.8B" 或 "-$131M" 的字符串转换为浮点数。
    "B" 代表十亿（1e9），"M" 代表百万（1e6）。
    """
    if not isinstance(money_str, str):
        return 0
    money_str = money_str.strip().replace(',', '')
    pattern = r'^([+-]?)[\$]?(\d+(\.\d+)?)([BM]?)$'
    match = re.match(pattern, money_str)
    if not match:
        return 0
    sign, amount, _, unit = match.groups()
    amount = float(amount)
    if unit == 'B':
        amount *= 1e9
    elif unit == 'M':
        amount *= 1e6
    if sign == '-':
        amount *= -1
    return amount


@api_view(['GET'])
def growth_top_30(request):
    """
    返回财富增长最多的前30名（包括负增长）。
    按照 last_change 的实际值从大到小排序（正增长大于负增长）。
    """
    billionaires = RichPerson.objects.all()

    # 按照 last_change 解析后的实际值从大到小排序
    sorted_billionaires = sorted(
        billionaires,
        key=lambda x: parse_money(x.last_change),
        reverse=True
    )

    top_30 = sorted_billionaires[:30]
    data = []
    for b in top_30:
        data.append({
            'name': b.name,
            'last_change': parse_money(b.last_change)
        })
    return Response(data)

@api_view(['GET'])
def wealth_top_30(request):
    """
    返回财富最多的前30名。
    按照 total_net_worth 从大到小排序。
    """
    billionaires = RichPerson.objects.all()

    # 按照 total_net_worth 解析后的值从大到小排序
    sorted_billionaires = sorted(
        billionaires,
        key=lambda x: parse_money(x.total_net_worth),
        reverse=True
    )

    top_30 = sorted_billionaires[:30]
    data = []
    for b in top_30:
        data.append({
            'name': b.name,
            'total_net_worth': parse_money(b.total_net_worth)
        })
    return Response(data)

@api_view(['GET'])
def industry_proportion(request):
    """
    返回所有富豪的行业占比。
    使用 Django ORM 的聚合功能优化查询。
    """
    industries = RichPerson.objects.values('industry').annotate(count=Count('id')).order_by('-count')
    data = list(industries)
    return Response(data)
