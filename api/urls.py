from django.urls import path
from .views import (
    MenuListView,
    MenuDetailView,
    CategoryListView,
    ReservationListCreateView,
    ReservationDetailView,
    OrderListCreateView,
    OrderDetailView,
    OrderStatusUpdateView,
    SeedMenuView,
    RegisterUserView  
)

urlpatterns = [
    
    path('menu/', MenuListView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', MenuDetailView.as_view(), name='menu-detail'),


    path('categories/', CategoryListView.as_view(), name='category-list'),


    path('reservations/', ReservationListCreateView.as_view(), name='reservation-list-create'),
    path('reservations/<int:pk>/', ReservationDetailView.as_view(), name='reservation-detail'),

    
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderStatusUpdateView.as_view(), name='order-status-update'),


    path('seed-menu/', SeedMenuView.as_view(), name='seed-menu'),


    path('register/', RegisterUserView.as_view(), name='register'),
]