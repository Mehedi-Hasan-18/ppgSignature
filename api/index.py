import os
import sys
import django

# Add parent directory to path so Django settings can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signature_restaurant.settings')
django.setup()

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()