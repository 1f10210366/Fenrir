from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests as req
from .models import Restaurant

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class TopView(TemplateView):
    template_name = "fenrir/search_input.html"
    
class SearchResultsView(TemplateView):
    template_name = "fenrir/search_results.html"

    def get(self, request, *args, **kwargs):
        # ユーザーの現在地を取得
        user_location = get_user_location(request)

        # レストランデータを取得
        restaurants = get_restaurant_data(user_location)

        # ページネーションを適用
        paginated_restaurants = paginate_restaurants(request, restaurants)

        # テンプレートにデータを渡してレンダリング
        context = {
            'restaurants': paginated_restaurants,
        }
        return render(request, self.template_name, context)


class RestaurantDetailView(TemplateView):
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
            'name': entry.get('name', ''),
            'address': entry.get('address', ''),
            'access': entry.get('access', ''),
            'thumbnail_image': entry.get('photo', {}).get('pc', {}).get('l', ''),
        }
        restaurants.append(restaurant)

    return restaurants



def paginate_restaurants(request, restaurants):
    paginator = Paginator(restaurants, 10)  # 1ページあたり10アイテム

    page = request.GET.get('page')
    try:
        paginated_restaurants = paginator.page(page)
    except PageNotAnInteger:
        paginated_restaurants = paginator.page(1)
    except EmptyPage:
        paginated_restaurants = paginator.page(paginator.num_pages)

    return paginated_restaurants



#def search_restaurants(request):
    # ユーザーの現在地を取得
    user_location = get_user_location(request)

    # レストランデータを取得
    restaurants = get_restaurant_data(user_location)

    
    return render(request, 'fenrir/search_result.html', restaurants)