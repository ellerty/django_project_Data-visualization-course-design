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


def character_analysis_view(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = RichPerson.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'character_analysis.html', context)

import json
import httpx
import logging
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse, JsonResponse
from .models import RichPerson
from django.conf import settings
import asyncio

logger = logging.getLogger('visualization')  # 使用你的应用名

async def get_ai_summary_stream(request, pk):
    if request.method != 'GET':
        logger.warning(f"Invalid request method: {request.method} for pk={pk}")
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    person = get_object_or_404(RichPerson, pk=pk)
    logger.debug(f"Fetching AI summary for person: {person.name} (pk={pk})")

    # 替换为你的中转 API 平台的 OpenAI API 地址
    api_url = 'https://your-relay-api-platform.com/api/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.AI_API_KEY}'
    }
    user_message = (
        f"请概括以下人物的信息：\n"
        f"姓名: {person.name}\n"
        f"排名: {person.rank}\n"
        f"总财富: {person.total_net_worth}\n"
        f"国家/地区: {person.country_region}\n"
        f"行业: {person.industry}\n"
        f"简介: {person.extract}"
    )
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': user_message}
    ]
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
        'stream': True  # 启用流式响应
    }

    try:
        async with httpx.AsyncClient(timeout=None) as client:
            logger.debug(f"Sending POST request to AI API at {api_url}")
            response = await client.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            logger.debug(f"Received response status: {response.status_code}")

            async def stream():
                async for chunk in response.aiter_text():
                    if chunk:
                        # 假设中转 API 的流式响应格式与 OpenAI 相同
                        if chunk.startswith('data: '):
                            data_str = chunk.replace('data: ', '').strip()
                            if data_str == '[DONE]':
                                logger.debug("Received [DONE] signal from AI API")
                                break
                            try:
                                data_json = json.loads(data_str)
                                text = data_json['choices'][0]['delta'].get('content', '')
                                if text:
                                    logger.debug(f"Streaming text chunk: {text}")
                                    yield text
                            except json.JSONDecodeError as e:
                                logger.error(f"JSON decode error: {e} - Chunk: {data_str}")
                                continue

            return StreamingHttpResponse(stream(), content_type='text/plain')
    except httpx.HTTPError as e:
        logger.error(f"HTTPError when fetching AI summary: {e}")
        return JsonResponse({'error': 'Failed to get summary from AI API.'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt  # 如果使用 AJAX POST 请求，确保 CSRF 令牌正确传递，或根据需要禁用
def get_ai_summary(request, pk):
    if request.method != 'POST':
        logger.warning(f"Invalid request method: {request.method} for pk={pk}")
        return JsonResponse({'error': 'Invalid request method.'}, status=405)

    person = get_object_or_404(RichPerson, pk=pk)
    logger.debug(f"Fetching AI summary for person: {person.name} (pk={pk})")

    api_url = 'https://gpt.soruxgpt.com/api/api/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.AI_API_KEY}'  # 从 settings.py 中获取
    }
    user_message = (
        f"请概括以下人物的信息：\n"
        f"姓名: {person.name}\n"
        f"排名: {person.rank}\n"
        f"总财富: {person.total_net_worth}\n"
        f"国家/地区: {person.country_region}\n"
        f"行业: {person.industry}\n"
        f"简介: {person.extract}"
    )
    messages = [
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': user_message}
    ]
    data = {
        'model': 'gpt-3.5-turbo',
        'messages': messages,
        'stream': False  # 关闭流式响应
    }

    try:
        with httpx.Client(timeout=60) as client:
            logger.debug(f"Sending POST request to AI API at {api_url}")
            response = client.post(api_url, headers=headers, json=data)
            response.raise_for_status()
            logger.debug(f"Received response status: {response.status_code}")

            response_data = response.json()
            logger.debug(f"AI API response: {response_data}")

            # 解析 AI API 返回的内容
            ai_text = ""
            for choice in response_data.get('choices', []):
                ai_text += choice.get('message', {}).get('content', '')

            return JsonResponse({'ai_summary': ai_text})
    except httpx.HTTPError as e:
        logger.error(f"HTTPError when fetching AI summary: {e}")
        return JsonResponse({'error': 'Failed to get summary from AI API.'}, status=500)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return JsonResponse({'error': 'An unexpected error occurred.'}, status=500)

def character_detail_view(request, pk):
    # 获取单个人物对象
    person = get_object_or_404(RichPerson, pk=pk)

    # 将人物数据序列化为 JSON 格式
    person_data = json.dumps({
        'id': person.id,
        'name': person.name,
        'rank': person.rank,
        'total_net_worth': person.total_net_worth,
        'country_region': person.country_region,
        'industry': person.industry,
        'image_url': person.image_url or '',
        'extract': person.extract or '',
    })

    # 将人物对象和 JSON 数据传递到模板
    return render(request, 'character_detail.html', {'person': person, 'person_data': person_data})
