from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import ProductAdminViewSet, ProductManagementViewSet

router = DefaultRouter()
router.register(r'admin-products', ProductAdminViewSet, basename='admin-product')
router.register(r'manage-products', ProductManagementViewSet, basename='manage-product')

urlpatterns = [
    # Customer Views
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    

    # Authentication (Website)
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Order & External Services Logic
    path('order/create/', views.order_create, name='order_create'),
    path('order/success/', views.payment_success, name='payment_success'),

    # API
    path('api/products/', views.ProductListAPIView.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
    path('api/order/create/', views.OrderCreateView.as_view(), name='api_order_create'),
    path('api/auth/login/', views.CustomAuthToken.as_view(), name='api_auth_login'),
    path('api/auth/register/', views.RegisterAPIView.as_view(), name='api_auth_register'),
    path('api/auth/logout/', views.LogoutAPIView.as_view(), name='api_auth_logout'),
    path('checkout/', views.checkout_view, name='checkout'),

    path('api/', include(router.urls)),
]