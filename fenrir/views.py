from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.views.generic import TemplateView


import requests as req
from fenrir.models import Restaurant


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
        radius = int(request.GET.get('radius', 500))

        # ページネーションを考慮してデータを取得
        page = request.GET.get('page', 1)

        restaurants = get_restaurant_data(user_location, radius,page)
        paginated_restaurants = self.paginate_restaurants(request, restaurants)

        return self.render_to_response({'user_location': user_location, 'restaurants': paginated_restaurants})
     
    #検索半径の調整
    def get_search_range(self, radius):
        if radius <= 300:
            return 1
        elif radius <= 500:
            return 2
        elif radius <= 1000:
            return 3
        elif radius <= 2000:
            return 4
        else:
            return 5

    def paginate_restaurants(self, request, restaurants):
        # リクエストのGETパラメータから現在のページ番号を取得
        page = request.GET.get('page')

        # 10件ずつページネート
        paginator = Paginator(restaurants, 10)
        # 現在のページのPageオブジェクトを取得
        paginated_restaurants = paginator.get_page(page)


       # try:
            # 現在のページのPageオブジェクトを取得
            #paginated_restaurants = paginator.get_page(page)
        #except PageNotAnInteger:
            # もしページが整数でない場合は、最初のページを表示
           # paginated_restaurants = paginator.page(1)
        #except EmptyPage:
            # もしページが範囲外（例：9999）の場合は、結果の最後のページを表示
            #paginated_restaurants = paginator.page(paginator.num_pages)

        return paginated_restaurants





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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.get_object()
        return context




def get_user_location(request):
    # クライアントのブラウザからGeolocation APIを使用して現在地を取得
    # 現在地の緯度と経度を取得する処理を実装

    user_location = {
        'latitude': 35.6895,  # 仮のデフォルト値（東京駅周辺）
        'longitude': 139.6917,
    }

    return user_location








def get_restaurant_data(user_location, radius, page=1):
    api_key = '7699907c06980421'
    endpoint = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

    params = {
        'key': api_key,
        'lat': user_location['latitude'],
        'lng': user_location['longitude'],
        'range': radius,
        'format': 'json',
        'start': page,
    }

    response = req.get(endpoint, params=params)

    if response.status_code != 200:
        print(f"APIリクエストエラー: {response.status_code}")
        print(response.text)  # エラーレスポンスの内容を表示
        return []  # エラーの場合は空のリストを返すか、エラーを処理するか

    data = response.json()

    restaurants = []
    for entry in data.get('results', {}).get('shop', []):
        restaurant_data = {
            'id': entry.get('id', ''),  # id フィールドを追加
            'name': entry.get('name', ''),
            'address': entry.get('address', ''),
            'access': entry.get('access', ''),
            'business_hours':entry.get('open',''),
            'thumbnail_image': entry.get('photo', {}).get('pc', {}).get('l', ''),
        }

        

        # 新しい Restaurant インスタンスを作成
        restaurant = Restaurant(**restaurant_data)
        restaurant.save()  # データベースに保存

        restaurants.append(restaurant)

    return restaurants


