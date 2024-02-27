from django.urls import path
from . import views


urlpatterns = [
    path('', views.view_items, name = 'home'),
    path('item/<int:item_id>/', views.view_item, name = 'view_item'),
    path('item/<int:item_id>/add_review/', views.add_review, name='add_review'),    
    path('cart/', views.view_cart, name = 'cart'),
    path('checkout/', views.view_checkout, name = 'checkout'),
    path('add/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('item/<int:item_id>/add_review/', views.add_review, name='add_review'),
    path('search/', views.search, name='search_results'),
]