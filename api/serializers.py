from rest_framework import serializers
from .models import MenuItem, Review, Outlet, Reservation, Order, OrderItem


class MenuItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False, write_only=True)
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'description', 'price', 'category', 'image', 'image_url', 'is_featured', 'order_count', 'created_at', 'updated_at']

    def _get_uploaded_image(self):
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request is not None:
            return request.FILES.get('image') or request.FILES.get('image_url')
        return self.initial_data.get('image') or self.initial_data.get('image_url')

    def get_image_url(self, obj):
        if obj.image and obj.image.url:
            url = obj.image.url.url if hasattr(obj.image.url, 'url') else obj.image.url
            request = self.context.get('request')
            if url.startswith('http'):
                return url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def create(self, validated_data):
        image_file = validated_data.pop('image', None) or self._get_uploaded_image()
        menu_item = super().create(validated_data)
        if image_file:
            from .models import Image
            image_instance = Image.objects.create(url=image_file)
            menu_item.image = image_instance
            menu_item.save()
        return menu_item

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None) or self._get_uploaded_image()
        menu_item = super().update(instance, validated_data)
        if image_file:
            from .models import Image
            if menu_item.image:
                menu_item.image.url = image_file
                menu_item.image.save()
            else:
                image_instance = Image.objects.create(url=image_file)
                menu_item.image = image_instance
                menu_item.save()
        return menu_item


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class OutletSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(required=False, write_only=True)
    
    class Meta:
        model = Outlet
        fields = ['id', 'name', 'address', 'phone', 'hours', 'image', 'image_url', 'created_at', 'updated_at']

    def _get_uploaded_image(self):
        request = self.context.get('request') if hasattr(self, 'context') else None
        if request is not None:
            return request.FILES.get('image') or request.FILES.get('image_url')
        return self.initial_data.get('image') or self.initial_data.get('image_url')

    def get_image_url(self, obj):
        if obj.image and obj.image.url:
            url = obj.image.url.url if hasattr(obj.image.url, 'url') else obj.image.url
            request = self.context.get('request')
            if url.startswith('http'):
                return url
            if request is not None:
                return request.build_absolute_uri(url)
            return url
        return None

    def create(self, validated_data):
        image_file = validated_data.pop('image', None) or self._get_uploaded_image()
        outlet = super().create(validated_data)
        if image_file:
            from .models import Image
            image_instance = Image.objects.create(url=image_file)
            outlet.image = image_instance
            outlet.save()
        return outlet

    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None) or self._get_uploaded_image()
        outlet = super().update(instance, validated_data)
        if image_file:
            from .models import Image
            if outlet.image:
                outlet.image.url = image_file
                outlet.image.save()
            else:
                image_instance = Image.objects.create(url=image_file)
                outlet.image = image_instance
                outlet.save()
        return outlet


class ReservationSerializer(serializers.ModelSerializer):
    outlet_name = serializers.CharField(source='outlet.name', read_only=True)
    
    class Meta:
        model = Reservation
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menu_item_image = serializers.URLField(source='menu_item.image.url', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

