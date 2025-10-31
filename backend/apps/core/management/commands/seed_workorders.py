"""
Management command to seed work orders
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.workorders.models import WorkOrder, InfrastructureInspection
from apps.incidents.models import Incident
from apps.users.models import User, UserRole
import random


class Command(BaseCommand):
    help = 'Seed work orders and infrastructure inspections'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=30,
            help='Number of work orders to create (default: 30)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS('Starting work order seeding...'))
        
        # Kenya coordinates
        kenya_coordinates = [
            (-1.2921, 36.8219), (-1.6500, 37.0000), (-2.0000, 37.2000),
            (-1.1500, 36.9500), (-0.8000, 36.6000), (-0.3031, 36.0800),
            (-1.5000, 37.3000), (-2.2000, 37.7000), (-1.4000, 36.8500),
        ]
        
        # Get users for assignment
        field_inspectors = list(User.objects.filter(role=UserRole.FIELD_INSPECTOR))
        maintenance_crew = list(User.objects.filter(role=UserRole.MAINTENANCE_CREW))
        dispatchers = list(User.objects.filter(role=UserRole.DISPATCHER))
        
        # Get incidents
        incidents = list(Incident.objects.all()[:count])
        
        work_type_choices = [choice[0] for choice in WorkOrder.WORK_TYPES]
        status_choices = [choice[0] for choice in WorkOrder.STATUS_CHOICES]
        priorities = ['low', 'medium', 'high', 'urgent']
        
        descriptions = [
            'Road surface repair and pothole filling',
            'Guardrail replacement and installation',
            'Road sign installation and maintenance',
            'Culvert cleaning and repair',
            'Bridge inspection and structural assessment',
            'Drainage system maintenance',
            'Road marking and signage refresh',
            'Shoulder repair and stabilization',
            'Traffic light system maintenance',
            'Roadside vegetation clearing',
        ]
        
        created_count = 0
        
        for i in range(count):
            # Random coordinates
            lat, lng = random.choice(kenya_coordinates)
            lat = Decimal(str(lat)) + Decimal(str(random.uniform(-0.05, 0.05)))
            lng = Decimal(str(lng)) + Decimal(str(random.uniform(-0.05, 0.05)))
            
            lat = max(Decimal('-4.7'), min(Decimal('5.5'), lat))
            lng = max(Decimal('33.9'), min(Decimal('41.9'), lng))
            
            # Link to incident if available
            incident = incidents[i] if i < len(incidents) else None
            
            # Assign to users if available
            assigned_to = None
            assigned_by = None
            
            work_type = random.choice(work_type_choices)
            status = random.choice(status_choices)
            
            if status in ['assigned', 'in_progress', 'completed']:
                if work_type in ['inspection']:
                    assigned_to = random.choice(field_inspectors) if field_inspectors else None
                else:
                    assigned_to = random.choice(maintenance_crew) if maintenance_crew else None
                assigned_by = random.choice(dispatchers) if dispatchers else None
            
            work_order = WorkOrder.objects.create(
                incident=incident,
                work_type=work_type,
                assigned_to=assigned_to,
                assigned_by=assigned_by,
                status=status,
                priority=random.choice(priorities),
                description=random.choice(descriptions),
                latitude=lat,
                longitude=lng,
                estimated_duration=random.randint(30, 480),
                actual_duration=random.randint(30, 480) if status == 'completed' else None,
                started_at=timezone.now() - timedelta(days=random.randint(0, 30)) if status in ['in_progress', 'completed'] else None,
                completed_at=timezone.now() - timedelta(days=random.randint(0, 15)) if status == 'completed' else None,
                completion_notes=f"Work order completed. {random.choice(['All work completed successfully', 'Minor adjustments made', 'Follow-up required'])}." if status == 'completed' else '',
            )
            
            # Create infrastructure inspection for inspection work orders
            if work_type == 'inspection' and assigned_to:
                InfrastructureInspection.objects.create(
                    work_order=work_order,
                    inspector=assigned_to,
                    inspection_date=work_order.created_at + timedelta(hours=random.randint(1, 24)),
                    inspection_type=random.choice(['Routine', 'Emergency', 'Post-Incident', 'Preventive']),
                    damage_assessment={
                        'severity': random.choice(['Minor', 'Moderate', 'Severe']),
                        'affected_area_sqm': random.randint(10, 500),
                        'estimated_repair_cost': random.randint(50000, 500000),
                    },
                    repair_needed=random.choice([True, False]),
                    priority=random.choice(priorities),
                    inspection_report=f"Inspection completed. Condition assessment: {random.choice(['Good', 'Fair', 'Poor', 'Critical'])}. Recommendations provided.",
                )
            
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_count} work orders'
        ))

