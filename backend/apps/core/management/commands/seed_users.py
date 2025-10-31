"""
Management command to seed users with all roles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile, UserReputation, UserRole
from decimal import Decimal
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed users with all available roles'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of users to create per role (default: 5)',
        )

    def handle(self, *args, **options):
        count = options['count']
        self.stdout.write(self.style.SUCCESS('Starting user seeding...'))
        
        # Kenya phone number prefixes
        prefixes = ['0700', '0701', '0702', '0703', '0704', '0705', '0706', '0707', '0708', '0709',
                    '0710', '0711', '0712', '0713', '0714', '0715', '0716', '0717', '0718', '0719',
                    '0720', '0721', '0722', '0723', '0724', '0725', '0726', '0727', '0728', '0729',
                    '0733', '0734', '0735', '0736', '0737', '0738', '0740', '0741', '0742', '0743',
                    '0744', '0745', '0746', '0747', '0748', '0749', '0750', '0751', '0752', '0753',
                    '0754', '0755', '0756', '0757', '0758', '0759', '0760', '0761', '0762', '0763',
                    '0764', '0765', '0766', '0767', '0768', '0769', '0770', '0771', '0772', '0773',
                    '0774', '0775', '0776', '0777', '0778', '0779', '0789', '0790', '0791', '0792',
                    '0793', '0794', '0795', '0796', '0797', '0798', '0799']
        
        # Organizations based on roles
        organizations = {
            'super_admin': 'KeNHA Headquarters',
            'system_admin': 'KeNHA IT Department',
            'tmc_operator': 'Traffic Management Center',
            'dispatcher': 'KeNHA Dispatch Center',
            'field_inspector': 'KeNHA Field Operations',
            'maintenance_crew': 'KeNHA Maintenance',
            'police': 'Kenya Police Service',
            'ems': 'Emergency Medical Services',
            'fire_rescue': 'Fire & Rescue Services',
            'towing': 'Towing Services',
            'analyst': 'KeNHA Analytics',
            'policy_analyst': 'KeNHA Policy',
            'support': 'KeNHA Support',
            'qa_reviewer': 'KeNHA QA',
            'road_user_registered': None,
            'road_user_anonymous': None,
        }
        
        departments = {
            'super_admin': 'Administration',
            'system_admin': 'IT',
            'tmc_operator': 'Operations',
            'dispatcher': 'Dispatch',
            'field_inspector': 'Field Operations',
            'maintenance_crew': 'Maintenance',
            'police': 'Traffic Police',
            'ems': 'EMS',
            'fire_rescue': 'Fire Rescue',
            'towing': 'Recovery',
            'analyst': 'Data Analytics',
            'policy_analyst': 'Policy',
            'support': 'Customer Support',
            'qa_reviewer': 'Quality Assurance',
            'road_user_registered': None,
            'road_user_anonymous': None,
        }
        
        created_count = 0
        
        # Create users for each role
        for role_value, role_display in UserRole.choices:
            self.stdout.write(f'Creating {count} users with role: {role_display}')
            
            for i in range(count):
                # Generate unique email and phone
                email = f"{role_value}_{i+1}@kenha.test"
                phone = f"{random.choice(prefixes)}{random.randint(100000, 999999)}"
                
                # Determine admin permissions based on role
                is_staff = role_value in [
                    'super_admin', 'system_admin', 'tmc_operator', 
                    'dispatcher', 'analyst', 'policy_analyst', 
                    'support', 'qa_reviewer'
                ]
                is_superuser = role_value == 'super_admin'
                
                # Check if user already exists
                if User.objects.filter(email=email).exists():
                    # Update existing user with admin permissions if missing
                    user = User.objects.get(email=email)
                    updated = False
                    if user.is_staff != is_staff:
                        user.is_staff = is_staff
                        updated = True
                    if user.is_superuser != is_superuser:
                        user.is_superuser = is_superuser
                        updated = True
                    if updated:
                        user.save()
                        self.stdout.write(self.style.SUCCESS(f'Updated admin permissions for {email}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'User {email} already exists, skipping...'))
                    continue
                
                # Create user
                user = User.objects.create_user(
                    username=f"{role_value}_{i+1}",
                    email=email,
                    phone=phone,
                    password='Test1234!',  # Default password for testing
                    first_name=role_display.split()[0] if role_display else 'User',
                    last_name=f"Role{i+1}",
                    role=role_value,
                    is_verified=True,
                    email_verified=True,
                    phone_verified=True,
                    is_active=True,
                    is_staff=is_staff,  # Required for Django admin access
                    is_superuser=is_superuser,  # Required for full admin access
                    reputation_score=Decimal(random.uniform(30.0, 100.0)).quantize(Decimal('0.01')),
                )
                
                # Create user profile
                profile = UserProfile.objects.create(
                    user=user,
                    organization=organizations.get(role_value),
                    department=departments.get(role_value),
                    badge_number=f"BADGE-{role_value.upper()}-{i+1:03d}" if role_value not in ['road_user_registered', 'road_user_anonymous'] else None,
                    language='en',
                    notification_preferences={
                        'email': True,
                        'sms': role_value in ['tmc_operator', 'dispatcher', 'field_inspector', 'police', 'ems', 'fire_rescue'],
                        'push': True,
                    },
                )
                
                # Create reputation for registered road users and citizen reporters
                if role_value in ['road_user_registered', 'road_user_anonymous']:
                    UserReputation.objects.create(
                        user=user,
                        accuracy_score=Decimal(random.uniform(60.0, 95.0)).quantize(Decimal('0.01')),
                        report_count=random.randint(0, 50),
                        verified_reports=random.randint(0, 40),
                        false_reports=random.randint(0, 5),
                        spam_count=random.randint(0, 2),
                    )
                
                created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} users with all roles'))

