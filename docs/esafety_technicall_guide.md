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
- Onboarding & identity verification (OTP, optional anonymous mode)
- Incident reporting wizard with camera/gallery, audio notes, map preview
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

### 5.2 Blockchain (Base)
- Account abstraction with sponsored transactions (Paymaster service) to ensure zero gas UX
- Smart contracts (Solidity) managed in separate repo/submodule; deployment scripts with Hardhat
- Backend relayer monitors mempool, retries with exponential backoff, logs receipts for auditing
- On-chain data limited to hashes and milestone markers; sensitive PII kept off-chain

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

## 7. References & Next Steps

- Product context: `docs/eSafety-PRD.md`, `eSafety-White-Paper.md`
- Smart contract specs: pending architecture workshop with Base ecosystem
- Next actions:
  1. Populate service-specific `.env.example` files with agreed variable list.
  2. Scaffold initial Django/Next.js/Flutter codebases within `kenha_challenge/`.
  3. Establish CI/CD templates aligned with this guide.

