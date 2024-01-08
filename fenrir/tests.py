from django.test import TestCase,Client
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests as req
#from fenrir.models import Restaurant


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404

import requests as req  # Assuming you have requests library imported

def get_all_restaurants(user_location, radius, per_page=10):
    api_key = '7699907c06980421'
    endpoint = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    
    all_restaurants = []
    page = 1

    while True:
        start = (page - 1) * per_page + 1

        params = {
            'key': api_key,
            'lat': user_location['latitude'],
            'lng': user_location['longitude'],
            'range': radius,
            'format': 'json',
            'start': start,
            'count': per_page,
        }

        response = req.get(endpoint, params=params)

        if response.status_code != 200:
            print(f"APIリクエストエラー: {response.status_code}")
            print(response.text)
            return all_restaurants

        data = response.json()

        current_page_restaurants = data.get('results', {}).get('shop', [])
        if not current_page_restaurants:
            break

        all_restaurants.extend(current_page_restaurants)
        page += 1

    return all_restaurants





def paginate_restaurants(restaurants, current_page=1, per_page=10):
    # リクエストのGETパラメータから現在のページ番号を取得
    paginator = Paginator(restaurants, per_page)
    
    # デバッグ用にPaginatorの属性を表示
    print(f"ページ数: {paginator.num_pages}")
    print(f"オブジェクト数: {paginator.count}")
    print(f"ページレンジ: {paginator.page_range}")

   
        
    try:
        paginated_restaurants = paginator.page(current_page)
    except PageNotAnInteger:
        # もしページが整数でない場合は、最初のページを返します。
        paginated_restaurants = paginator.page(1)
    except EmptyPage:
        # もしページが範囲外（例：9999）の場合は、結果の最後のページを返します。
        paginated_restaurants = paginator.page(paginator.num_pages)

    return paginated_restaurants


user_location = {
    'latitude': 35.6895,  # 仮のデフォルト値（東京駅周辺）
    'longitude': 139.6917,
}

all_restaurants = get_all_restaurants(user_location, 500)
paginated_all_restaurants = paginate_restaurants(all_restaurants, current_page=1, per_page=10)



from django.test import TestCase, Client
from django.urls import reverse

class FenrirViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_search_results_view(self):
        # ビューのURLをreverseして取得
        url = reverse('fenrir:search_results')

        # テスト用のデータを作成
        user_location = {'latitude': 35.6895, 'longitude': 139.6917}
        restaurants = get_all_restaurants(user_location, 500)

        # テスト用のクエリパラメータを含んだURLを生成
        url_with_params = f"{url}?latitude={user_location['latitude']}&longitude={user_location['longitude']}&radius=500&page=1"

        # クライアントを使用してビューにリクエストを送信
        response = self.client.get(url_with_params)

        # レスポンスが正常なステータスコードを返すかを確認
        self.assertEqual(response.status_code, 200)

        # 特定のHTML要素やテキストがレスポンスに含まれているかを確認
        self.assertContains(response, '検索結果')
        self.assertContains(response, 'ホーム')

        # 特定のテンプレートが使われているかを確認
        self.assertTemplateUsed(response, 'fenrir/search_results.html')

        # ページネーションのテスト
        self.assertContains(response, '1 /')  # 1ページ目を表示しているか

        # レストランの情報が表示されているか
        for restaurant in restaurants:
            self.assertContains(response, restaurant['name'])
            self.assertContains(response, restaurant['address'])
            self.assertContains(response, restaurant['access'])
            self.assertContains(response, restaurant['thumbnail_image'])

       
