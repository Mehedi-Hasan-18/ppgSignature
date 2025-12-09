from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MenuItemViewSet, ReviewViewSet, OutletViewSet,
    ReservationViewSet, OrderViewSet
)

router = DefaultRouter()
router.register(r'menu', MenuItemViewSet, basename='menu')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'outlets', OutletViewSet, basename='outlets')
router.register(r'reservations', ReservationViewSet, basename='reservations')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]

