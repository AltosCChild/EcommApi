from django.urls import path
from . import views

urlpatterns = [
    path('products/',views.productsList,name='products-list'),
    path('products/<str:pk>/',views.productsDetails,name='products-detail'),
    path('top/',views.topProducts,name='top-products'),
    
    path('orders/',views.allOrders,name='orders'),
    path('myorders/',views.myOrder,name='myOrder'),
    path('orderbyid/<str:pk>/',views.OrderById,name='order-id'),
    path('addorderitems/',views.addOrderItems,name='add-items')
]