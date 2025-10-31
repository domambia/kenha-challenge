# eSafety Incident Management Platform – Product Requirements Document

## 1. Overview

**Product Name:** eSafety  
**Prepared For:** Kenya National Highways Authority (KeNHA) and partner agencies  
**Prepared By:** MUIA LTD  

### 1.1 Vision
Position Kenya as the benchmark for digital road safety governance in Africa by deploying a citizen-powered, Base blockchain-enabled platform that delivers transparent, real-time incident management without burdening users with transaction fees.

### 1.2 Problem Statement
KeNHA manages over 22,000 km of trunk roads without a unified digital system for near real-time incident reporting and response. Current paper-based and siloed processes lead to slow intervention, fragmented data, limited citizen participation, and weak accountability. Road incidents and infrastructure vandalism often go unreported or are reported through inefficient channels, delaying response and repair actions.

### 1.3 Strategic Pillars
- **Citizen-first reporting:** Simple, trusted channels for road users to submit evidence-rich incidents.
- **Coordinated response:** Shared operational picture for KeNHA, emergency services, and partners.
- **Trusted data:** Immutable evidence lifecycle using Base blockchain with gasless submissions.
- **Intelligence-driven improvement:** AI-assisted verification, predictive analytics, and policy-ready insights.

### 1.4 Out of Scope (Phase 1)
- Compulsory integration with existing regional CAD systems.
- Insurance claims processing or financial settlements.
- Paid roadside assistance services or hardware deployment.

---

## 2. Objectives & Success Metrics

- **Reduce emergency response time** by 40% on pilot corridors within 12 months.
- **Increase validated citizen reports** by 300% while maintaining ≥90% verification accuracy.
- **Resolve 95% of priority incidents** (P1/P2) within defined service levels.
- **Achieve 50% citizen participation growth** in targeted regions.
- **Deliver tamper-proof auditability** with zero user gas fees via Base smart contracts and sponsored transactions.

Lagging metrics include reduction in secondary crashes (20%) and decrease in incident management costs (25%). Leading indicators include active daily reporters, responder adoption, and AI accuracy trends.

---

## 3. Stakeholders & Personas

- **KeNHA National Operations Center:** Program owners monitoring KPIs and compliance.
- **Regional Traffic Control & Maintenance Teams:** Dispatch, incident triage, infrastructure follow-up.
- **Emergency Services (Police, Ambulance, Fire, Towing):** Receive assignments, update status, close incidents.
- **Road Users (Drivers, PSV operators, pedestrians, cyclists):** Submit reports with multimedia evidence, track resolutions.
- **Data & Policy Analysts:** Explore trends, prepare reports, recommend interventions.
- **Technology & Integration Partners:** Base blockchain team, telcos, mapping providers, AI vendors.
- **Governance Bodies (NTSA, Ministry of Transport, county governments):** Regulatory oversight and policy alignment.

### 3.1 Comprehensive User Roles & Access Levels

The platform supports multiple user roles with distinct permissions and capabilities:

#### 3.1.1 Citizen Roles
- **Road User (Normal User / Anonymous Reporter):**
  - Report incidents via mobile app or web portal
  - View real-time traffic updates and alerts
  - Track reported incidents and receive status updates
  - Provide feedback and ratings post-resolution
  - Access safety tips and educational content
  - Optional: Anonymous reporting with limited follow-up capability
  - **Access:** Public incident reports (own submissions), real-time alerts, safety information

- **Registered Road User:**
  - All anonymous user capabilities
  - Reputation scoring based on report accuracy
  - Receive incentives for high-quality reports
  - Access to detailed reporting history
  - Priority support for verified accounts
  - **Access:** Enhanced features, reputation dashboard, incentive tracking

#### 3.1.2 Emergency Response Personnel
- **Police Services:**
  - Access incident assignments with priority routing
  - View CCTV feeds and sensor data for incident validation
  - Document violations and enforcement actions
  - Coordinate with other emergency services
  - Access traffic violation records and vehicle identification (via RFID)
  - **Access:** Incident dispatch queue, CCTV feeds, RFID vehicle data, enforcement tools, multi-agency coordination

- **Emergency Medical Services (EMS / Ambulance):**
  - Receive medical emergency dispatches
  - Access patient information and incident severity
  - Coordinate with hospitals for patient transport
  - Update incident status (en route, on scene, transporting, cleared)
  - Request additional medical resources
  - **Access:** Medical incident queue, patient details (when authorized), hospital coordination, resource management

- **Fire & Rescue Services:**
  - Receive fire and rescue incident assignments
  - Access infrastructure damage assessments
  - Coordinate hazmat and specialized response
  - Document scene safety and resource deployment
  - **Access:** Fire/rescue dispatch, infrastructure maps, hazmat protocols, equipment inventory

- **Towing & Recovery Services:**
  - Receive vehicle recovery assignments
  - Access vehicle information (make, model, license plate) via RFID correlation
  - View incident location and route optimization
  - Update vehicle recovery status
  - Submit billing and service completion reports
  - Coordinate with police for impound procedures
  - **Access:** Towing dispatch queue, vehicle details, location data, billing interface, police coordination tools

#### 3.1.3 KeNHA Operational Staff
- **Traffic Management Center (TMC) Operator:**
  - Monitor all incidents in real-time across the network
  - Access integrated feeds from CCTV, RFID, and sensors
  - Coordinate multi-agency responses
  - Manage traffic flow and lane control
  - Broadcast traveler information and alerts
  - **Access:** Comprehensive dashboards, all sensor feeds, traffic control systems, broadcast management

- **KeNHA Dispatcher:**
  - Triage and prioritize incidents based on severity and verification scores
  - Assign resources to incidents
  - Verify incidents using CCTV, RFID, and sensor data
  - Merge duplicate reports
  - Escalate incidents when SLA breaches occur
  - Close incidents with resolution documentation
  - **Access:** Incident queue management, verification tools, resource assignment, SLA monitoring, blockchain evidence logging

- **KeNHA Field Inspector:**
  - Receive infrastructure maintenance assignments
  - Document infrastructure damage and repair needs
  - Upload field inspection reports with photos
  - Coordinate with maintenance crews
  - Validate citizen-reported infrastructure issues
  - **Access:** Inspection assignments, incident details, reporting tools, maintenance coordination

- **KeNHA Maintenance Crew:**
  - Receive infrastructure repair and maintenance assignments
  - Access work order details and safety protocols
  - Update work progress and completion status
  - Request additional resources or equipment
  - Document repair work with photos and reports
  - **Access:** Maintenance queue, work orders, safety protocols, resource requests, documentation tools

#### 3.1.4 Administrative & Analysis Roles
- **System Administrator:**
  - Full system configuration and user management
  - Manage integrations with KeNHA systems (RFID, CCTV, sensors)
  - Configure AI models and validation rules
  - System health monitoring and troubleshooting
  - **Access:** System administration, integration management, user role assignment, system configuration

- **Super Admin:**
  - All administrative capabilities
  - Blockchain contract management
  - Compliance and audit oversight
  - Critical system operations
  - **Access:** Full system access, blockchain administration, compliance tools

- **Data Analyst:**
  - Access anonymized incident data and trends
  - Generate custom reports and dashboards
  - Export data for policy analysis
  - Access predictive analytics models
  - **Access:** Analytics dashboards, data export, reporting tools, predictive models

- **Policy Analyst:**
  - Access aggregated safety statistics
  - Generate policy recommendations
  - Review compliance metrics
  - Access research and development data (anonymized)
  - **Access:** Aggregated data views, compliance reports, research datasets, recommendation tools

#### 3.1.5 Support & Quality Assurance
- **Customer Support:**
  - Access user reports and feedback
  - Assist users with technical issues
  - Manage user accounts and verification
  - Escalate technical issues to development team
  - **Access:** User support dashboard, account management, ticket system

- **Quality Assurance Reviewer:**
  - Review and verify AI-classified incidents
  - Validate evidence quality and authenticity
  - Flag false reports and spam
  - Improve AI model training data
  - **Access:** Verification queue, evidence review tools, AI training interface

Primary personas include: Road User Reporter, KeNHA Dispatcher, Emergency Responder, Analyst, and System Administrator.

---

## 4. User Experience & Journeys

### 4.1 Road User (Flutter Mobile App) - Citizen Reporter

The mobile application empowers road users to report incidents and infrastructure vandalism using their smartphones with built-in GPS and camera capabilities.

**Core Reporting Flow:**
1. **Launch App & Report Type Selection:**
   - User opens eSafety mobile app
   - Selects incident type:
     - Road accident/collision
     - Road hazard (potholes, debris, obstructions)
     - Infrastructure vandalism (damaged guardrails, stolen signs, graffiti)
     - Traffic violation or dangerous driving
     - Emergency situation requiring immediate response

2. **GPS Location Capture (Mandatory):**
   - **Automatic GPS Capture:** App requests location permission and automatically captures current GPS coordinates (latitude/longitude)
   - **Manual Override:** User can manually adjust location on map if automatic capture is inaccurate
   - **Location Verification:** Displays address or landmark based on GPS coordinates for user confirmation
   - **GPS Metadata:** Captures altitude, accuracy, and timestamp along with coordinates

3. **Incident Details Entry:**
   - **Free-text Description:** User describes the incident in detail (minimum 20 characters)
   - **Incident Category:** Accidents, vandalism, hazards, emergencies
   - **Severity Level:** Critical, High, Medium, Low
   - **Timestamp:** Auto-captured, user can adjust if reporting delayed incident
   - **Additional Metadata:** Weather conditions, number of vehicles involved, injuries present

4. **Pictorial Evidence (Mandatory):**
   - **Photo Capture:** 
     - Up to 5 photos using phone camera or gallery
     - Camera integrated directly in app for immediate capture
     - Automatic compression and optimization for network efficiency
     - EXIF data scrubbing for privacy (removes personal metadata)
     - Geotagging confirmation (embeds GPS coordinates in image metadata)
   - **Video Recording:**
     - Up to 120-second video recording capability
     - Integrated video recorder in app
     - Automatic compression to reduce file size
     - GPS timestamp embedded in video metadata
   - **Optional Audio Notes:** Voice description of incident (60 seconds max)

5. **Submission to Centralized Servers:**
   - **Data Transmission:** All incident data (text, GPS coordinates, photos, videos) transmitted to centralized Django backend servers
   - **Offline Support:** If network unavailable, data stored locally and synced when connection restored
   - **Confirmation:** User receives unique incident ID immediately upon successful submission
   - **Blockchain Notarization:** Incident hash automatically recorded on Base blockchain via relayer service (gasless for user)

6. **Status Tracking & Follow-up:**
   - Receive real-time status updates via push notifications
   - View incident status: Submitted → Verified → Assigned → In Progress → Resolved
   - Track responder location (when authorized)
   - Receive follow-up messages from dispatchers or responders
   - Post-resolution feedback and rating prompts

### 4.2 Centralized Dashboard Access (Next.js Admin Portal)

All authorized users access the same centralized dashboard hosted on Django backend servers, with role-based permissions controlling data visibility and actions.

**Dashboard Users & Access Levels:**

#### 4.2.1 KeNHA HQ (Platform Owner - Full Access)
- **Full System Access:** Complete oversight of all incidents, users, and system operations
- **Dashboard Features:**
  - Real-time incident map showing all reported incidents across the network
  - Incident queue with AI-verified confidence scores
  - Access to all photos, videos, and GPS coordinates from citizen reports
  - Multi-source correlation view (RFID, CCTV, sensor data overlay)
  - Analytics dashboards: response times, incident trends, road safety metrics
  - System configuration and user management
  - Blockchain audit trail viewer
  - Export capabilities for reports and analytics

#### 4.2.2 Police Services
- **Incident Assignment Access:** Receive assignments for traffic incidents, violations, and emergencies
- **Dashboard Features:**
  - Incident queue filtered by priority and jurisdiction
  - Full access to citizen-reported photos, videos, and GPS coordinates
  - CCTV feed integration for incident validation
  - RFID vehicle identification data (when authorized)
  - Route optimization to incident location
  - Enforcement action logging and documentation
  - Real-time communication with dispatchers and other responders

#### 4.2.3 Emergency Services (Ambulance, Fire, Towing)
- **Emergency Dispatch Access:** Receive medical, fire, or vehicle recovery assignments
- **Dashboard Features:**
  - Emergency incident queue with severity filtering
  - Access to incident photos/videos for scene assessment
  - GPS navigation to precise incident location
  - Resource allocation and status updates
  - Coordination tools for multi-agency responses
  - Patient information access (for medical emergencies, when authorized)

#### 4.2.4 Other Authorized Users
- **Analysts & Policy Makers:**
  - Access anonymized incident data and trends
  - Analytics dashboards and reporting tools
  - Historical data export capabilities
- **Maintenance Crews:**
  - Infrastructure repair assignments
  - Access to vandalism and damage reports with photos
  - GPS locations for repair sites
  - Work order management

**Common Dashboard Workflow (All Authorized Users):**
1. **Login:** MFA-protected login with role-based access control
2. **Incident View:** Monitor live incident queue ranked by severity and AI credibility score on interactive map/timeline
3. **Evidence Review:** 
   - Inspect citizen-submitted photos and videos directly in dashboard
   - View GPS coordinates on map overlay
   - Review incident description and metadata
   - Access multi-source correlation data (RFID, CCTV, sensor matches)
   - View AI analysis results (incident classification, severity assessment)
4. **Verification & Assignment:**
   - Verify incidents using integrated CCTV feeds and sensor data
   - Merge duplicate reports
   - Assign to appropriate responders (police, emergency services, maintenance)
   - Set SLA timers and trigger alerts
5. **Tracking & Resolution:**
   - Track responder progress in real-time
   - Monitor SLA compliance
   - Escalate on SLA breach
   - Close incidents with resolution notes and documentation
   - All actions logged to blockchain for audit trail  

### 4.3 Emergency Responder
- Accept assignment via mobile web/app, view optimized route, update status (en route/on scene/cleared), add additional media, and confirm resolution.

### 4.4 Analyst & Leadership
- Explore dashboards (hotspots, response KPIs, trend analysis), export reports, audit blockchain-stamped evidence history.

---

## 5. Functional Requirements

### 5.1 Identity & Access
- Role-based access control: Super Admin, KeNHA Ops, Emergency Lead, Responder, Analyst, Support.
- Social/OTP onboarding for citizens; optional anonymity with limited follow-up.
- Reputation scoring for reporters (accuracy, spam tolerance) stored off-chain with hashed references on Base.

### 5.2 Incident Capture (Citizen Mobile App)

**Mandatory Fields:**
- **GPS Coordinates (Latitude/Longitude):** Automatically captured from phone GPS, mandatory for all reports
- **Incident Type:** Road accident, hazard, vandalism, emergency, or other
- **Severity Level:** Critical, High, Medium, Low
- **Free-text Description:** Detailed description of incident (minimum 20 characters)
- **Timestamp:** When incident occurred (auto-captured, user adjustable)
- **Pictorial Evidence:** At least one photo required; video optional but recommended
- **Road Classification:** National highway, county road, urban street, etc.

**Photo & Video Requirements:**
- **Photos:** Up to 5 photos per incident, captured using phone camera
  - Automatic GPS geotagging embedded in image metadata
  - EXIF data scrubbing for privacy (removes user device info)
  - Compression to optimize upload while maintaining quality
  - Virus scanning before storage
- **Videos:** Up to 120 seconds, captured using phone camera
  - GPS timestamp embedded in video metadata
  - Compression and encoding optimization
  - Privacy redaction for faces/license plates (configurable)

**Optional Metadata:**
- Weather conditions at incident time
- Number of vehicles involved
- Injury presence indicator
- Infrastructure damage tags (for vandalism reports)
- Lane count and road conditions
- Witness contact information

**Offline Support:**
- Offline-first persistence: All data stored locally when network unavailable
- Automatic sync when connection restored
- Conflict resolution during sync (latest timestamp wins)
- User notification when offline submissions are successfully synced

### 5.3 Evidence Management
- Media pipeline: validate file type, compress, virus scan, redact faces/license plates (configurable), store in secure object storage.
- Hash each asset and incident payload; record proof on Base via gasless meta-transaction relays.
- Time-stamped evidence timeline accessible by authorized roles.

### 5.4 AI-Powered Analysis & Multi-Source Verification

#### 5.4.1 AI Photo & Video Analysis
The platform employs advanced AI/ML models to analyze citizen-submitted photos and videos for automatic incident classification and validation.

**Photo Analysis:**
- **Image Classification:** 
  - Detect incident type: accident, hazard, vandalism, infrastructure damage
  - Identify severity indicators: vehicle damage, road obstructions, safety hazards
  - Object detection: vehicles, people, road infrastructure, debris
  - Damage assessment: extent of damage, repair urgency estimation
- **Metadata Extraction:**
  - Verify GPS coordinates embedded in photo EXIF data
  - Cross-check reported location with geotag coordinates
  - Extract timestamp from image metadata
- **Quality Assessment:**
  - Image clarity and usability scoring
  - Detect blur, poor lighting, or unusable images
  - Suggest when additional photos needed

**Video Analysis:**
- **Video Processing:**
  - Frame-by-frame analysis for incident detection
  - Motion detection and tracking
  - Event identification: collision, obstruction formation, vandalism activity
- **Temporal Analysis:**
  - Sequence of events reconstruction
  - Incident timeline extraction from video
  - Duration and impact assessment
- **Privacy Protection:**
  - Automatic face detection and blurring
  - License plate detection and redaction (configurable)
  - Privacy compliance before storage and sharing

**AI Model Details:**
- **Computer Vision:** YOLOv8 or similar for object detection
- **Image Classification:** ResNet or EfficientNet for incident type classification
- **Video Processing:** Temporal CNNs for sequence analysis
- **Training Data:** Continuous improvement with human-verified incident reports
- **Model Updates:** Regular retraining with new data to improve accuracy

#### 5.4.2 Multi-Source Correlation (KeNHA System Integration)
Cross-reference citizen reports with existing KeNHA systems for enhanced validation and verification.

**RFID Reader Integration:**
- Correlate reported vehicle incidents with RFID reader logs
- Verify vehicle presence at incident location and time (±2km radius, ±10 minutes)
- Vehicle identification matching (privacy-preserved through hashing)
- Movement pattern analysis for hit-and-run investigations

**CCTV Camera Integration:**
- Automatic retrieval of nearby CCTV feeds based on GPS coordinates (±500m radius)
- Video feed analysis for incident time window (±5 minutes from reported timestamp)
- AI-powered video analysis confirms incident type and severity
- Manual review interface for dispatchers to view CCTV evidence

**Sensor Data Correlation:**
- Traffic flow sensors: Validate congestion/accident reports with traffic anomaly detection
- Weather sensors: Correlate weather-related incidents with meteorological data
- Road surface sensors: Match infrastructure damage reports with sensor readings
- Vibration sensors: Validate infrastructure damage or landslide reports

**Confidence Scoring Algorithm:**
- **Multi-source Confidence Score (0-100%):**
  - AI Photo/Video Analysis: 40% weight
  - CCTV Verification: 30% weight
  - RFID Correlation: 20% weight
  - Sensor Correlation: 10% weight
- **Verification Status:**
  - **VERIFIED (≥70%):** High confidence, immediate dispatch priority
  - **PROBABLE (50-69%):** Moderate confidence, human review recommended
  - **UNVERIFIED (<50%):** Low confidence, additional evidence needed

#### 5.4.3 Human Review & Triage
- Human reviewer queue with map overlay showing all incidents
- Timeline view showing incident sequence and correlations
- Blockchain proof references for all evidence sources
- SLA engine mapping severity levels to response timers and escalation paths
- Duplicate detection and merging within spatial-temporal radius

### 5.5 Response Coordination
- Assignment engine considering responder role, location, workload, and equipment.
- Real-time location sharing and geofenced arrival detection.
- Integrated communication: in-app messaging, SMS/email, push notifications.
- Responder checklists and protocol guidance accessible on mobile.

### 5.6 Blockchain Layer (Base)
- Use Base L2 network with account abstraction and sponsored meta-transactions to eliminate user gas fees.
- Smart contracts (Solidity) handle: incident hash notarization, response milestone logging, role access registry, incentive pool management.
- Off-chain services manage private data; only hashed references stored on-chain to preserve privacy.
- Relayer/Paymaster service operated by platform covers minimal gas costs, abstracted from end users.

### 5.7 Notifications & Communications
- Configurable templates for submission receipt, dispatch assignment, ETA updates, resolution confirmation, escalation notices.
- Multi-channel: push (FCM/APNS), SMS, email, USSD prompts for low-end devices.
- Broadcast alerts for major incidents or road closures with geofencing.

### 5.8 Analytics & Reporting
- Dashboards: response time distribution, incident heatmaps, recurring hazards, reporter engagement, responder utilization, AI accuracy.
- Export formats: CSV, PDF, API feeds.
- Predictive models for high-risk segments and maintenance planning.

### 5.9 Administration & Configuration
- Taxonomy management (incident categories, severity definitions, road networks).
- SLA and escalation rule editor.
- Integration management (mapping API keys, SMS gateways, Base relayer endpoints).
- Content management for safety tips, FAQ, user education modules.

---

## 6. Technical Architecture

### 6.1 Platform Components

**Citizen Mobile Application (Flutter):**
- Cross-platform mobile app (iOS, Android, web)
- GPS location capture (latitude/longitude) with high accuracy
- Camera integration for photo and video capture
- Offline storage and sync when connection restored
- Push notifications for status updates
- Real-time incident tracking

**Centralized Dashboard (Next.js Admin Portal):**
- Web-based dashboard accessible to all authorized users (Police, KeNHA HQ, Emergency Services, Others)
- Real-time incident monitoring with map visualization
- Photo and video viewer integrated in dashboard
- Multi-user access with role-based permissions
- Responsive design for desktop and tablet access

**Centralized Backend Servers (Django):**
- **Core Services:** Django + Django REST Framework
- **Database:** PostgreSQL with PostGIS for geospatial queries (GPS coordinates)
- **Cache:** Redis for session management and queue management
- **Background Jobs:** Celery workers for async processing
- **Real-time Updates:** WebSocket server (Django Channels) for live dashboard updates
- **Media Storage:** Secure object storage (S3/MinIO) for photos and videos
- **Data Processing:** All incident data (GPS, photos, videos, metadata) processed and stored on centralized servers

**AI Analysis Services:**
- **Computer Vision Microservices:** Python-based FastAPI services
  - Photo analysis: Image classification, object detection, damage assessment
  - Video analysis: Frame-by-frame processing, temporal event detection
  - Model serving: YOLOv8, ResNet, or similar for incident classification
- **Orchestration:** Message queues (Redis/Celery) for AI task distribution
- **Model Training Pipeline:** Continuous improvement with verified incident data

**KeNHA System Integration Layer:**
- **IoT Adapter Services:** Python microservices for existing KeNHA systems
  - RFID reader integration (MQTT/REST protocols)
  - CCTV camera integration (ONVIF/RTSP protocols)
  - Sensor data ingestion (MQTT/CoAP protocols)
- **Protocol Converters:** MQTT, REST, gRPC adapters for different KeNHA systems
- **Real-time Correlation:** Multi-source data correlation engine

**Blockchain Integration:**
- Base L2 network integration via relayer service
- Node.js or Python service for smart contract interaction
- Uses ethers.js/web3.py for transaction signing and verification
- Gasless transactions for end users (sponsored by platform)

**Observability Stack:**
- Prometheus for metrics collection
- Grafana for visualization dashboards
- ELK/Opensearch for centralized logging
- Sentry for error tracking and alerting

### 6.2 KeNHA System Integration Architecture

#### 6.2.1 RFID Reader Integration
- **Purpose:** Vehicle identification and movement tracking for incident validation
- **Integration Method:**
  - Real-time data ingestion via MQTT or REST API from KeNHA RFID infrastructure
  - Vehicle registration number correlation with incident reports
  - Temporal-spatial matching: verify reported vehicles were present at incident location/time
  - Privacy-preserving: hash vehicle identifiers before correlation
- **Data Flow:**
  1. RFID readers capture vehicle tags at highway checkpoints
  2. Data streamed to KeNHA middleware → eSafety IoT adapter
  3. Normalized and stored in time-series database (TimescaleDB extension)
  4. Incident validation service queries RFID logs for correlation
  5. Confidence score calculated based on RFID proximity and timing
- **Use Cases:**
  - Validate vehicle presence at accident scene
  - Identify hit-and-run vehicles
  - Track vehicle movement patterns for investigation
  - Verify commercial vehicle compliance

#### 6.2.2 CCTV Camera Integration
- **Purpose:** Visual verification of reported incidents using existing KeNHA surveillance network
- **Integration Method:**
  - API integration with KeNHA CCTV management system
  - Automatic camera feed retrieval based on incident GPS coordinates
  - Computer vision analysis of video footage for incident detection
  - Manual review interface for dispatchers
- **Data Flow:**
  1. Incident reported with GPS coordinates
  2. System identifies nearest CCTV cameras (±500m radius)
  3. Retrieves video feed for incident time window (±5 minutes)
  4. AI analyzes footage for incident validation (accident, obstruction, traffic violation)
  5. Dispatcher can manually review feeds in admin console
  6. Validated footage clips stored as evidence with blockchain hash
- **Technical Specifications:**
  - Support for RTSP, ONVIF protocols
  - Video storage: H.264/H.265 encoded, 30-day retention for validation clips
  - AI inference: YOLOv8 or similar for object detection, incident classification
  - Privacy: Automatic face and license plate blurring (configurable)
- **Use Cases:**
  - Visual confirmation of accidents and hazards
  - Detect unreported incidents automatically
  - Investigate false reports and spam
  - Traffic flow analysis and congestion monitoring

#### 6.2.3 Sensor Integration (Weather, Traffic, Road Conditions)
- **Purpose:** Multi-sensor data correlation for incident validation and predictive safety
- **Sensor Types:**
  - **Traffic Flow Sensors:** Inductive loops, radar sensors measuring vehicle count, speed, occupancy
  - **Weather Sensors:** Temperature, humidity, precipitation, visibility, wind speed
  - **Road Surface Sensors:** Temperature, moisture, ice detection
  - **Air Quality Sensors:** Pollutant levels affecting visibility
  - **Vibration Sensors:** Detect infrastructure damage, landslides
- **Integration Method:**
  - MQTT or CoAP protocols for real-time sensor data ingestion
  - Edge computing nodes aggregate sensor data before transmission
  - Time-series database storage (InfluxDB or TimescaleDB) for historical analysis
- **Data Flow:**
  1. Sensors continuously transmit data to KeNHA data aggregation points
  2. eSafety platform subscribes to sensor data streams
  3. Real-time correlation engine matches sensor anomalies with incident reports
  4. Validation confidence score includes sensor data correlation
  5. Predictive models use sensor data for hazard forecasting
- **Validation Logic:**
  - Traffic flow anomalies → validate congestion/accident reports
  - Weather sensor data → validate weather-related incident claims
  - Road surface conditions → correlate with infrastructure damage reports
  - Vibration spikes → validate infrastructure damage or landslides

#### 6.2.4 Integration Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         KeNHA Existing Infrastructure                     │
├─────────────────┬─────────────────┬─────────────────┬───────────────────┤
│  RFID Readers   │   CCTV Cameras  │  Traffic Sensors │  Weather Sensors │
│  (Highway       │   (Surveillance │  (Flow/Speed)    │  (Temp/Rain)     │
│   Checkpoints)  │   Network)      │                  │                   │
└────────┬────────┴────────┬─────────┴────────┬─────────┴────────┬────────┘
         │                 │                    │                   │
         │ MQTT/REST       │ ONVIF/RTSP         │ MQTT/CoAP         │ MQTT
         │                 │                    │                   │
┌────────▼─────────────────▼────────────────────▼───────────────────▼──────┐
│              eSafety IoT Integration Layer (Django Microservices)         │
├──────────────────────────────────────────────────────────────────────────┤
│  • RFID Adapter Service    • CCTV Integration Service                    │
│  • Sensor Data Ingestion   • Protocol Converters (MQTT/CoAP/REST/gRPC)   │
│  • Data Normalization      • Real-time Stream Processing                 │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │
                         │ Message Queue (Redis/Celery)
                         │
┌────────────────────────▼─────────────────────────────────────────────────┐
│                   Incident Validation Service                             │
├──────────────────────────────────────────────────────────────────────────┤
│  • Multi-source correlation engine                                       │
│  • Confidence scoring algorithm                                           │
│  • Temporal-spatial matching                                              │
│  • AI-powered anomaly detection                                           │
└────────────────────────┬─────────────────────────────────────────────────┘
                         │
                         │ Validated Incident Data
                         │
┌────────────────────────▼─────────────────────────────────────────────────┐
│                    eSafety Core Platform                                  │
│  (Django Backend, PostgreSQL/PostGIS, Blockchain Integration)             │
└──────────────────────────────────────────────────────────────────────────┘
```

### 6.3 Data Flow Highlights
1. Reporter submits incident → Django API validates, stores metadata, queues AI tasks.  
2. **IoT Integration:** Incident triggers multi-source validation query (RFID, CCTV, sensors)  
3. **Validation Service:** Correlates citizen report with sensor data, calculates confidence score  
4. AI results update incident record; hashed payload sent to blockchain integration service.  
5. Relayer signs and submits Base transaction covering gas via sponsored meta-transaction; transaction receipt stored in backend.  
6. Dispatcher receives validated incident with confidence score and sensor correlation evidence  
7. Dispatcher actions trigger updates, notifications, and additional blockchain checkpoints.  
8. Analytics pipelines aggregate data into dashboards and external reports.  

### 6.4 Security & Privacy
- TLS 1.3 everywhere, AES-256 encryption at rest, Vault/KMS for secrets.  
- MFA for privileged accounts, OAuth2/OIDC integration.  
- Immutable audit logs with tamper detection.  
- Compliance with Kenya Data Protection Act & GDPR (data minimization, consent management, right-to-be-forgotten processes).  
- Privacy-preserving techniques: PII stored off-chain, zero-knowledge proof exploration for future phases.  
- **IoT Integration Security:**
  - Mutual TLS (mTLS) for all KeNHA system connections
  - API key rotation for external integrations
  - Network segmentation: IoT integration layer in isolated network segment
  - Data anonymization: Vehicle identifiers hashed before storage
  - CCTV privacy: Automatic blurring of faces/license plates, configurable retention policies  

---

## 7. Non-Functional Requirements

- **Performance:** API median latency <500 ms; WebSockets handle ≥10k concurrent clients; mobile UI loads <3 s on 3G.  
- **Reliability:** 99.9% uptime target; regional redundancy; RPO ≤1 hour, RTO ≤4 hours; graceful degradation if Base network unavailable (queue + replay).  
- **Scalability:** Kubernetes deployment with autoscaling; CDN-backed media delivery; sharded PostGIS for geospatial queries.  
- **Accessibility:** WCAG 2.1 AA compliance for admin, English and Swahili localization, voice assistance, low-bandwidth mode.  
- **Monitoring:** Alerts on SLA breaches, AI drift detection, blockchain transaction latency, relayer health.  
- **Regulatory:** Audit trails for 10 years, adherence to NTSA reporting standards, readiness for Base ecosystem compliance reviews.  

---

## 8. Implementation Roadmap (Indicative)

### Phase 0 – Alignment (2 Weeks)
- Stakeholder workshops, legal/data-sharing agreements, KPI confirmation, technical architecture approval.

### Phase 1 – Core MVP (6 Weeks)
- Django backend (incidents, users, media pipeline, Base relayer integration).  
- Flutter app (registration, incident capture, offline sync, notifications).  
- Next.js admin (incident queue, map view, responder assignment).  
- Simple analytics dashboard, Base contract deployment for incident notarization.  

### Phase 2 – Automation & Integrations (6 Weeks)
- AI verification services, responder mobile web, SLA engine, SMS/email channels.  
- Expanded Base contracts for milestone tracking, incentives, and role registry.  
- IoT/CCTV ingestion pilots, predictive analytics prototypes.  
- Beta deployment on selected corridors with training.  

### Phase 3 – Scale & Optimization (6 Weeks)
- Advanced dashboards, after-action review tooling, gamified citizen incentives.  
- Offline USSD/SMS fallback, multilingual support, public awareness campaign.  
- Security hardening, performance tuning, disaster recovery drills.  

Continuous activities: model retraining, stakeholder training, regulatory engagement, community outreach.

---

## 9. Dependencies & Assumptions

### 9.1 Technical Dependencies
- Access to road network GIS data and incident logs for training and benchmarking.  
- Partnerships with Base ecosystem for relayer/paymaster infrastructure and ongoing support.  
- Telco agreements for SMS/USSD channels and zero-rated application access.  
- Mapping licenses (Google Maps, Mapbox, or OpenStreetMap enhancements).  
- Budget for AI data labeling, community engagement, and hardware for field teams.  
- Cloud hosting approvals aligned with Kenyan public sector guidelines.  

### 9.2 KeNHA Integration Dependencies
- **RFID Infrastructure Access:**
  - API access to KeNHA RFID reader network
  - Vehicle registration database integration (privacy-compliant)
  - Real-time data stream access (MQTT broker or REST API endpoints)
  - Historical RFID log access for incident investigation

- **CCTV System Integration:**
  - API access to KeNHA CCTV management system
  - Camera location and metadata database
  - Video feed access protocols (ONVIF, RTSP, or proprietary API)
  - Storage capacity for incident validation clips (minimum 30-day retention)

- **Sensor Network Access:**
  - Integration with KeNHA traffic monitoring sensors
  - Weather station data feeds
  - Road condition sensor access
  - Real-time data stream protocols (MQTT, CoAP, or REST)

- **Network Connectivity:**
  - Dedicated network segment for IoT integration
  - Low-latency connection to KeNHA data centers
  - Redundant connectivity paths for high availability
  - VPN or private network connection for secure data transmission

### 9.3 Operational Assumptions
- KeNHA systems (RFID, CCTV, sensors) are operational and accessible 95%+ uptime
- Existing KeNHA infrastructure supports modern API protocols
- KeNHA operational teams trained on integrated system workflows
- Data sharing agreements in place for cross-system data correlation
- Regulatory approval for vehicle identification correlation (privacy-compliant)  

---

## 10. Risks & Mitigations

- **Citizen adoption lag:** Run awareness campaigns, partner with matatu saccos, offer non-monetary rewards and recognition.  
- **AI misclassification:** Maintain human-in-the-loop reviews, continuous retraining, explainable AI dashboards.  
- **Connectivity gaps:** Offline caching, delayed sync notifications, SMS/USSD fallback, explore roadside Wi-Fi pilots.  
- **Blockchain regulation shifts:** Modular blockchain adapter, legal counsel engagement, option to toggle notarization frequency.  
- **Operational overload:** SLA-based auto-escalation, staffing plans, phased rollout starting with high-priority corridors.  
- **Security threats:** Regular penetration tests, bug bounty, incident response runbooks.  

---

## 11. Open Questions

1. What level of identity verification does KeNHA require for citizen reporters (national ID linking, driving license, or OTP only)?  
2. Which existing KeNHA/NTSA systems must integrate at launch (maintenance work orders, CAD, CCTV)?  
3. Who funds relayer infrastructure for gasless Base transactions long term, and what monitoring/reporting is needed?  
4. How should incentives for high-quality reports be structured (recognition, airtime sponsorship, Base ecosystem partnerships)?  
5. What data retention timelines and anonymization policies align with regulatory expectations?  