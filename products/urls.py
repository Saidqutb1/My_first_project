from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, AddToCartView, CartDetailView, RemoveFromCartView
from . import views

app_name = 'products'
urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='create-product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete'),
    path('add/<int:pk>/', AddToCartView.as_view(), name='add-to-cart'),
    path('detail/', CartDetailView.as_view(), name='cart-detail'),
    path('remove/<int:pk>/', RemoveFromCartView.as_view(), name='remove-from-cart'),
]



















