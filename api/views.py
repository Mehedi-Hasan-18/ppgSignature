from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MenuItem, Review, Outlet, Reservation, Order, OrderItem, Image
from .serializers import (
    MenuItemSerializer, ReviewSerializer, OutletSerializer,
    ReservationSerializer, OrderSerializer, OrderItemSerializer
)


from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        self._handle_image(instance, self.request.data.get('image'))

    def perform_update(self, serializer):
        instance = serializer.save()
        self._handle_image(instance, self.request.data.get('image'))

    def _handle_image(self, instance, image):
        if image:
            if hasattr(image, 'read'):  # It's a file
                import cloudinary.uploader
                result = cloudinary.uploader.upload(image, folder='menu_items/')
                img_obj, created = Image.objects.get_or_create(url=result['secure_url'])
            elif isinstance(image, str) and image.strip():  # It's a URL string
                img_obj, created = Image.objects.get_or_create(url=image.strip())
            else:
                return
            instance.image = img_obj
            instance.save()


class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class OutletViewSet(viewsets.ModelViewSet):
    queryset = Outlet.objects.all()
    serializer_class = OutletSerializer
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        self._handle_image(instance, self.request.data.get('image'))

    def perform_update(self, serializer):
        instance = serializer.save()
        self._handle_image(instance, self.request.data.get('image'))

    def _handle_image(self, instance, image):
        if image:
            if hasattr(image, 'read'):  # It's a file
                import cloudinary.uploader
                result = cloudinary.uploader.upload(image, folder='outlets/')
                img_obj, created = Image.objects.get_or_create(url=result['secure_url'])
            elif isinstance(image, str) and image.strip():  # It's a URL string
                img_obj, created = Image.objects.get_or_create(url=image.strip())
            else:
                return
            instance.image = img_obj
            instance.save()


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

