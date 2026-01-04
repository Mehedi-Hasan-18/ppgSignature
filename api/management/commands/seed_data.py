from django.core.management.base import BaseCommand
from api.models import MenuItem, Review, Outlet, Image


class Command(BaseCommand):
    help = 'Seed the database with initial data'

    def handle(self, *args, **options):
        # Clear existing data
        MenuItem.objects.all().delete()
        Review.objects.all().delete()
        Outlet.objects.all().delete()
        Image.objects.all().delete()

        # Create Menu Items
        menu_items = [
            {
                'name': 'Signature Pasta',
                'description': 'Handcrafted pasta with premium ingredients, served with our secret sauce',
                'price': 24.99,
                'category': 'Main Course',
                'image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 150
            },
            {
                'name': 'Gourmet Pizza',
                'description': 'Fresh ingredients, authentic taste, wood-fired to perfection',
                'price': 18.99,
                'category': 'Main Course',
                'image_url': 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 120
            },
            {
                'name': 'Premium Burger',
                'description': 'Juicy, flavorful, unforgettable - our signature burger',
                'price': 16.99,
                'category': 'Main Course',
                'image_url': 'https://images.unsplash.com/photo-1551782450-a2132b4ba21d?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 95
            },
            {
                'name': 'Artisan Desserts',
                'description': 'Sweet perfection in every bite, crafted by our pastry chef',
                'price': 12.99,
                'category': 'Dessert',
                'image_url': 'https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 110
            },
            {
                'name': 'Caesar Salad',
                'description': 'Fresh romaine lettuce with our house-made Caesar dressing',
                'price': 14.99,
                'category': 'Appetizer',
                'image_url': 'https://images.unsplash.com/photo-1546793665-c74683f339c1?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 75
            },
            {
                'name': 'Grilled Salmon',
                'description': 'Fresh Atlantic salmon, perfectly grilled with herbs',
                'price': 28.99,
                'category': 'Main Course',
                'image_url': 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?w=400&h=300&fit=crop',
                'is_featured': True,
                'order_count': 80
            },
        ]

        for item_data in menu_items:
            image_url = item_data.pop('image_url')
            image_obj = Image.objects.create(url=image_url)
            item_data['image'] = image_obj
            MenuItem.objects.create(**item_data)

        # Create Reviews
        reviews = [
            {
                'customer_name': 'John Doe',
                'rating': 5,
                'comment': 'Amazing food and excellent service! The Signature Pasta was absolutely delicious. Will definitely come back!',
            },
            {
                'customer_name': 'Jane Smith',
                'rating': 5,
                'comment': 'Best restaurant in town. Highly recommended! The atmosphere is great and the staff is very friendly.',
            },
            {
                'customer_name': 'Mike Johnson',
                'rating': 4,
                'comment': 'Great atmosphere and delicious food. The pizza was fantastic, though the wait time was a bit long.',
            },
            {
                'customer_name': 'Sarah Williams',
                'rating': 5,
                'comment': 'Perfect for special occasions. Will come back! The desserts are to die for.',
            },
            {
                'customer_name': 'David Brown',
                'rating': 5,
                'comment': 'Outstanding experience from start to finish. The grilled salmon was cooked to perfection!',
            },
        ]

        for review_data in reviews:
            Review.objects.create(**review_data)

        # Create Outlets
        outlets = [
            {
                'name': 'Downtown Branch',
                'address': '123 Main Street, Downtown, City 12345',
                'phone': '+1 (555) 123-4567',
                'hours': 'Mon-Sun: 11:00 AM - 10:00 PM',
                'image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=600&h=400&fit=crop'
            },
            {
                'name': 'Mall Location',
                'address': '456 Shopping Mall, Second Floor, City 12345',
                'phone': '+1 (555) 234-5678',
                'hours': 'Mon-Sun: 10:00 AM - 9:00 PM',
                'image_url': 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&h=400&fit=crop'
            },
            {
                'name': 'Airport Branch',
                'address': '789 Airport Terminal, Gate 5, City 12345',
                'phone': '+1 (555) 345-6789',
                'hours': 'Mon-Sun: 6:00 AM - 11:00 PM',
                'image_url': 'https://images.unsplash.com/photo-1559339352-11d035aa65de?w=600&h=400&fit=crop'
            },
        ]

        for outlet_data in outlets:
            image_url = outlet_data.pop('image_url')
            image_obj = Image.objects.create(url=image_url)
            outlet_data['image'] = image_obj
            Outlet.objects.create(**outlet_data)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with initial data!'))

