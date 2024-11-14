from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('category-view/', views.CategoryView.as_view(), name="category_view"),
    path('category-view/<int:id>/', views.CategoryView.as_view(), name="category_view"),
    path('set-product-stock/', views.set_product_stock, name="set_product_stock"),
    path('delete-item-from-cart/', views.delete_item_from_cart, name="delete_item_from_cart"),
    path('clear-cart/', views.clear_cart, name="clear_cart"),
    path('place-order/', views.place_order, name="place_order"),
    path('orders-view/', views.OrdersView.as_view(), name="orders_view"),
    path("product-detail/<pk>/", views.ProductsDetailView.as_view(), name="products_detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

