from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView

app_name = 'products'
urlpatterns = [
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path('detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('create/', ProductCreateView.as_view(), name='create-product'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product-delete')

]



















