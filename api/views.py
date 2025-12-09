from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MenuItem, Review, Outlet, Reservation, Order, OrderItem
from .serializers import (
    MenuItemSerializer, ReviewSerializer, OutletSerializer,
    ReservationSerializer, OrderSerializer, OrderItemSerializer
)


class MenuItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OutletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Extract items from request
        items_data = request.data.pop('items', [])
        
        # Calculate total amount
        total_amount = 0
        for item_data in items_data:
            menu_item_id = item_data.get('menu_item')
            quantity = item_data.get('quantity', 1)
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
                total_amount += menu_item.price * quantity
            except MenuItem.DoesNotExist:
                pass
        
        # Create order
        order_data = request.data.copy()
        order_data['total_amount'] = total_amount
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # Create order items
        for item_data in items_data:
            menu_item_id = item_data.get('menu_item')
            quantity = item_data.get('quantity', 1)
            try:
                menu_item = MenuItem.objects.get(id=menu_item_id)
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=menu_item.price
                )
            except MenuItem.DoesNotExist:
                pass
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

