# eSafety Backend API

Django REST Framework backend for the eSafety Incident Management Platform.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file from `.env.example`:
```bash
cp .env.example .env
```

4. Configure PostgreSQL database with PostGIS extension:
```sql
CREATE DATABASE esafety;
\c esafety
CREATE EXTENSION postgis;
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Project Structure

```
backend/
├── apps/
│   ├── users/          # User management & authentication
│   ├── incidents/      # Core incident models & APIs
│   ├── media/          # Media/evidence management
│   ├── response/       # Response coordination
│   ├── iot/            # IoT integration (RFID, CCTV, Sensors)
│   ├── verification/   # AI verification & human review
│   ├── notifications/  # Notifications & alerts
│   ├── analytics/      # Analytics & reporting
│   ├── blockchain/     # Blockchain integration
│   ├── config/         # Configuration & taxonomy
│   ├── workorders/     # Work orders & maintenance
│   └── audit/           # Audit logging
├── esafety/            # Django project settings
├── manage.py
└── requirements.txt
```

## API Documentation

API endpoints will be available at:
- Development: `http://localhost:8000/api/`
- Swagger UI: `http://localhost:8000/api/docs/` (when configured)

## Key Features

- **RESTful API** with Django REST Framework
- **JWT Authentication** for secure API access
- **PostGIS** for geospatial queries
- **WebSocket** support for real-time updates
- **Celery** for async task processing
- **Blockchain Integration** with Base network
- **IoT Integration** for RFID, CCTV, and sensors

## Testing

```bash
pytest
```

## License

Copyright (c) MUIA LTD

