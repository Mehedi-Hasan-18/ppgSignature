from django.contrib import admin
from .models import MenuItem, Review, Outlet, Reservation, Order, OrderItem, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['url', 'uploaded_at']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'image', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'rating', 'date', 'created_at']
    list_filter = ['rating', 'date']
    search_fields = ['customer_name', 'comment']


@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'image', 'created_at']
    search_fields = ['name', 'address']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'outlet', 'date', 'time', 'number_of_guests', 'status', 'created_at']
    list_filter = ['status', 'date', 'outlet']
    search_fields = ['customer_name', 'email', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['customer_name', 'email', 'phone', 'delivery_address']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]

