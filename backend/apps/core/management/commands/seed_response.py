"""
Management command to seed response assignments and milestones
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.response.models import (
    IncidentAssignment, ResponseMilestone, ResponderLocation,
    MilestoneType, AssignmentStatus
)
from apps.incidents.models import Incident, IncidentStatus
from apps.users.models import User, UserRole
import random


class Command(BaseCommand):
    help = 'Seed response assignments and milestones'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=40,
            help='Number of assignments to create (default: 40)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS('Starting response seeding...'))
        
        # Get responders
        police = list(User.objects.filter(role=UserRole.POLICE))
        ems = list(User.objects.filter(role=UserRole.EMS))
        fire_rescue = list(User.objects.filter(role=UserRole.FIRE_RESCUE))
        towing = list(User.objects.filter(role=UserRole.TOWING))
        dispatchers = list(User.objects.filter(role=UserRole.DISPATCHER))
        
        # Get incidents that need response
        incidents = list(Incident.objects.filter(
            status__in=[IncidentStatus.ASSIGNED, IncidentStatus.IN_PROGRESS, IncidentStatus.VERIFIED, IncidentStatus.PENDING]
        )[:count])
        
        if not incidents:
            incidents = list(Incident.objects.all()[:count])
        
        assignment_types = ['primary', 'backup', 'specialist']
        milestone_types = [mt[0] for mt in MilestoneType.choices]
        assignment_statuses = [as_[0] for as_ in AssignmentStatus.choices]
        
        created_assignments = 0
        created_milestones = 0
        created_locations = 0
        
        for incident in incidents:
            # Determine which responders are needed based on incident type
            responders_needed = []
            if incident.has_injuries:
                responders_needed.extend(random.sample(ems, min(2, len(ems))))
            if 'accident' in incident.incident_type.category.lower() or incident.has_injuries:
                responders_needed.extend(random.sample(police, min(1, len(police))))
            if 'fire' in incident.description.lower() or incident.incident_type.category == 'hazard':
                responders_needed.extend(random.sample(fire_rescue, min(1, len(fire_rescue))))
            if incident.vehicles_involved_count > 0:
                responders_needed.extend(random.sample(towing, min(1, len(towing))))
            
            # If no specific responders needed, assign based on severity
            if not responders_needed:
                if incident.severity.level in ['P1', 'P2']:
                    responders_needed.extend(random.sample(ems, min(1, len(ems))))
                responders_needed.extend(random.sample(police, min(1, len(police))))
            
            # Create assignments
            for responder in responders_needed[:3]:  # Max 3 assignments per incident
                assignment = IncidentAssignment.objects.create(
                    incident=incident,
                    assigned_to=responder,
                    assigned_by=random.choice(dispatchers) if dispatchers else None,
                    assignment_type=random.choice(assignment_types),
                    status=random.choice(assignment_statuses),
                    accepted_at=timezone.now() - timedelta(minutes=random.randint(5, 60)) if random.choice([True, False]) else None,
                    estimated_arrival_time=incident.timestamp + timedelta(minutes=random.randint(10, 90)),
                    actual_arrival_time=incident.timestamp + timedelta(minutes=random.randint(15, 120)) if random.choice([True, False]) else None,
                    notes=f"Assignment for {incident.incident_type.name}. {random.choice(['Proceed with caution', 'Multiple units responding', 'High priority response'])}.",
                )
                created_assignments += 1
                
                # Create milestones if assignment is accepted or in progress
                if assignment.status in [AssignmentStatus.ACCEPTED, AssignmentStatus.IN_PROGRESS, AssignmentStatus.COMPLETED]:
                    # Create milestone sequence
                    milestone_sequence = ['dispatched', 'en_route', 'on_scene']
                    if assignment.status == AssignmentStatus.COMPLETED:
                        milestone_sequence.extend(['cleared'])
                    
                    milestone_time = assignment.assigned_at
                    for milestone_type in milestone_sequence:
                        milestone_time += timedelta(minutes=random.randint(5, 30))
                        
                        milestone = ResponseMilestone.objects.create(
                            incident=incident,
                            responder=responder,
                            assignment=assignment,
                            milestone_type=milestone_type,
                            latitude=incident.latitude + Decimal(str(random.uniform(-0.01, 0.01))),
                            longitude=incident.longitude + Decimal(str(random.uniform(-0.01, 0.01))),
                            notes=f"{milestone_type.replace('_', ' ').title()} milestone reached.",
                            timestamp=milestone_time,
                        )
                        created_milestones += 1
                        
                        # Create responder location tracking
                        for loc_count in range(random.randint(2, 5)):
                            ResponderLocation.objects.create(
                                responder=responder,
                                latitude=incident.latitude + Decimal(str(random.uniform(-0.05, 0.05))),
                                longitude=incident.longitude + Decimal(str(random.uniform(-0.05, 0.05))),
                                timestamp=milestone_time - timedelta(minutes=loc_count * 5),
                                accuracy=Decimal(random.uniform(5.0, 50.0)).quantize(Decimal('0.01')),
                                speed=Decimal(random.uniform(0.0, 80.0)).quantize(Decimal('0.01')) if milestone_type != 'on_scene' else Decimal(0),
                                heading=Decimal(random.uniform(0.0, 360.0)).quantize(Decimal('0.01')),
                                is_active=milestone_type != 'cleared',
                            )
                            created_locations += 1
                
                # Update incident status if assignments are active
                if assignment.status == AssignmentStatus.IN_PROGRESS:
                    incident.status = IncidentStatus.IN_PROGRESS
                    incident.save()
                elif assignment.status == AssignmentStatus.COMPLETED:
                    if not incident.resolved_at:
                        incident.status = IncidentStatus.RESOLVED
                        incident.resolved_at = timezone.now()
                        incident.resolved_by = responder
                        incident.save()
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created {created_assignments} assignments, '
            f'{created_milestones} milestones, and {created_locations} responder locations'
        ))

