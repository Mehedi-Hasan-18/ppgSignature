# Signature Restaurant - Backend

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```
   - Update `SECRET_KEY` with a secure Django secret key

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Seed initial data:
```bash
python manage.py seed_data
```

7. Run development server:
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

- `GET /api/menu/` - List all menu items
- `GET /api/reviews/` - List all reviews
- `GET /api/outlets/` - List all outlets
- `GET /admin/` - Django admin panel

