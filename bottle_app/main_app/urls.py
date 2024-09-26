from .views import *
from django.urls import path
urlpatterns = [
    path('bottles/create/', BottleCreateView.as_view()),
    path('bottles/<int:pk>/', BottleReadView.as_view()),
    path('shop/items/', ShopItemListView.as_view()),
    path('user/profile/create/', UserProfileCreateView.as_view()),
    path('user/rankings' , UserRankingView.as_view),
    path('user/create/', UserProfileCreateView.as_view())
]
