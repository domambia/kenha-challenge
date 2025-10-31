# eSafety Incident Management Platform – Product Requirements Document

## 1. Overview

**Product Name:** eSafety  
**Prepared For:** Kenya National Highways Authority (KeNHA) and partner agencies  
**Prepared By:** MUIA LTD  

### 1.1 Vision
Position Kenya as the benchmark for digital road safety governance in Africa by deploying a citizen-powered, Base blockchain-enabled platform that delivers transparent, real-time incident management without burdening users with transaction fees.

### 1.2 Problem Statement
KeNHA manages over 22,000 km of trunk roads without a unified digital system for near real-time incident reporting and response. Current paper-based and siloed processes lead to slow intervention, fragmented data, limited citizen participation, and weak accountability.

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

### 4.1 Road User (Flutter Mobile App)
1. Optional sign-in or anon flag (phone/email verification for registered users).  
2. One-tap SOS or guided report flow capturing incident type, severity, textual description (≥20 characters), timestamp, and GPS coordinates with manual override.  
3. Attach media: up to five photos, one 120-second video, one audio note; auto-compress, scrub EXIF, geotag.  
4. Submit; backend stores locally if offline and syncs when online.  
5. Receive incident ID, live status updates, and follow-up requests (chat style).  
6. Post-resolution feedback and rating prompts.

### 4.2 KeNHA Dispatcher (Next.js Admin)
1. MFA-protected login with role-based access.  
2. Monitor live incident queue ranked by severity and AI credibility score on map/timeline.  
3. Inspect media, reporter history, geospatial context; verify/merge duplicates.  
4. Assign emergency responders, set SLA clock, and trigger alerts.  
5. Track progress, escalate on breach, close incident with resolution notes anchored to Base blockchain.  

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

### 5.2 Incident Capture
- Mandatory fields: incident type, severity, free-text description, timestamp, GPS coordinates, road classification.
- Metadata options: weather, lane count, vehicles involved, injury presence, infrastructure damage tags.
- Offline-first persistence with conflict resolution during sync.

### 5.3 Evidence Management
- Media pipeline: validate file type, compress, virus scan, redact faces/license plates (configurable), store in secure object storage.
- Hash each asset and incident payload; record proof on Base via gasless meta-transaction relays.
- Time-stamped evidence timeline accessible by authorized roles.

### 5.4 Triage & Verification
- AI services for image classification (accident, hazard, obstruction), duplicate detection within spatial-temporal radius, and credibility scoring.
- Human reviewer queue with map overlay, timeline, and blockchain proof references.
- SLA engine mapping severity levels to response timers and escalation paths.
- **Multi-source Validation:** Cross-reference citizen reports with KeNHA IoT sensor data:
  - **RFID Reader Validation:** Correlate reported vehicle incidents with RFID reader logs to verify vehicle presence and timing
  - **CCTV Camera Verification:** Automatically retrieve nearby camera feeds at incident time/location to validate reports
  - **Sensor Correlation:** Match reports with traffic flow sensors, weather sensors, and road condition monitors
  - **Confidence Scoring:** Assign verification scores based on multiple data source correlation (0-100% confidence)

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
- **Mobile App:** Flutter (iOS, Android, web) with offline storage, push notifications, camera integration.
- **Admin Web App:** Next.js + TypeScript, Tailwind UI, Mapbox/Leaflet, Redux Toolkit state.
- **Backend:** Django + Django REST Framework, PostgreSQL with PostGIS, Redis cache, Celery workers, WebSocket server for live updates.
- **AI Microservices:** Python-based models (FastAPI) for computer vision and deduplication, orchestrated via message queues.
- **IoT Integration Layer:** Python microservices for KeNHA system integration (RFID, CCTV, sensors) with protocol adapters (MQTT, REST, gRPC).
- **Blockchain Integration:** Node.js or Python service interacting with Base smart contracts through relayers; uses ethers.js/web3.py for signing and verification.
- **Observability Stack:** Prometheus, Grafana, ELK/Opensearch, Sentry for error tracking.

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