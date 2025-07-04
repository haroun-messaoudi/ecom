
from django.urls import path,include
from .views import ProductListView, CategoryListView, ProductDetailView , DiscountedProductListView, TopOrderedProductsView , NewProductListView

urlpatterns = [
    path('list',ProductListView.as_view(), name='product-list-create'),
    path('category/list', CategoryListView.as_view(), name='category-list-create'),
    path('<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('discounted/', DiscountedProductListView.as_view(), name='discounted-product-list'),
    path('top-ordered/', TopOrderedProductsView.as_view(), name='top-ordered-products'),
    path('new-products/', NewProductListView.as_view(), name='new-product-list'),

]
