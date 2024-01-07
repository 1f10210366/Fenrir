from django.test import TestCase
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests as req
#from fenrir.models import Restaurant


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

import requests as req  # Assuming you have requests library imported

def get_restaurant_data(user_location, radius, page=1, per_page=10):
    api_key = '7699907c06980421'
    endpoint = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

    start = (page - 1) * per_page + 1


    params = {
        'key': api_key,
        'lat': user_location['latitude'],
        'lng': user_location['longitude'],
        'range': radius,
        'format': 'json',
        'start': start,
        'count': per_page,  # 修正: ページごとの結果数を指定
    }

    response = req.get(endpoint, params=params)

    if response.status_code != 200:
        print(f"APIリクエストエラー: {response.status_code}")
        print(response.text)  # エラーレスポンスの内容を表示
        return []  # エラーの場合は空のリストを返すか、エラーを処理するか

    data = response.json()

    restaurants = []
    for entry in data.get('results', {}).get('shop', []):
        restaurant = {
            'id': entry.get('id', ''),
            'name': entry.get('name', ''),
            'address': entry.get('address', ''),
            'access': entry.get('access', ''),
            'thumbnail_image': entry.get('photo', {}).get('pc', {}).get('l', ''),
        }
        restaurants.append(restaurant)

    print("Number of restaurants:", len(restaurants))

    return restaurants




def paginate_restaurants(restaurants):
        # リクエストのGETパラメータから現在のページ番号を取得
      
        paginator = Paginator(restaurants, 10)
    # デバッグ用にPaginatorの属性を表示
        print(f"ページ数: {paginator.num_pages}")
        print(f"オブジェクト数: {paginator.count}")
        print(f"ページレンジ: {paginator.page_range}")

       



user_location = {
        'latitude': 35.6895 ,  # 仮のデフォルト値（東京駅周辺）
        'longitude': 139.6917,
    }


restaurants = get_restaurant_data(user_location, 500)
paginated_restaurants = paginate_restaurants(restaurants)

print(paginated_restaurants)