from django.urls import path
from . import views

app_name = "fenrir"
urlpatterns = [
  path("",views.TopView.as_view(),name="search_input"),
  path("search_results/", views.SearchResultsView.as_view(), name="search_results"),
  path('restaurant_detail/<str:restaurant_id>/', views.RestaurantDetailView.as_view(), name='restaurant_detail'),
  path("question/", views.questionView.as_view(), name="question"),
  path("use/", views.useView.as_view(), name="use"),
]
