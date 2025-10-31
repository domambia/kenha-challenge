"""
Management command to run all seed commands
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run all seed commands to populate the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users-count',
            type=int,
            default=5,
            help='Number of users per role (default: 5)',
        )
        parser.add_argument(
            '--incidents-count',
            type=int,
            default=50,
            help='Number of incidents (default: 50)',
        )
        parser.add_argument(
            '--rfid-count',
            type=int,
            default=20,
            help='Number of RFID readers (default: 20)',
        )
        parser.add_argument(
            '--cctv-count',
            type=int,
            default=30,
            help='Number of CCTV cameras (default: 30)',
        )
        parser.add_argument(
            '--sensor-count',
            type=int,
            default=25,
            help='Number of sensors (default: 25)',
        )
        parser.add_argument(
            '--logs-count',
            type=int,
            default=100,
            help='Number of RFID logs (default: 100)',
        )
        parser.add_argument(
            '--readings-count',
            type=int,
            default=150,
            help='Number of sensor readings (default: 150)',
        )
        parser.add_argument(
            '--workorders-count',
            type=int,
            default=30,
            help='Number of work orders (default: 30)',
        )
        parser.add_argument(
            '--response-count',
            type=int,
            default=40,
            help='Number of response assignments (default: 40)',
        )
        parser.add_argument(
            '--skip-users',
            action='store_true',
            help='Skip seeding users',
        )
        parser.add_argument(
            '--skip-incidents',
            action='store_true',
            help='Skip seeding incidents',
        )
        parser.add_argument(
            '--skip-iot',
            action='store_true',
            help='Skip seeding IoT devices',
        )
        parser.add_argument(
            '--skip-workorders',
            action='store_true',
            help='Skip seeding work orders',
        )
        parser.add_argument(
            '--skip-response',
            action='store_true',
            help='Skip seeding response data',
        )
        parser.add_argument(
            '--skip-config',
            action='store_true',
            help='Skip seeding configurations',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('Starting database seeding process...'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Seed configurations first (foundation)
        if not options['skip_config']:
            self.stdout.write(self.style.WARNING('\n[1/6] Seeding system configurations...'))
            call_command('seed_config')
        
        # Seed users (required for other entities)
        if not options['skip_users']:
            self.stdout.write(self.style.WARNING('\n[2/6] Seeding users with all roles...'))
            call_command('seed_users', count=options['users_count'])
        
        # Seed incidents (core data)
        if not options['skip_incidents']:
            self.stdout.write(self.style.WARNING('\n[3/6] Seeding incidents, types, and severities...'))
            call_command('seed_incidents', count=options['incidents_count'])
        
        # Seed IoT devices
        if not options['skip_iot']:
            self.stdout.write(self.style.WARNING('\n[4/6] Seeding IoT devices (RFID, CCTV, Sensors)...'))
            call_command(
                'seed_iot',
                rfid_count=options['rfid_count'],
                cctv_count=options['cctv_count'],
                sensor_count=options['sensor_count'],
                logs_count=options['logs_count'],
                readings_count=options['readings_count'],
            )
        
        # Seed work orders
        if not options['skip_workorders']:
            self.stdout.write(self.style.WARNING('\n[5/6] Seeding work orders...'))
            call_command('seed_workorders', count=options['workorders_count'])
        
        # Seed response data
        if not options['skip_response']:
            self.stdout.write(self.style.WARNING('\n[6/6] Seeding response assignments and milestones...'))
            call_command('seed_response', count=options['response_count'])
        
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 60))
        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('\nSummary:')
        self.stdout.write(f'  - Users: {options["users_count"]} per role (unless skipped)')
        self.stdout.write(f'  - Incidents: {options["incidents_count"]} (unless skipped)')
        self.stdout.write(f'  - RFID Readers: {options["rfid_count"]} (unless skipped)')
        self.stdout.write(f'  - CCTV Cameras: {options["cctv_count"]} (unless skipped)')
        self.stdout.write(f'  - Sensors: {options["sensor_count"]} (unless skipped)')
        self.stdout.write(f'  - Work Orders: {options["workorders_count"]} (unless skipped)')
        self.stdout.write(f'  - Response Assignments: {options["response_count"]} (unless skipped)')
        self.stdout.write('\n')

