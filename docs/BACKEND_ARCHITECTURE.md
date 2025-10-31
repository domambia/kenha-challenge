# eSafety Backend Architecture - Models, Routes & Features

## Table of Contents
1. [Database Models](#database-models)
2. [API Routes/Endpoints](#api-routesendpoints)
3. [Features & Functionality](#features--functionality)

---

## Database Models

### Core Models

#### 1. **User Models**
- **User** (extends Django AbstractUser)
  - Fields: email, phone, first_name, last_name, is_active, date_joined
  - Roles: SuperAdmin, SystemAdmin, TMC Operator, Dispatcher, FieldInspector, MaintenanceCrew, Police, EMS, FireRescue, Towing, Analyst, PolicyAnalyst, Support, QA Reviewer, RoadUser (Anonymous/Registered)
  - Reputation score, verification status, MFA enabled, last_login
  - Blockchain wallet address (optional for registered users)

- **UserProfile**
  - user (OneToOne), profile_picture, department, organization, badge_number, equipment_assigned
  - Location preferences, notification preferences, language (en/sw)

- **UserReputation**
  - user (ForeignKey), accuracy_score, report_count, verified_reports, false_reports
  - spam_count, last_reputation_update, blockchain_hash_reference

#### 2. **Incident Models**
- **Incident**
  - Fields: incident_id (unique), incident_type, severity (P1/P2/P3/P4), status (pending/verified/assigned/in_progress/resolved/closed), description (≥20 chars), timestamp, reporter (FK to User, nullable for anonymous), is_anonymous
  - Location: GPS coordinates (PointField PostGIS), road_classification, road_name, nearest_milestone
  - Metadata: weather, lane_count, vehicles_involved_count, has_injuries, infrastructure_damage_tags
  - Verification: ai_confidence_score (0-100), verification_status (pending/verified/false), verified_by (FK), verified_at
  - SLA: severity_level, sla_start_time, sla_target_time, sla_breach_time, escalation_level
  - Blockchain: incident_hash, blockchain_tx_hash, blockchain_timestamp, blockchain_block_number
  - Duplicate detection: parent_incident (self-referential FK for merged duplicates), is_duplicate
  - Created/Updated timestamps

- **IncidentType**
  - name, category (accident/hazard/infrastructure/other), severity_template, default_sla_minutes
  - description, icon

- **IncidentSeverity**
  - level (P1/P2/P3/P4), name, description, response_time_target_minutes, escalation_time_minutes
  - color_code, priority_score

#### 3. **Evidence/Media Models**
- **MediaAsset**
  - incident (ForeignKey), uploader (FK to User), asset_type (photo/video/audio), file_path (S3/storage URL)
  - file_hash (SHA256), file_size, mime_type, thumbnail_path
  - metadata: original_filename, compression_applied, exif_scrubbed, geotag_removed
  - privacy: faces_redacted, license_plates_redacted, redaction_config
  - blockchain: blockchain_hash, blockchain_tx_hash
  - virus_scan_status, virus_scan_result
  - created_at, updated_at

- **EvidenceTimeline**
  - incident (ForeignKey), media_asset (FK), actor (FK to User), action_type (upload/verify/update/delete)
  - timestamp, description, blockchain_reference

#### 4. **Response Coordination Models**
- **IncidentAssignment**
  - incident (ForeignKey), assigned_to (FK to User), assigned_by (FK to User dispatcher)
  - assignment_type (primary/backup/specialist), status (pending/accepted/rejected/in_progress/completed)
  - assigned_at, accepted_at, completed_at, notes
  - estimated_arrival_time, actual_arrival_time (geofenced detection)

- **ResponderLocation**
  - responder (FK to User), location (PointField), timestamp, accuracy, speed, heading
  - is_active, device_id

- **ResponseMilestone**
  - incident (ForeignKey), responder (FK), milestone_type (dispatched/en_route/on_scene/transporting/cleared)
  - timestamp, location (PointField), notes, media_attachments (JSON)
  - blockchain: milestone_hash, blockchain_tx_hash

- **ResponderChecklist**
  - incident_type (FK), checklist_items (JSON), responder_role (FK)
  - is_required, order

#### 5. **IoT Integration Models**

- **RFIDReader**
  - reader_id, location (PointField), installation_date, status (active/inactive/maintenance)
  - metadata: manufacturer, model, api_endpoint, mqtt_topic

- **RFIDLog**
  - reader (FK), vehicle_tag (hashed), vehicle_registration (hashed for privacy), timestamp
  - direction, lane, speed, vehicle_type
  - blockchain_hash (for audit trail)

- **CCTVCamera**
  - camera_id, location (PointField), installation_date, status, camera_type
  - protocol (RTSP/ONVIF/proprietary), api_endpoint, rtsp_url, onvif_url
  - coverage_radius_meters, metadata

- **CCTVFeed**
  - camera (FK), incident (FK, nullable), start_time, end_time, video_file_path
  - ai_analysis_result (JSON), incident_detected (boolean), confidence_score
  - manual_review_status, reviewed_by (FK), reviewed_at
  - blockchain_hash, retention_until

- **Sensor**
  - sensor_id, location (PointField), sensor_type (traffic_flow/weather/road_surface/air_quality/vibration)
  - manufacturer, model, installation_date, status, api_endpoint, mqtt_topic
  - metadata (JSON)

- **SensorReading**
  - sensor (FK), timestamp, reading_type, value (JSON - can store different types of readings)
  - unit, quality_score, anomaly_detected (boolean)
  - blockchain_hash (for critical readings)

- **IncidentValidation**
  - incident (FK), validation_source (citizen_report/rfid/cctv/sensor/ai)
  - confidence_score (0-100), validation_status (pending/confirmed/contradicted/inconclusive)
  - source_data (JSON), correlation_details (JSON)
  - validated_at, validated_by (FK, nullable for auto-validation)

#### 6. **Verification & AI Models**
- **AIVerificationResult**
  - incident (FK), model_version, classification_result (accident/hazard/obstruction/false)
  - confidence_score, duplicate_detection_score, credibility_score
  - processing_time, model_metadata (JSON)
  - created_at

- **HumanReview**
  - incident (FK), reviewer (FK to User), review_type (verification/qa/audit)
  - review_status (approved/rejected/flagged), review_notes
  - reviewed_at, review_duration_seconds

#### 7. **SLA & Escalation Models**
- **SLAConfiguration**
  - incident_severity (FK), incident_type (FK, nullable), target_response_time_minutes
  - target_resolution_time_minutes, escalation_rules (JSON)
  - is_active

- **SLAViolation**
  - incident (FK), sla_config (FK), violation_type (response_time/resolution_time)
  - violated_at, target_time, actual_time, breach_minutes
  - escalation_level, escalated_to (FK), resolved_at

- **EscalationRule**
  - name, trigger_condition (JSON), severity_level, escalation_path (JSON)
  - is_active, priority

#### 8. **Blockchain Models**
- **BlockchainTransaction**
  - transaction_type (incident_notarization/milestone/evidence/role_registry/incentive)
  - entity_type (incident/media/user), entity_id
  - transaction_hash, block_number, block_timestamp
  - gas_used, gas_price, relayer_address, from_address, to_address (contract)
  - status (pending/confirmed/failed), confirmation_count
  - created_at, confirmed_at

- **BlockchainContract**
  - contract_name, contract_address, contract_abi (JSON), network (base_mainnet/base_sepolia)
  - version, deployed_at, is_active

#### 9. **Notification Models**
- **NotificationTemplate**
  - name, notification_type (submission_receipt/dispatch_assignment/eta_update/resolution/escalation)
  - channel (push/sms/email/ussd), subject, body_template, variables (JSON)
  - is_active

- **Notification**
  - recipient (FK to User), template (FK), incident (FK, nullable)
  - channel, status (pending/sent/failed), sent_at, delivered_at
  - content (rendered template), error_message
  - device_token (for push), phone_number, email_address

- **BroadcastAlert**
  - alert_type (major_incident/road_closure/weather_warning), title, message
  - geofence (PolygonField), start_time, end_time, priority
  - channels (JSON array), created_by (FK), is_active
  - sent_count, delivered_count

#### 10. **Analytics & Reporting Models**
- **IncidentAnalytics**
  - date, incident_type, severity, region, total_count
  - avg_response_time, avg_resolution_time, sla_compliance_rate
  - ai_accuracy_rate, false_positive_rate
  - aggregated_data (JSON)

- **ReporterEngagement**
  - user (FK), period_start, period_end
  - reports_submitted, reports_verified, reputation_score_change
  - incentives_earned (JSON)

- **ResponderUtilization**
  - responder (FK), period_start, period_end
  - incidents_assigned, incidents_completed, avg_response_time
  - utilization_rate, availability_hours

- **PredictiveModel**
  - model_name, model_type (hazard_forecast/maintenance_planning), version
  - model_file_path, training_data_hash, accuracy_metrics (JSON)
  - deployed_at, is_active

- **PredictiveResult**
  - model (FK), predicted_date, location (PointField), prediction_type
  - risk_score, confidence, factors (JSON), created_at

#### 11. **Configuration & Taxonomy Models**
- **RoadNetwork**
  - road_id, road_name, road_classification, start_point (PointField), end_point (PointField)
  - geometry (LineString), length_km, jurisdiction, maintenance_organization
  - metadata (JSON)

- **IncidentCategory**
  - name, parent_category (self-referential, nullable), description
  - icon, color, default_severity (FK), is_active
  - metadata_fields_required (JSON)

- **Taxonomy**
  - taxonomy_type (incident_category/severity/road_classification), name, value
  - parent (FK, nullable), order, is_active, metadata (JSON)

- **SystemConfiguration**
  - key, value, value_type (string/integer/boolean/json), category
  - description, is_editable, requires_restart

- **IntegrationConfiguration**
  - integration_type (rfid/cctv/sensor/mapping/sms/email/blockchain), name
  - configuration (JSON - API keys, endpoints, credentials encrypted), is_active
  - last_sync_at, sync_status, error_message

#### 12. **Communication Models**
- **IncidentComment**
  - incident (FK), user (FK), comment_text, comment_type (internal/public)
  - parent_comment (self-referential FK for threading), is_edited, edited_at
  - created_at, updated_at

- **IncidentMessage**
  - incident (FK), sender (FK), recipient (FK, nullable), message_text
  - message_type (chat/follow_up/request), is_read, read_at
  - created_at

#### 13. **Workflow & Maintenance Models**
- **WorkOrder**
  - incident (FK, nullable - can be standalone), work_type (inspection/repair/maintenance)
  - assigned_to (FK), assigned_by (FK), status, priority
  - description, location (PointField), estimated_duration, actual_duration
  - started_at, completed_at, completion_notes, media_attachments (JSON)

- **InfrastructureInspection**
  - work_order (FK), inspector (FK), inspection_date, inspection_type
  - damage_assessment (JSON), repair_needed (boolean), priority
  - photos (JSON), inspection_report, blockchain_hash
  - created_at

#### 14. **Audit & Compliance Models**
- **AuditLog**
  - user (FK, nullable), action_type, entity_type, entity_id
  - action_details (JSON), ip_address, user_agent
  - timestamp, blockchain_hash (for critical actions)

- **DataRetentionPolicy**
  - entity_type, retention_period_days, anonymization_rules (JSON)
  - is_active, last_cleanup_at

#### 15. **Incentive Models**
- **IncentivePool**
  - pool_name, total_amount, allocated_amount, remaining_amount
  - pool_type (reputation/quality/engagement), blockchain_contract_address
  - metadata (JSON)

- **IncentiveTransaction**
  - user (FK), incentive_pool (FK), amount, transaction_type (earned/redeemed)
  - reason, incident (FK, nullable), blockchain_tx_hash
  - created_at

---

## API Routes/Endpoints

### Authentication & Authorization
- `POST /api/auth/register/` - User registration (phone/email + OTP)
- `POST /api/auth/login/` - Login (email/phone + password/OTP)
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/verify-otp/` - Verify OTP for registration/login
- `POST /api/auth/resend-otp/` - Resend OTP
- `POST /api/auth/refresh/` - Refresh JWT token
- `POST /api/auth/mfa/enable/` - Enable MFA (for privileged users)
- `POST /api/auth/mfa/verify/` - Verify MFA token
- `GET /api/auth/me/` - Get current user profile
- `PUT /api/auth/me/` - Update current user profile
- `POST /api/auth/password/reset/` - Request password reset
- `POST /api/auth/password/reset/confirm/` - Confirm password reset

### Incidents
- `POST /api/incidents/` - Create incident (citizen report)
- `GET /api/incidents/` - List incidents (filtered by role, status, severity, location)
- `GET /api/incidents/{id}/` - Get incident details
- `PUT /api/incidents/{id}/` - Update incident (authorized roles)
- `PATCH /api/incidents/{id}/verify/` - Verify incident (dispatcher/QA)
- `PATCH /api/incidents/{id}/merge/` - Merge duplicate incidents
- `PATCH /api/incidents/{id}/assign/` - Assign incident to responder
- `PATCH /api/incidents/{id}/status/` - Update incident status
- `PATCH /api/incidents/{id}/close/` - Close incident with resolution notes
- `POST /api/incidents/{id}/escalate/` - Escalate incident
- `GET /api/incidents/{id}/timeline/` - Get incident timeline
- `GET /api/incidents/{id}/validation/` - Get multi-source validation results
- `GET /api/incidents/map/` - Get incidents for map view (geospatial query)
- `GET /api/incidents/queue/` - Get dispatcher queue (filtered, sorted)
- `POST /api/incidents/{id}/comments/` - Add comment to incident
- `GET /api/incidents/{id}/comments/` - Get incident comments

### Media/Evidence
- `POST /api/incidents/{id}/media/` - Upload media (photo/video/audio)
- `GET /api/incidents/{id}/media/` - List incident media
- `GET /api/media/{id}/` - Get media asset details
- `DELETE /api/media/{id}/` - Delete media (with authorization)
- `GET /api/media/{id}/download/` - Download media file
- `GET /api/media/{id}/thumbnail/` - Get thumbnail
- `POST /api/media/{id}/redact/` - Request face/license plate redaction

### Response Coordination
- `GET /api/incidents/{id}/assignments/` - Get incident assignments
- `POST /api/incidents/{id}/assignments/` - Create assignment
- `PATCH /api/assignments/{id}/accept/` - Accept assignment (responder)
- `PATCH /api/assignments/{id}/reject/` - Reject assignment
- `PATCH /api/assignments/{id}/status/` - Update assignment status
- `POST /api/incidents/{id}/milestones/` - Create response milestone
- `GET /api/incidents/{id}/milestones/` - Get response milestones
- `POST /api/responders/location/` - Update responder location (real-time)
- `GET /api/responders/{id}/location/` - Get responder current location
- `GET /api/incidents/{id}/route/` - Get optimized route to incident

### IoT Integration
- `GET /api/rfid/readers/` - List RFID readers
- `GET /api/rfid/logs/` - Query RFID logs (with filters)
- `POST /api/rfid/validate/` - Validate incident with RFID data
- `GET /api/cctv/cameras/` - List CCTV cameras
- `GET /api/cctv/cameras/{id}/feed/` - Get camera feed URL
- `POST /api/cctv/incidents/{id}/retrieve/` - Retrieve CCTV footage for incident
- `GET /api/cctv/incidents/{id}/feeds/` - Get CCTV feeds for incident
- `GET /api/sensors/` - List sensors
- `GET /api/sensors/{id}/readings/` - Get sensor readings (time-series)
- `POST /api/sensors/correlate/` - Correlate sensor data with incident
- `POST /api/validation/incidents/{id}/` - Trigger multi-source validation

### Verification & AI
- `POST /api/ai/verify/` - Trigger AI verification for incident
- `GET /api/ai/incidents/{id}/results/` - Get AI verification results
- `GET /api/reviews/queue/` - Get human review queue
- `POST /api/reviews/` - Submit human review
- `PATCH /api/reviews/{id}/` - Update review

### Notifications
- `GET /api/notifications/` - Get user notifications
- `PATCH /api/notifications/{id}/read/` - Mark notification as read
- `POST /api/notifications/mark-all-read/` - Mark all as read
- `GET /api/notifications/settings/` - Get notification preferences
- `PUT /api/notifications/settings/` - Update notification preferences
- `POST /api/alerts/broadcast/` - Create broadcast alert (authorized roles)
- `GET /api/alerts/` - Get active alerts

### Analytics & Reporting
- `GET /api/analytics/dashboard/` - Get dashboard data (role-based)
- `GET /api/analytics/incidents/` - Incident analytics (heatmaps, trends)
- `GET /api/analytics/response-times/` - Response time analytics
- `GET /api/analytics/reporter-engagement/` - Reporter engagement metrics
- `GET /api/analytics/responder-utilization/` - Responder utilization metrics
- `GET /api/analytics/ai-accuracy/` - AI accuracy metrics
- `GET /api/analytics/hotspots/` - Incident hotspots (geospatial)
- `POST /api/reports/generate/` - Generate custom report
- `GET /api/reports/{id}/download/` - Download report (CSV/PDF)
- `GET /api/predictions/` - Get predictive model results

### User Management
- `GET /api/users/` - List users (admin)
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user (admin)
- `PATCH /api/users/{id}/role/` - Update user role (admin)
- `GET /api/users/{id}/reputation/` - Get user reputation
- `GET /api/users/{id}/incidents/` - Get user's reported incidents
- `GET /api/users/roles/` - List available roles

### Configuration & Taxonomy
- `GET /api/taxonomy/categories/` - Get incident categories
- `GET /api/taxonomy/severities/` - Get severity levels
- `GET /api/taxonomy/road-networks/` - Get road networks
- `GET /api/config/system/` - Get system configuration
- `PUT /api/config/system/{key}/` - Update system configuration (admin)
- `GET /api/integrations/` - List integrations
- `PUT /api/integrations/{id}/` - Update integration config (admin)
- `POST /api/integrations/{id}/test/` - Test integration connection

### Blockchain
- `GET /api/blockchain/incidents/{id}/` - Get blockchain record for incident
- `POST /api/blockchain/incidents/{id}/notarize/` - Trigger blockchain notarization
- `GET /api/blockchain/transactions/` - List blockchain transactions
- `GET /api/blockchain/contracts/` - List deployed contracts
- `GET /api/blockchain/status/` - Get blockchain service status

### Work Orders & Maintenance
- `GET /api/work-orders/` - List work orders
- `POST /api/work-orders/` - Create work order
- `GET /api/work-orders/{id}/` - Get work order details
- `PATCH /api/work-orders/{id}/status/` - Update work order status
- `POST /api/inspections/` - Create infrastructure inspection
- `GET /api/inspections/` - List inspections

### WebSocket Endpoints (Real-time)
- `/ws/incidents/` - Real-time incident updates
- `/ws/notifications/` - Real-time notifications
- `/ws/location/{responder_id}/` - Real-time responder location tracking

---

## Features & Functionality

### Core Features

#### 1. **Identity & Access Management**
- Multi-role RBAC system with 15+ distinct roles
- OTP-based authentication for citizens
- MFA for privileged accounts (TOTP)
- OAuth2/OIDC integration capability
- Anonymous reporting support with optional registration
- Reputation scoring system for citizen reporters
- User profile management with preferences

#### 2. **Incident Reporting & Capture**
- Mobile-first incident reporting (Flutter app integration)
- One-tap SOS feature
- Guided report flow with validation
- Mandatory fields: type, severity, description (≥20 chars), GPS, timestamp
- Optional metadata: weather, lane count, vehicles involved, injuries, infrastructure damage
- Offline-first data persistence with conflict resolution
- Anonymous reporting support
- Road classification and geospatial tagging

#### 3. **Media & Evidence Management**
- Multi-format support: photos (up to 5), video (120s max), audio notes
- Automatic media compression
- EXIF data scrubbing and geotag removal
- Configurable face and license plate redaction
- Virus scanning pipeline
- Secure object storage (S3-compatible)
- SHA256 hashing for all assets
- Blockchain anchoring for evidence integrity
- Thumbnail generation
- Evidence timeline tracking

#### 4. **AI-Powered Verification**
- Image classification (accident/hazard/obstruction detection)
- Duplicate detection using spatial-temporal algorithms
- Credibility scoring for reports
- Automated false positive detection
- Human-in-the-loop review queue
- AI model versioning and accuracy tracking
- Explainable AI results

#### 5. **Multi-Source Validation**
- RFID reader integration for vehicle validation
- CCTV camera feed retrieval and analysis
- Sensor data correlation (traffic, weather, road conditions)
- Temporal-spatial matching algorithms
- Confidence scoring (0-100%) based on multi-source correlation
- Automatic validation when confidence threshold met
- Validation evidence trail

#### 6. **Response Coordination**
- Intelligent assignment engine (role, location, workload, equipment)
- Real-time location tracking for responders
- Geofenced arrival detection
- Response milestone tracking (dispatched/en_route/on_scene/transporting/cleared)
- Route optimization
- Responder checklists and protocol guidance
- Multi-agency coordination
- Assignment acceptance/rejection workflow

#### 7. **SLA Management & Escalation**
- Configurable SLA rules per severity/type
- Automatic SLA clock tracking
- Real-time SLA breach detection
- Automated escalation paths
- Escalation level tracking
- SLA compliance reporting

#### 8. **Blockchain Integration (Base)**
- Gasless meta-transactions (sponsored transactions)
- Incident hash notarization
- Response milestone logging on-chain
- Evidence anchoring
- Role access registry on-chain
- Incentive pool management (smart contracts)
- Relayer/Paymaster service integration
- Off-chain private data with on-chain hashes
- Transaction retry and queue management

#### 9. **Notifications & Communications**
- Multi-channel notifications (Push/FCM/APNS, SMS, Email, USSD)
- Configurable notification templates
- Real-time push notifications
- Incident-specific messaging
- Broadcast alerts with geofencing
- Notification preference management
- Delivery status tracking

#### 10. **Analytics & Reporting**
- Real-time dashboards (role-based)
- Response time distribution analysis
- Incident heatmaps (geospatial)
- Recurring hazard identification
- Reporter engagement metrics
- Responder utilization analytics
- AI accuracy tracking
- Predictive analytics (hazard forecasting, maintenance planning)
- Custom report generation (CSV, PDF)
- API feeds for external systems

#### 11. **IoT Integration Layer**
- RFID adapter service with MQTT/REST support
- CCTV integration with RTSP/ONVIF protocols
- Sensor data ingestion (MQTT/CoAP/REST)
- Real-time stream processing
- Protocol converters (MQTT/CoAP/REST/gRPC)
- Data normalization and storage
- Privacy-preserving vehicle identification (hashing)
- Time-series data storage (TimescaleDB)

#### 12. **Administration & Configuration**
- Taxonomy management (categories, severities, road networks)
- SLA and escalation rule editor
- Integration management (API keys, endpoints, credentials)
- Content management (safety tips, FAQ, education modules)
- System configuration management
- User role management
- AI model configuration

#### 13. **Work Orders & Maintenance**
- Infrastructure inspection assignments
- Field inspection reporting with photos
- Work order management
- Maintenance crew coordination
- Progress tracking
- Completion documentation

#### 14. **Audit & Compliance**
- Immutable audit logs
- Tamper detection
- 10-year retention policy
- Compliance with Kenya Data Protection Act & GDPR
- Right-to-be-forgotten processes
- Data anonymization
- Blockchain-anchored critical actions

#### 15. **Incentive Management**
- Reputation-based incentives
- Quality report rewards
- Engagement tracking
- Blockchain-based incentive distribution
- Incentive pool management

### Technical Features

#### Performance
- API median latency <500ms
- WebSocket support for 10k+ concurrent clients
- Mobile UI optimization (<3s load on 3G)
- CDN-backed media delivery
- Database query optimization
- Caching layer (Redis)

#### Reliability
- 99.9% uptime target
- Regional redundancy
- RPO ≤1 hour, RTO ≤4 hours
- Graceful degradation (blockchain queue + replay)
- Offline-first mobile support

#### Security
- TLS 1.3 everywhere
- AES-256 encryption at rest
- Secrets management (Vault/KMS)
- Mutual TLS (mTLS) for KeNHA integrations
- API key rotation
- Network segmentation
- Regular security audits

#### Scalability
- Kubernetes deployment ready
- Autoscaling support
- Sharded PostGIS for geospatial queries
- Message queue for async processing (Celery)
- Horizontal scaling capability

#### Observability
- Prometheus metrics
- Grafana dashboards
- ELK/OpenSearch logging
- Sentry error tracking
- SLA breach alerts
- AI drift detection
- Blockchain transaction monitoring

---

## Next Steps

This document provides the comprehensive architecture for building the eSafety backend. The Django implementation should follow these models, routes, and features as specified.

