"""
Management command to seed incidents, incident types, and severities
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import uuid
import random
from apps.incidents.models import (
    IncidentType, IncidentSeverity, Incident, IncidentComment,
    IncidentStatus, VerificationStatus
)
from apps.users.models import User, UserRole


class Command(BaseCommand):
    help = 'Seed incidents with types and severities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of incidents to create (default: 50)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS('Starting incident seeding...'))
        
        # Create Incident Types
        incident_types_data = [
            # Accidents
            {'name': 'Vehicle Collision', 'category': 'accident', 'severity_template': 'P1', 'default_sla_minutes': 30},
            {'name': 'Multiple Vehicle Pile-up', 'category': 'accident', 'severity_template': 'P1', 'default_sla_minutes': 15},
            {'name': 'Single Vehicle Accident', 'category': 'accident', 'severity_template': 'P2', 'default_sla_minutes': 45},
            {'name': 'Pedestrian Accident', 'category': 'accident', 'severity_template': 'P1', 'default_sla_minutes': 20},
            {'name': 'Motorcycle Accident', 'category': 'accident', 'severity_template': 'P2', 'default_sla_minutes': 40},
            
            # Hazards
            {'name': 'Fallen Tree', 'category': 'hazard', 'severity_template': 'P2', 'default_sla_minutes': 60},
            {'name': 'Debris on Road', 'category': 'hazard', 'severity_template': 'P3', 'default_sla_minutes': 90},
            {'name': 'Oil Spill', 'category': 'hazard', 'severity_template': 'P2', 'default_sla_minutes': 45},
            {'name': 'Animal on Road', 'category': 'hazard', 'severity_template': 'P3', 'default_sla_minutes': 120},
            {'name': 'Pothole', 'category': 'hazard', 'severity_template': 'P4', 'default_sla_minutes': 180},
            {'name': 'Flooding', 'category': 'hazard', 'severity_template': 'P2', 'default_sla_minutes': 30},
            {'name': 'Landslide', 'category': 'hazard', 'severity_template': 'P1', 'default_sla_minutes': 20},
            
            # Infrastructure
            {'name': 'Road Damage', 'category': 'infrastructure', 'severity_template': 'P2', 'default_sla_minutes': 120},
            {'name': 'Bridge Damage', 'category': 'infrastructure', 'severity_template': 'P1', 'default_sla_minutes': 15},
            {'name': 'Missing Road Sign', 'category': 'infrastructure', 'severity_template': 'P4', 'default_sla_minutes': 240},
            {'name': 'Broken Guardrail', 'category': 'infrastructure', 'severity_template': 'P3', 'default_sla_minutes': 180},
            {'name': 'Traffic Light Malfunction', 'category': 'infrastructure', 'severity_template': 'P2', 'default_sla_minutes': 60},
            {'name': 'Culvert Blockage', 'category': 'infrastructure', 'severity_template': 'P3', 'default_sla_minutes': 120},
            
            # Other
            {'name': 'Vandalism', 'category': 'other', 'severity_template': 'P3', 'default_sla_minutes': 180},
            {'name': 'Illegal Roadside Trading', 'category': 'other', 'severity_template': 'P4', 'default_sla_minutes': 240},
        ]
        
        incident_types = {}
        for it_data in incident_types_data:
            incident_type, created = IncidentType.objects.get_or_create(
                name=it_data['name'],
                defaults=it_data
            )
            incident_types[it_data['name']] = incident_type
            if created:
                self.stdout.write(f'Created incident type: {incident_type.name}')
        
        # Create Incident Severities
        severities_data = [
            {
                'level': 'P1',
                'name': 'Critical',
                'description': 'Life-threatening or immediate danger. Requires immediate response.',
                'response_time_target_minutes': 15,
                'escalation_time_minutes': 20,
                'color_code': '#FF0000',
                'priority_score': 100,
            },
            {
                'level': 'P2',
                'name': 'High',
                'description': 'Serious incident requiring urgent attention. High priority response.',
                'response_time_target_minutes': 30,
                'escalation_time_minutes': 45,
                'color_code': '#FF6600',
                'priority_score': 75,
            },
            {
                'level': 'P3',
                'name': 'Medium',
                'description': 'Moderate incident requiring timely response.',
                'response_time_target_minutes': 60,
                'escalation_time_minutes': 90,
                'color_code': '#FFCC00',
                'priority_score': 50,
            },
            {
                'level': 'P4',
                'name': 'Low',
                'description': 'Minor incident. Can be scheduled for response.',
                'response_time_target_minutes': 120,
                'escalation_time_minutes': 180,
                'color_code': '#00CC00',
                'priority_score': 25,
            },
        ]
        
        severities = {}
        for sev_data in severities_data:
            severity, created = IncidentSeverity.objects.get_or_create(
                level=sev_data['level'],
                defaults=sev_data
            )
            severities[sev_data['level']] = severity
            if created:
                self.stdout.write(f'Created severity: {severity.level} - {severity.name}')
        
        # Kenya coordinates - Major highway locations
        # Coordinates along KENHA's 22,000 KM road network
        kenya_coordinates = [
            # Nairobi - Mombasa Highway (A109)
            (-1.2921, 36.8219),  # Nairobi
            (-1.6500, 37.0000),  # Along A109
            (-2.0000, 37.2000),
            (-2.5000, 37.5000),
            (-3.0000, 38.0000),
            (-3.5000, 38.5000),
            (-4.0435, 39.6682),  # Mombasa
            
            # Thika Highway (A2)
            (-1.1500, 36.9500),
            (-1.0000, 37.0500),
            (-0.9000, 37.1000),  # Thika area
            
            # Nairobi - Nakuru Highway (A104)
            (-1.2000, 36.8000),
            (-0.8000, 36.6000),
            (-0.5000, 36.4000),
            (-0.3031, 36.0800),  # Nakuru
            
            # Western routes
            (-0.1000, 34.7500),  # Kisumu area
            (-0.5000, 35.0000),
            
            # Northern routes
            (0.3000, 36.9000),  # Nyeri area
            (0.5000, 37.0000),
            
            # Eastern routes
            (-1.3000, 38.0000),
            (-1.0000, 37.8000),
            
            # Additional highway points
            (-1.4500, 36.9000),
            (-1.1000, 37.1000),
            (-0.7000, 36.5000),
            (-0.4000, 36.2000),
            (-1.5000, 37.3000),
            (-2.2000, 37.7000),
            (-3.2000, 38.3000),
        ]
        
        # Road classifications
        road_classifications = ['A-Class', 'B-Class', 'C-Class', 'Trunk Road', 'Main Road']
        road_names = [
            'Nairobi-Mombasa Highway', 'Thika Highway', 'Nairobi-Nakuru Highway',
            'Northern Corridor', 'Western Bypass', 'Eastern Bypass', 'Great North Road',
            'Nairobi-Thika Superhighway', 'Mombasa Road', 'Nakuru-Eldoret Highway'
        ]
        
        # Weather conditions
        weather_conditions = ['Clear', 'Sunny', 'Cloudy', 'Rainy', 'Foggy', 'Windy']
        
        # Get users for reporting
        reporters = list(User.objects.filter(
            role__in=[UserRole.ROAD_USER_REGISTERED, UserRole.ROAD_USER_ANONYMOUS]
        ))
        
        created_count = 0
        
        for i in range(count):
            # Random incident type and severity
            incident_type = random.choice(list(incident_types.values()))
            severity = severities[incident_type.severity_template]
            
            # Random coordinates
            lat, lng = random.choice(kenya_coordinates)
            # Convert to Decimal and add small random variation
            lat = Decimal(str(lat)) + Decimal(str(random.uniform(-0.05, 0.05)))
            lng = Decimal(str(lng)) + Decimal(str(random.uniform(-0.05, 0.05)))
            
            # Ensure within Kenya boundaries
            lat = max(Decimal('-4.7'), min(Decimal('5.5'), lat))
            lng = max(Decimal('33.9'), min(Decimal('41.9'), lng))
            
            # Random timestamp (within last 30 days)
            incident_time = timezone.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            
            # Generate unique incident ID
            unique_suffix = str(uuid.uuid4())[:8].upper()
            incident_id = f"INC-{timezone.now().strftime('%Y%m%d%H%M%S')}-{unique_suffix}"
            
            # Create incident
            incident = Incident.objects.create(
                incident_id=incident_id,
                incident_type=incident_type,
                severity=severity,
                status=random.choice(list(IncidentStatus.choices))[0],
                reporter=random.choice(reporters) if reporters else None,
                is_anonymous=random.choice([True, False]),
                description=f"{incident_type.name} reported. {random.choice(['Multiple vehicles involved', 'Single vehicle', 'No injuries reported', 'Injuries reported', 'Heavy traffic', 'Road blocked'])}. Immediate attention required.",
                latitude=lat,
                longitude=lng,
                road_classification=random.choice(road_classifications),
                road_name=random.choice(road_names),
                nearest_milestone=f"KM {random.randint(1, 500)}",
                timestamp=incident_time,
                weather=random.choice(weather_conditions),
                lane_count=random.choice([2, 4, 6, 8]),
                vehicles_involved_count=random.randint(0, 5),
                has_injuries=random.choice([True, False]),
                verification_status=random.choice(list(VerificationStatus.choices))[0],
                ai_confidence_score=Decimal(random.uniform(60.0, 95.0)).quantize(Decimal('0.01')),
            )
            
            # Set SLA times
            if incident.verification_status == VerificationStatus.VERIFIED:
                incident.sla_start_time = incident.timestamp
                incident.sla_target_time = incident.timestamp + timedelta(minutes=severity.response_time_target_minutes)
                incident.verified_at = incident.timestamp + timedelta(minutes=random.randint(5, 30))
                if random.choice([True, False]):
                    incident.verified_by = random.choice(list(User.objects.filter(
                        role__in=[UserRole.TMC_OPERATOR, UserRole.DISPATCHER, UserRole.FIELD_INSPECTOR]
                    ))) if User.objects.filter(role__in=[UserRole.TMC_OPERATOR, UserRole.DISPATCHER, UserRole.FIELD_INSPECTOR]).exists() else None
            
            if incident.status == IncidentStatus.RESOLVED:
                incident.resolved_at = incident.timestamp + timedelta(hours=random.randint(1, 6))
                incident.resolution_notes = f"Incident resolved. {random.choice(['Traffic cleared', 'Debris removed', 'Repairs completed', 'Emergency services cleared scene'])}."
                incident.resolved_by = random.choice(list(User.objects.filter(
                    role__in=[UserRole.FIELD_INSPECTOR, UserRole.MAINTENANCE_CREW, UserRole.DISPATCHER]
                ))) if User.objects.filter(role__in=[UserRole.FIELD_INSPECTOR, UserRole.MAINTENANCE_CREW, UserRole.DISPATCHER]).exists() else None
            
            incident.save()
            
            # Create some comments for some incidents
            if random.choice([True, False]) and User.objects.filter(
                role__in=[UserRole.TMC_OPERATOR, UserRole.DISPATCHER, UserRole.FIELD_INSPECTOR]
            ).exists():
                commenter = random.choice(list(User.objects.filter(
                    role__in=[UserRole.TMC_OPERATOR, UserRole.DISPATCHER, UserRole.FIELD_INSPECTOR]
                )))
                IncidentComment.objects.create(
                    incident=incident,
                    user=commenter,
                    comment_text=f"Internal note: {random.choice(['Dispatch crew assigned', 'Verification in progress', 'Resources en route', 'Monitoring situation'])}.",
                    comment_type='internal',
                )
            
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} incidents with types and severities'
        ))

