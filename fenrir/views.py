from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests 
from .models import Restaurant

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class TopView(TemplateView):
    template_name = "fenrir/seach_input.html"


class SearchResultsView(TemplateView):
    template_name = "fenrir/seach_result.html"

class restaurant_detailView(TemplateView):
    template_name = "fenrir/restaurant_detail.html"






def get_user_location(request):
    # クライアントのブラウザからGeolocation APIを使用して現在地を取得
    # 現在地の緯度と経度を取得する処理を実装

    user_location = {
        'latitude': 35.6895,  # 仮のデフォルト値（東京駅周辺）
        'longitude': 139.6917,
    }

    return user_location





def get_restaurant_data(user_location, radius=500):
   
    api_key = '7699907c06980421'
    endpoint = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/?key=sample&large_area=Z011'

    params = {
        'key': api_key,
        'lat': user_location['latitude'],
        'lng': user_location['longitude'],
        'range': radius,
        'format': 'json',
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    # レスポンスから必要な情報を抽出してリストに格納
    restaurants = []
    for entry in data['results']['shop']:
        restaurant = Restaurant(
            name=entry['name'],
            address=entry['address'],
            access=entry.get('access', ''),
            business_hours=entry.get('open', ''),
            thumbnail_image=entry.get('photo', {}).get('pc', {}).get('l', ''),
        )
        restaurants.append(restaurant)

    return restaurants






def search_results(request):
    user_location = get_user_location(request)
    restaurants = get_restaurant_data(user_location)
    paginated_restaurants = paginate_restaurants(request, restaurants)

    return render(request, 'fenrir/search_results.html', {'user_location': user_location, 'restaurants': paginated_restaurants})



def paginate_restaurants(request, restaurants):
    # ページネーションを実装
    # 1ページあたりのアイテム数は適宜調整

    paginator = Paginator(restaurants, 10)  # 1ページあたり10アイテム

    page = request.GET.get('page')
    try:
        paginated_restaurants = paginator.page(page)
    except PageNotAnInteger:
        paginated_restaurants = paginator.page(1)
    except EmptyPage:
        paginated_restaurants = paginator.page(paginator.num_pages)

    return paginated_restaurants



