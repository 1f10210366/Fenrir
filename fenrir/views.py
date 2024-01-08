from django.views.generic import TemplateView, ListView
from django.shortcuts import get_object_or_404
from fenrir.models import Restaurant
import requests as req

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
class TopView(TemplateView):
    template_name = "fenrir/search_input.html"

class SearchResultsView(ListView):
    model = Restaurant
    template_name = "fenrir/search_results.html"
    context_object_name = "restaurants"
    paginate_by = 10

    def get_queryset(self):
        user_location = {
            'latitude': float(self.request.GET.get('latitude', 35.6895)),
            'longitude': float(self.request.GET.get('longitude', 139.6917)),
        }
        radius = int(self.request.GET.get('radius', 500))
        search_range = self.get_search_range(radius)
        all_restaurants = self.get_all_restaurants(user_location, search_range)

        if not all_restaurants:
            return []

        return all_restaurants

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ページネーションの処理を追加
        paginator = Paginator(self.object_list, self.paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            restaurants = paginator.page(page)
        except PageNotAnInteger:
            restaurants = paginator.page(1)
        except EmptyPage:
            restaurants = paginator.page(paginator.num_pages)

        context['restaurants'] = restaurants
        return context
    

    def get_all_restaurants(self, user_location, radius, per_page=10):
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

            for entry in current_page_restaurants:
                restaurant_data = {
                    'id': entry.get('id', ''),
                    'name': entry.get('name', ''),
                    'address': entry.get('address', ''),
                    'access': entry.get('access', ''),
                    'business_hours': entry.get('open', ''),
                    'thumbnail_image': entry.get('photo', {}).get('pc', {}).get('l', ''),
                }

                restaurant = Restaurant(**restaurant_data)
                restaurant.save()
                all_restaurants.append(restaurant)

            page += 1

        return all_restaurants

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

class RestaurantDetailView(TemplateView):
    template_name = "fenrir/restaurant_detail.html"

    model = Restaurant
    template_name = "fenrir/restaurant_detail.html"
    context_object_name = "restaurant"

    def get_object(self, queryset=None):
        restaurant_id = self.kwargs.get('restaurant_id')
        return get_object_or_404(Restaurant, id=restaurant_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['restaurant'] = self.get_object()
        return context

def get_user_location(request):
    user_location = {
        'latitude': 35.6895,
        'longitude': 139.6917,
    }
    return user_location


