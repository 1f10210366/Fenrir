from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests as req
from .models import Restaurant

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404


class TopView(TemplateView):
    template_name = "fenrir/search_input.html"
    
class SearchResultsView(TemplateView):
    template_name = "fenrir/search_results.html"

    def get(self, request, *args, **kwargs):
        # クライアントから送信された位置情報を取得
        user_location = {
            'latitude': float(request.GET.get('latitude', 35.6895)),
            'longitude': float(request.GET.get('longitude', 139.6917)),
        }
        radius = int(request.GET.get('radius',500))

        restaurants = get_restaurant_data(user_location, radius)
        paginated_restaurants = paginate_restaurants(request, restaurants)

        return self.render_to_response({'user_location': user_location, 'restaurants': paginated_restaurants})
            


class RestaurantDetailView(TemplateView):
    template_name = "fenrir/restaurant_detail.html"


    model = Restaurant
    template_name = "fenrir/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_object(self, queryset=None):
        # URL パターンで指定された restaurant_id を取得
        restaurant_id = self.kwargs.get('restaurant_id')
        # データベースから Restaurant モデルのインスタンスを取得
        return get_object_or_404(Restaurant, id=restaurant_id)




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
    endpoint = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

    params = {
        'key': api_key,
        'lat': user_location['latitude'],
        'lng': user_location['longitude'],
        'range': radius,
        'format': 'json',
    }

    response = req.get(endpoint, params=params)

    if response.status_code != 200:
        print(f"APIリクエストエラー: {response.status_code}")
        print(response.text)  # エラーレスポンスの内容を表示

    data = response.json()
    

    # レスポンスから必要な情報を抽出してリストに格納
    restaurants = []
    for entry in data.get('results', {}).get('shop', []):
        restaurant = {
            'id': entry.get('id', ''),  # id フィールドを追加
            'name': entry.get('name', ''),
            'address': entry.get('address', ''),
            'access': entry.get('access', ''),
            'thumbnail_image': entry.get('photo', {}).get('pc', {}).get('l', ''),
        }
        restaurants.append(restaurant)

    return restaurants



def paginate_restaurants(request, restaurants):
    paginator = Paginator(restaurants, 10)  # 1ページあたり10アイテム

    page = request.GET.get('page',1)
    try:
        paginated_restaurants = paginator.page(page)
    except PageNotAnInteger:
        paginated_restaurants = paginator.page(1)
    except EmptyPage:
        paginated_restaurants = paginator.page(paginator.num_pages)

    return paginated_restaurants



