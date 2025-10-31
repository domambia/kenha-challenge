# eSafety Technical Guide

## 1. Repository Layout

```
hep-project/
├─ docs/
│  ├─ eSafety-White-Paper.md
│  ├─ eSafety-PRD.md
│  └─ esafety_technicall_guide.md
└─ kenha_challenge/
   ├─ backend/        # Django services
   ├─ client/         # Next.js admin console
   └─ mobile_app/     # Flutter citizen app
```

All services share a common `.env.example` pattern and leverage Docker for local orchestration. Git hooks (Husky for JS, pre-commit for Python, custom script for Flutter) enforce linting prior to commits.

---

## 2. Backend (Django)

### 2.1 Stack
- Python 3.12, Django 5, Django REST Framework
- PostgreSQL + PostGIS, Redis
- Celery + Redis for background jobs
- Channels (ASGI) for WebSockets
- `pyethers` or `web3.py` for Base blockchain integration

### 2.2 Local Setup
1. Copy env template:
   ```
   cp kenha_challenge/backend/.env.example kenha_challenge/backend/.env
   ```
2. Populate secrets: database DSN, Redis URI, SMTP creds, Base RPC URL, relayer key.
3. Install system dependencies: GDAL/GEOS for PostGIS, OpenCV libs for media processing.
4. Create Python environment:
   ```
   cd kenha_challenge/backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements/dev.txt
   ```
5. Run database migrations and seed reference data (`manage.py seed_reference_data`).
6. Start stack:
   ```
   docker compose up -d db redis
   python manage.py runserver 0.0.0.0:8000
   python -m celery -A config worker -l info
   python -m celery -A config beat -l info
   ```

### 2.3 Key Apps
- `incidents`: core models, geospatial queries, AI hooks, validation
- `media`: upload pipeline, virus scan, compression
- `blockchain`: Base transaction service, relayer integration, audit bridge
- `notifications`: SMS/email/push adapters
- `analytics`: ETL jobs, data warehouse connectors
- `accounts`: RBAC, OAuth/OIDC, reporter reputation scoring
- `iot_integration`: KeNHA system adapters (RFID, CCTV, sensors)
- `validation`: Multi-source incident validation service
- `timeseries`: Time-series data storage for sensor/RFID logs

### 2.4 API Surface
- REST endpoints for incident submission, evidence, assignments, responder status
- Admin GraphQL endpoint for analytics dashboards
- WebSocket channels for live queues and status updates
- gRPC or REST adapters for third-party integrations (CCTV, CAD)

### 2.5 Testing
- `pytest` + `pytest-django` for unit/integration tests
- `factory_boy` fixtures, `pytest-asyncio` for async testing
- Contract tests (schemathesis) for API stability
- Load tests with Locust; geospatial query benchmarks included in CI

### 2.6 Deployment
- Docker image built via GitHub Actions workflow
- Helm charts deploy to Kubernetes (AKS/EKS/GKE subject to client policy)
- Secrets managed through HashiCorp Vault or cloud KMS
- Observability: OpenTelemetry, Prometheus exporters, Grafana dashboards

---

## 3. Client (Next.js Admin)

### 3.1 Stack
- Next.js 14 (App Router, TypeScript)
- Tailwind CSS, Radix UI, Mapbox GL / Leaflet
- Redux Toolkit Query for API state
- Socket.IO client for real-time updates
- Jest, Testing Library, Playwright for QA

### 3.2 Setup
1. Environment:
   ```
   cp kenha_challenge/client/.env.example kenha_challenge/client/.env.local
   npm install
   npm run dev
   ```
2. Required variables: API base URL, WebSocket URL, map provider tokens, auth issuer, feature flags.

### 3.3 Architecture
- `app/` route structure with server actions for secure data fetching
- `features/` domain slices (incidents, responders, analytics, settings)
- `lib/` utilities (auth, i18n, formatting)
- `components/` shared UI blocks with design tokens
- Internationalization via `next-intl` (English, Swahili)

### 3.4 CI/CD
- Pre-commit Husky hooks: `eslint`, `prettier`, `tsc --noEmit`
- GitHub Actions pipeline: lint → unit tests → Playwright smoke → Docker build
- Deployment to Vercel for preview, Kubernetes ingress for production

### 3.5 Security & Compliance
- Enforced HTTPS, CSP headers, rate limiting via edge middleware
- JWT/OIDC integration with backend; refresh token rotation
- Role-based rendering guards and feature toggles
- Accessibility audits with axe-core; WCAG 2.1 AA checklists

---

## 4. Mobile App (Flutter)

### 4.1 Stack
- Flutter 3.x, Dart 3.x
- State management: Riverpod or Bloc (choose per sprint decision)
- Offline persistence: Hive / SQLite (floor)
- Networking: `dio` with interceptors, WebSockets for live updates
- Push: Firebase Cloud Messaging (Android/iOS)
- Native integrations: camera, geolocation, background fetch, audio recording

### 4.2 Setup
1. Install Flutter SDK and platform dependencies (Xcode, Android SDK).
2. Copy environment:
   ```
   cp kenha_challenge/mobile_app/.env.example kenha_challenge/mobile_app/.env
   ```
   Use `flutter_dotenv` or similar to expose config.
3. Fetch packages and run:
   ```
   cd kenha_challenge/mobile_app
   flutter pub get
   flutter run
   ```
4. Configure Firebase projects per environment; add `google-services.json` and `GoogleService-Info.plist`.

### 4.3 Project Structure
- `lib/features/<domain>/` for modular features (auth, report, history, messaging)
- `lib/services/` (api client, storage, notification, blockchain signing)
- `lib/widgets/` reusable UI components
- `assets/` for translations, icons, tutorials
- `test/` and `integration_test/` suites with `flutter_test` and `integration_test` framework

### 4.4 Core Flows

#### 4.4.1 Incident Reporting Flow (Primary Feature)
1. **GPS Location Capture:**
   - Request location permission on app launch
   - Automatic GPS coordinate capture (latitude/longitude)
   - Display location on map for user verification
   - Allow manual adjustment if location inaccurate
   - Capture GPS metadata: accuracy, altitude, timestamp

2. **Incident Type Selection:**
   - Road accident/collision
   - Road hazard (potholes, debris, obstructions)
   - Infrastructure vandalism (damaged signs, guardrails, graffiti)
   - Traffic violation
   - Emergency situation

3. **Photo & Video Capture:**
   - Integrated camera for immediate photo capture
   - Support for gallery selection
   - Video recording (up to 120 seconds)
   - Automatic GPS geotagging in media metadata
   - Compression and optimization before upload
   - Preview before submission

4. **Incident Details Entry:**
   - Description text input (mandatory, ≥20 characters)
   - Severity level selection
   - Additional metadata (weather, vehicles involved, etc.)
   - Timestamp confirmation

5. **Submission to Centralized Servers:**
   - Data transmission to Django backend
   - Offline queue if network unavailable
   - Upload progress indicator
   - Confirmation with incident ID
   - Automatic blockchain notarization (transparent to user)

6. **Status Tracking:**
   - Real-time status updates via push notifications
   - Incident timeline view
   - Responder location tracking (when authorized)
   - Resolution confirmation and feedback prompts

#### 4.4.2 Additional Flows
- Onboarding & identity verification (OTP, optional anonymous mode)
- Offline sync handler with conflict resolution
- Incident timeline and status updates (push + polling fallback)
- Feedback and rating module post-resolution

### 4.5 Quality Assurance
- Unit tests for logic and state containers
- Golden tests for UI snapshots
- Integration tests (report flow, offline sync) via `integration_test` + Firebase Test Lab
- Static analysis with `dart analyze`, formatting with `dart format`
- Detox-like E2E via `flutter_driver` successor or Maestro (if selected)

### 4.6 Packaging & Release
- Fastlane scripts for beta distribution (TestFlight, Play Console)
- Code signing managed through secure credential store
- Crash reporting via Sentry + Firebase Crashlytics
- Feature flags controlled by backend-configurable remote config

---

## 5. Cross-Cutting Concerns

### 5.1 Environment Management
- Profiles: `development`, `staging`, `production`
- Shared secrets stored in Vault; services retrieve via CI/CD or runtime injection
- Feature flag service (LaunchDarkly or custom) toggles AI, blockchain modules, incentives
- KeNHA integration credentials: API keys, MQTT broker endpoints, CCTV access tokens stored in Vault

### 5.2 Blockchain (Base)
- Account abstraction with sponsored transactions (Paymaster service) to ensure zero gas UX
- Smart contracts (Solidity) managed in separate repo/submodule; deployment scripts with Hardhat
- Backend relayer monitors mempool, retries with exponential backoff, logs receipts for auditing
- On-chain data limited to hashes and milestone markers; sensitive PII kept off-chain

### 5.6 KeNHA IoT Integration Layer

#### 5.6.1 Architecture Overview
The IoT integration layer bridges eSafety platform with existing KeNHA infrastructure. It consists of microservices handling protocol translation, data normalization, and real-time processing.

**Component Structure:**
```
kenha_challenge/backend/
├── iot_integration/
│   ├── adapters/
│   │   ├── rfid_adapter.py      # RFID reader integration
│   │   ├── cctv_adapter.py       # CCTV camera integration
│   │   ├── sensor_adapter.py     # Sensor data ingestion
│   │   └── protocol_converters.py # MQTT/CoAP/REST/gRPC handlers
│   ├── services/
│   │   ├── validation_service.py # Multi-source correlation engine
│   │   ├── stream_processor.py    # Real-time data processing
│   │   └── data_normalizer.py    # Standardize data formats
│   ├── models/
│   │   ├── rfid_log.py           # RFID reading models
│   │   ├── sensor_data.py        # Sensor reading models
│   │   └── camera_feed.py        # CCTV feed metadata
│   └── tasks.py                  # Celery tasks for async processing
```

#### 5.6.2 RFID Integration Implementation

**Dependencies:**
```python
# requirements/dev.txt additions
paho-mqtt>=1.6.1          # MQTT client for RFID data streams
timescaledb>=0.15.0       # PostgreSQL extension for time-series
psycopg2-binary>=2.9.9    # PostgreSQL adapter
```

**RFID Adapter Service:**
```python
# iot_integration/adapters/rfid_adapter.py structure
class RFIDAdapter:
    - connect_to_mqtt_broker()
    - subscribe_to_rfid_streams()
    - normalize_vehicle_data()
    - store_rfid_reading()
    - query_vehicle_history()
    - hash_vehicle_identifier()  # Privacy-preserving
```

**Database Schema (TimescaleDB):**
```sql
-- RFID readings hypertable for time-series storage
CREATE TABLE rfid_readings (
    id BIGSERIAL,
    reader_id VARCHAR(50),
    vehicle_tag VARCHAR(255),  -- Hashed after ingestion
    timestamp TIMESTAMPTZ NOT NULL,
    location GEOMETRY(POINT, 4326),
    lane_number INTEGER,
    vehicle_class VARCHAR(20)
);
SELECT create_hypertable('rfid_readings', 'timestamp');
CREATE INDEX idx_location ON rfid_readings USING GIST(location);
```

**Integration Setup:**
1. Configure MQTT broker connection in `.env`:
   ```
   KENHA_RFID_MQTT_BROKER=mqtt.kenha.go.ke
   KENHA_RFID_MQTT_PORT=1883
   KENHA_RFID_MQTT_USERNAME=<vault_retrieved>
   KENHA_RFID_MQTT_PASSWORD=<vault_retrieved>
   KENHA_RFID_MQTT_TOPIC=kenha/rfid/readings/#
   ```
2. Start RFID ingestion worker:
   ```bash
   python manage.py run_iot_worker rfid
   ```

#### 5.6.3 CCTV Integration Implementation

**Dependencies:**
```python
# requirements/dev.txt additions
opencv-python>=4.8.0      # Video processing
ffmpeg-python>=0.2.0      # Video encoding/decoding
onvif-zeep>=0.2.12        # ONVIF protocol support
ultralytics>=8.0.0        # YOLOv8 for object detection
redis>=5.0.0              # Caching video metadata
```

**CCTV Adapter Service:**
```python
# iot_integration/adapters/cctv_adapter.py structure
class CCTVAdapter:
    - discover_cameras_in_radius()  # Query camera DB by GPS
    - retrieve_video_feed()          # RTSP/ONVIF stream
    - extract_incident_clip()       # ±5min window
    - analyze_with_ai()            # YOLOv8 inference
    - blur_privacy_elements()       # Face/plate redaction
    - store_validation_clip()      # S3/MinIO with blockchain hash
```

**Camera Database Model:**
```python
# iot_integration/models/camera_feed.py
class Camera:
    camera_id = models.CharField(max_length=100, unique=True)
    location = models.PointField(srid=4326)  # PostGIS
    protocol = models.CharField(choices=[('ONVIF', 'ONVIF'), ('RTSP', 'RTSP')])
    endpoint = models.URLField()
    coverage_radius_m = models.IntegerField(default=500)
    stream_url = models.URLField()
    is_active = models.BooleanField(default=True)
```

**AI Video Analysis Pipeline:**
```python
# iot_integration/services/video_analyzer.py
class VideoIncidentAnalyzer:
    def detect_incident(self, video_clip_path):
        # YOLOv8 model inference
        # Returns: incident_type, confidence, bounding_boxes
        pass
    
    def classify_severity(self, detection_results):
        # Rule-based + ML severity assessment
        pass
```

**Integration Setup:**
1. Populate camera database from KeNHA CCTV management system:
   ```bash
   python manage.py import_kenha_cameras --api-endpoint https://cctv.kenha.go.ke/api
   ```
2. Configure video storage in `.env`:
   ```
   CCTV_STORAGE_BACKEND=s3  # or minio for local dev
   CCTV_S3_BUCKET=esafety-cctv-clips
   CCTV_CLIP_RETENTION_DAYS=30
   ```

#### 5.6.4 Sensor Integration Implementation

**Dependencies:**
```python
# requirements/dev.txt additions
aiocoap>=1.0.0            # CoAP protocol support (async)
influxdb-client>=1.36.0  # Alternative: InfluxDB for sensor data
numpy>=1.24.0             # Data processing
pandas>=2.0.0             # Time-series analysis
```

**Sensor Adapter Service:**
```python
# iot_integration/adapters/sensor_adapter.py structure
class SensorAdapter:
    - connect_to_sensor_network()   # MQTT/CoAP subscription
    - normalize_sensor_data()       # Standardize formats
    - detect_anomalies()            # Real-time anomaly detection
    - correlate_with_incidents()    # Match sensor data to reports
    - store_time_series()           # TimescaleDB/InfluxDB
```

**Sensor Data Model:**
```python
# iot_integration/models/sensor_data.py
class SensorReading:
    sensor_id = models.CharField(max_length=100)
    sensor_type = models.CharField(choices=[
        ('TRAFFIC_FLOW', 'Traffic Flow'),
        ('WEATHER', 'Weather'),
        ('ROAD_SURFACE', 'Road Surface'),
        ('AIR_QUALITY', 'Air Quality'),
        ('VIBRATION', 'Vibration')
    ])
    timestamp = models.DateTimeField()
    location = models.PointField(srid=4326)
    readings = models.JSONField()  # Flexible schema per sensor type
```

**Anomaly Detection:**
```python
# iot_integration/services/anomaly_detector.py
class SensorAnomalyDetector:
    def detect_traffic_anomaly(self, location, time_window):
        # Compare current flow vs. historical patterns
        # Flag significant deviations
        pass
    
    def detect_weather_hazard(self, sensor_readings):
        # Low visibility, precipitation, temperature extremes
        pass
```

#### 5.6.5 Multi-Source Validation Service

**Validation Algorithm:**
```python
# iot_integration/services/validation_service.py
class IncidentValidationService:
    def validate_incident(self, incident):
        """
        Multi-source correlation engine:
        1. Query RFID logs for vehicle presence
        2. Retrieve CCTV feeds for visual confirmation
        3. Correlate with sensor anomalies
        4. Calculate confidence score (0-100%)
        """
        rfid_confidence = self._check_rfid_correlation(incident)
        cctv_confidence = self._analyze_cctv_feeds(incident)
        sensor_confidence = self._correlate_sensors(incident)
        
        # Weighted confidence score
        total_confidence = (
            rfid_confidence * 0.3 +
            cctv_confidence * 0.5 +
            sensor_confidence * 0.2
        )
        
        return {
            'confidence_score': total_confidence,
            'rfid_match': rfid_confidence > 50,
            'cctv_verified': cctv_confidence > 60,
            'sensor_correlation': sensor_confidence > 40,
            'validation_evidence': {...}
        }
```

**Confidence Scoring Logic:**
- **RFID Correlation (30% weight):** Vehicle present within ±2km and ±10min of incident
- **CCTV Verification (50% weight):** Visual confirmation of incident type and location
- **Sensor Correlation (20% weight):** Traffic flow anomalies, weather conditions match report

#### 5.6.6 Deployment Configuration

**Docker Compose Addition:**
```yaml
# docker-compose.yml
services:
  timescaledb:
    image: timescale/timescaledb:latest-pg15
    environment:
      POSTGRES_DB: esafety
      POSTGRES_USER: esafety_user
      POSTGRES_PASSWORD: ${TIMESCALE_PASSWORD}
    volumes:
      - timescale_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
  
  mqtt-broker:
    image: eclipse-mosquitto:2.0
    ports:
      - "1883:1883"
      - "9001:9001"
    volumes:
      - ./mosquitto.conf:/mosquitto/config/mosquitto.conf
```

**Environment Variables (.env.example additions):**
```
# KeNHA IoT Integration
KENHA_RFID_MQTT_BROKER=
KENHA_RFID_MQTT_PORT=1883
KENHA_RFID_MQTT_USERNAME=
KENHA_RFID_MQTT_PASSWORD=
KENHA_RFID_MQTT_TOPIC=kenha/rfid/readings/#

KENHA_CCTV_API_BASE_URL=
KENHA_CCTV_API_KEY=
KENHA_CCTV_RTSP_USERNAME=
KENHA_CCTV_RTSP_PASSWORD=

KENHA_SENSOR_MQTT_BROKER=
KENHA_SENSOR_MQTT_TOPIC=kenha/sensors/#
KENHA_SENSOR_COAP_ENDPOINT=

# Time-series Database
TIMESCALE_ENABLED=true
INFLUXDB_URL=  # Optional alternative

# Video Storage
CCTV_STORAGE_BACKEND=s3
CCTV_S3_BUCKET=
CCTV_CLIP_RETENTION_DAYS=30
```

#### 5.6.7 Testing IoT Integration

**Unit Tests:**
```python
# tests/iot_integration/test_rfid_adapter.py
@pytest.mark.asyncio
async def test_rfid_vehicle_correlation():
    # Mock RFID reading
    # Verify correlation logic
    pass

# tests/iot_integration/test_cctv_validation.py
def test_cctv_incident_detection():
    # Mock video clip
    # Verify AI detection
    pass
```

**Integration Tests:**
- Use test MQTT broker for RFID simulation
- Mock CCTV feeds with sample videos
- Generate synthetic sensor data for testing

### 5.3 Observability
- Centralized logging: backend (Structlog/ELK), frontend (Sentry), mobile (Sentry + Crashlytics)
- Metrics: Prometheus scraping, Grafana dashboards for SLA compliance, AI performance, Base transaction health
- Alerting: PagerDuty/OPSGenie hooks for P1 incidents, relayer failures, queue backlogs

### 5.4 Data Lifecycle
- Retention policy: raw media 5 years, metadata 10 years, anonymized aggregates indefinite
- GDPR/Kenya Data Protection Act compliance with subject access APIs handled by backend admin panel
- Backups: daily snapshots (Postgres, Redis persistence, object storage versioning)
- Disaster recovery playbook stored in `docs/operations/dr_plan.md` (to be created)

### 5.5 Security
- Regular pentests; dependency scanning (Dependabot + Snyk)
- Secrets rotation schedule (90 days)
- MFA enforced for admin accounts; device attestation for mobile responder logins
- Zero-trust network segmentation between services and data stores

---

## 6. Delivery Workflow

1. **Backlog Grooming:** PRD items decomposed into tickets (Jira/Linear) with acceptance criteria.  
2. **Branching:** `main` protected; feature branches from `develop`. Conventional commits, lint-staged checks.  
3. **Code Review:** Required approvals, automated test suite gating.  
4. **CI Pipeline:** Runs unit/integration tests, coverage, security scans, contract tests, Docker builds.  
5. **Staging Deploy:** Automated; smoke tests across web and mobile (via browserstack/firebase).  
6. **Release:** Production deployment with canary strategy; mobile releases follow staged rollout.  
7. **Post-release Monitoring:** 48-hour heightened observability; incident review if KPIs degrade.  

---

## 7. System Architecture Diagrams

### 7.1 High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           eSafety Platform Architecture                     │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐               │
│  │  Flutter     │    │  Next.js     │    │  API         │               │
│  │  Mobile App  │───▶│  Admin Web   │───▶│  Gateway     │               │
│  │              │    │              │    │  (Kong/Envoy)│               │
│  └──────────────┘    └──────────────┘    └──────┬───────┘               │
│                                                  │                         │
│  ┌──────────────────────────────────────────────▼──────────────────────┐  │
│  │                    Django Backend Core Services                       │  │
│  ├──────────────┬──────────────┬──────────────┬───────────────────────┤  │
│  │  Incidents   │  Accounts    │  Media       │  Notifications        │  │
│  │  Service     │  Service     │  Service     │  Service              │  │
│  └──────┬───────┴──────┬───────┴──────┬───────┴──────────┬────────────┘  │
│         │              │              │                   │                │
│  ┌──────▼──────────────▼──────────────▼───────────────────▼────────────┐  │
│  │              IoT Integration Layer (Django Microservices)           │  │
│  ├──────────────────┬──────────────────┬──────────────────────────────┤  │
│  │  RFID Adapter    │  CCTV Adapter    │  Sensor Adapter             │  │
│  │  Service         │  Service         │  Service                     │  │
│  └──────────────────┴──────────────────┴──────────────────────────────┘  │
│         │              │              │                                   │
│         │              │              │                                   │
│  ┌──────▼──────────────▼──────────────▼───────────────────────────────┐  │
│  │              Validation Service (Multi-source Correlation)           │  │
│  └──────────────────────────────┬──────────────────────────────────────┘  │
│                                 │                                         │
│  ┌──────────────────────────────▼──────────────────────────────────────┐  │
│  │                    Data Storage Layer                                 │  │
│  ├──────────────────┬──────────────────┬───────────────────────────────┤  │
│  │  PostgreSQL      │  TimescaleDB    │  Redis Cache                  │  │
│  │  + PostGIS        │  (Time-series) │  (Sessions/Queue)             │  │
│  └──────────────────┴──────────────────┴───────────────────────────────┘  │
│         │                                 │                                │
│         │                                 │                                │
│  ┌──────▼─────────────────────────────────▼─────────────────────────────┐  │
│  │  Object Storage (S3/MinIO) │  AI Services (FastAPI) │  Blockchain   │  │
│  │  - Media files              │  - Computer Vision    │  - Base L2    │  │
│  │  - CCTV clips               │  - NLP                │  - Relayer    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

External Systems:
  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
  │  KeNHA      │    │  KeNHA      │    │  KeNHA      │
  │  RFID       │───▶│  CCTV       │───▶│  Sensors    │
  │  Network    │    │  Network    │    │  Network    │
  └─────────────┘    └─────────────┘    └─────────────┘
```

### 7.2 Data Flow: Incident Validation Process

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    Incident Validation Data Flow                            │
└────────────────────────────────────────────────────────────────────────────┘

1. Citizen Reports Incident
   │
   ├─▶ Django API receives incident (GPS, timestamp, media, description)
   │
   ├─▶ Incident stored in PostgreSQL, queued for validation
   │
   └─▶ Validation Service triggered (Celery task)
       │
       ├─────────────────────────────────────────────────────────────────┐
       │                                                                │
       │  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐│
       │  │  RFID Correlation│  │  CCTV Retrieval │  │  Sensor       ││
       │  │                  │  │                 │  │  Correlation  ││
       │  │ Query RFID logs  │  │ Find cameras   │  │  Match sensor ││
       │  │ ±2km, ±10min     │  │ within 500m    │  │  anomalies    ││
       │  │                  │  │                 │  │  at location  ││
       │  │ Check vehicle    │  │ Retrieve video │  │               ││
       │  │ presence         │  │ ±5min window   │  │  Traffic flow ││
       │  │                  │  │                 │  │  Weather      ││
       │  │ Confidence: 30% │  │ AI analysis     │  │  Road surface ││
       │  │                  │  │                 │  │               ││
       │  │ Result: Match    │  │ Confidence: 50%│  │ Confidence:20%││
       │  │                  │  │                 │  │               ││
       │  │ Result: Verified │  │ Result: Detected│  │ Result: Match ││
       │  └──────────────────┘  └──────────────────┘  └───────────────┘│
       │                                                                │
       └───────────────────┬────────────────────────────────────────────┘
                           │
                           ▼
        ┌─────────────────────────────────────────────┐
        │      Multi-Source Confidence Calculation     │
        │                                                │
        │  Total Confidence = (RFID × 0.3) +            │
        │                    (CCTV × 0.5) +             │
        │                    (Sensor × 0.2)             │
        │                                                │
        │  Example: (70% × 0.3) + (85% × 0.5) +        │
        │           (60% × 0.2) = 76.5%                │
        └────────────────────┬──────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │      Validation Result                       │
        │                                                │
        │  • Confidence Score: 76.5%                    │
        │  • RFID Match: ✓ Vehicle present              │
        │  • CCTV Verified: ✓ Accident detected         │
        │  • Sensor Correlation: ✓ Traffic anomaly     │
        │  • Validation Status: VERIFIED                │
        └────────────────────┬──────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │      Update Incident Record                  │
        │                                                │
        │  • Set verification_status = VERIFIED        │
        │  • Store validation_confidence = 76.5%       │
        │  • Link CCTV clip hash to incident           │
        │  • Link RFID correlation data                │
        │  • Link sensor anomaly records               │
        │  • Hash incident + validation → Blockchain   │
        └────────────────────┬──────────────────────────┘
                             │
                             ▼
        ┌─────────────────────────────────────────────┐
        │      Dispatcher Queue                        │
        │                                                │
        │  • Incident appears in queue with high       │
        │    confidence score                          │
        │  • Dispatcher can view:                     │
        │    - Citizen report + media                  │
        │    - CCTV validation clip                    │
        │    - RFID correlation data                   │
        │    - Sensor data at incident time            │
        └─────────────────────────────────────────────┘
```

### 7.3 Deployment Architecture (Kubernetes)

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         Kubernetes Cluster                                  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Namespace: esafety-production                                              │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Ingress Controller (NGINX/Traefik)                                  │  │
│  │  - TLS termination                                                    │  │
│  │  - Rate limiting                                                      │  │
│  │  - Load balancing                                                     │  │
│  └──────────────────┬───────────────────────────────────────────────────┘  │
│                      │                                                        │
│  ┌───────────────────▼───────────────────────────────────────────────────┐  │
│  │  API Gateway (Kong/Envoy)                                              │  │
│  │  - Authentication                                                      │  │
│  │  - Request routing                                                    │  │
│  └───────────────────┬───────────────────────────────────────────────────┘  │
│                      │                                                        │
│  ┌───────────────────▼───────────────────────────────────────────────────┐  │
│  │  Backend Services (Django)                                             │  │
│  │  Replicas: 5                                                           │  │
│  │  Resources: 2 CPU, 4GB RAM per pod                                     │  │
│  │  Auto-scaling: 5-20 pods based on CPU/memory                           │  │
│  └───────────────────┬───────────────────────────────────────────────────┘  │
│                      │                                                        │
│  ┌───────────────────▼───────────────────────────────────────────────────┐  │
│  │  IoT Integration Services                                               │  │
│  │  - RFID Adapter (2 replicas)                                            │  │
│  │  - CCTV Adapter (3 replicas)                                           │  │
│  │  - Sensor Adapter (2 replicas)                                         │  │
│  │  - Validation Service (3 replicas)                                    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  Celery Workers                                                       │  │
│  │  - Incident processing workers (10 replicas)                         │  │
│  │  - IoT data ingestion workers (5 replicas)                           │  │
│  │  - AI inference workers (GPU-enabled, 3 replicas)                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  StatefulSets                                                        │  │
│  │  - PostgreSQL + PostGIS (Primary + 2 Replicas)                      │  │
│  │  - TimescaleDB (2 replicas with streaming replication)             │  │
│  │  - Redis Cluster (3 masters + 3 replicas)                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  External Services                                                    │  │
│  │  - Object Storage (S3/MinIO)                                         │  │
│  │  - AI Services (FastAPI microservices)                               │  │
│  │  - Blockchain Relayer Service                                        │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────────┘

Network Policies:
  - IoT integration services isolated in separate namespace
  - KeNHA system connections via VPN/private network
  - Database access restricted to backend services only
```

## 8. Project Setup: Initialization Guide

### 8.1 Prerequisites

**System Requirements:**
- Python 3.12+
- PostgreSQL 15+ with PostGIS extension
- Redis 7+
- Docker & Docker Compose
- Node.js 20+ (for frontend)
- Flutter 3.x (for mobile)

**KeNHA Integration Requirements:**
- Network access to KeNHA systems (VPN or private network)
- API credentials for KeNHA systems (RFID, CCTV, sensors)
- MQTT broker endpoint access (if applicable)

### 8.2 Initial Backend Setup

1. **Clone and Initialize:**
   ```bash
   cd kenha_challenge/backend
   python -m venv .venv
   source .venv/bin/activate  # or `.\venv\Scripts\activate` on Windows
   pip install -r requirements/dev.txt
   ```

2. **Database Setup:**
   ```bash
   # Start PostgreSQL with PostGIS
   docker compose up -d db timescaledb redis
   
   # Create database extensions
   python manage.py migrate
   python manage.py enable_timescaledb  # For time-series data
   
   # Seed initial data
   python manage.py seed_reference_data
   ```

3. **Configure KeNHA Integration:**
   ```bash
   # Populate camera database
   python manage.py import_kenha_cameras --api-endpoint $KENHA_CCTV_API
   
   # Test RFID connection
   python manage.py test_rfid_connection
   
   # Verify sensor data ingestion
   python manage.py test_sensor_ingestion
   ```

4. **Start Services:**
   ```bash
   # Django development server
   python manage.py runserver 0.0.0.0:8000
   
   # Celery workers (in separate terminals)
   celery -A config worker -l info -Q incidents,iot,ai_inference
   celery -A config beat -l info
   
   # IoT integration workers
   python manage.py run_iot_worker rfid
   python manage.py run_iot_worker cctv
   python manage.py run_iot_worker sensors
   ```

### 8.3 Frontend Setup

```bash
cd kenha_challenge/client
npm install
cp .env.example .env.local
# Edit .env.local with API endpoints
npm run dev
```

### 8.4 Mobile App Setup

```bash
cd kenha_challenge/mobile_app
flutter pub get
cp .env.example .env
# Configure Firebase and API endpoints
flutter run
```

## 9. References & Next Steps

- Product context: `docs/eSafety-PRD.md`, `eSafety-White-Paper.md`
- Smart contract specs: pending architecture workshop with Base ecosystem
- KeNHA integration documentation: `docs/kenha_integration.md` (to be created)
- Next actions:
  1. Populate service-specific `.env.example` files with agreed variable list.
  2. Scaffold initial Django/Next.js/Flutter codebases within `kenha_challenge/`.
  3. Establish CI/CD templates aligned with this guide.
  4. Create KeNHA integration test environment with mock services.
  5. Develop IoT adapter services for RFID, CCTV, and sensor integration.

