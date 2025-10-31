"""
Management command to seed IoT devices (RFID readers, CCTV cameras, Sensors)
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from apps.iot.models import (
    RFIDReader, RFIDLog, CCTVCamera, CCTVFeed, Sensor, SensorReading, IncidentValidation
)
from apps.incidents.models import Incident, VerificationStatus
import random


class Command(BaseCommand):
    help = 'Seed IoT devices and data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--rfid-count',
            type=int,
            default=20,
            help='Number of RFID readers to create (default: 20)',
        )
        parser.add_argument(
            '--cctv-count',
            type=int,
            default=30,
            help='Number of CCTV cameras to create (default: 30)',
        )
        parser.add_argument(
            '--sensor-count',
            type=int,
            default=25,
            help='Number of sensors to create (default: 25)',
        )
        parser.add_argument(
            '--logs-count',
            type=int,
            default=100,
            help='Number of RFID logs to create (default: 100)',
        )
        parser.add_argument(
            '--readings-count',
            type=int,
            default=150,
            help='Number of sensor readings to create (default: 150)',
        )

    def handle(self, *args, **options):
        rfid_count = options['rfid_count']
        cctv_count = options['cctv_count']
        sensor_count = options['sensor_count']
        logs_count = options['logs_count']
        readings_count = options['readings_count']
        
        self.stdout.write(self.style.SUCCESS('Starting IoT device seeding...'))
        
        # Kenya coordinates for IoT devices
        kenya_coordinates = [
            # Nairobi area
            (-1.2921, 36.8219), (-1.2500, 36.8500), (-1.3000, 36.8000),
            (-1.2000, 36.9000), (-1.3500, 36.7500),
            
            # Along major highways
            (-1.6500, 37.0000), (-2.0000, 37.2000), (-2.5000, 37.5000),
            (-1.1500, 36.9500), (-1.0000, 37.0500),
            (-0.8000, 36.6000), (-0.5000, 36.4000), (-0.3031, 36.0800),
            (-0.1000, 34.7500), (0.3000, 36.9000),
            
            # Additional strategic locations
            (-1.5000, 37.3000), (-2.2000, 37.7000), (-3.2000, 38.3000),
            (-1.4000, 36.8500), (-1.1000, 37.1000), (-0.7000, 36.5000),
        ]
        
        manufacturers = ['Hikvision', 'Bosch', 'Axis', 'Siemens', 'Honeywell', 'Motorola']
        models = ['Pro Series', 'Enterprise', 'Standard', 'Premium', 'Elite']
        protocols = ['RTSP', 'ONVIF', 'proprietary']
        
        # Create RFID Readers
        self.stdout.write(f'Creating {rfid_count} RFID readers...')
        rfid_readers = []
        rfid_created = 0
        for i in range(rfid_count):
            reader_id = f"RFID-{i+1:04d}"
            
            # Check if reader already exists
            reader, created = RFIDReader.objects.get_or_create(
                reader_id=reader_id,
                defaults={
                    'latitude': Decimal('-1.2921'),
                    'longitude': Decimal('36.8219'),
                    'status': 'active',
                }
            )
            
            if created:
                lat, lng = random.choice(kenya_coordinates)
                lat = Decimal(str(lat)) + Decimal(str(random.uniform(-0.02, 0.02)))
                lng = Decimal(str(lng)) + Decimal(str(random.uniform(-0.02, 0.02)))
                
                lat = max(Decimal('-4.7'), min(Decimal('5.5'), lat))
                lng = max(Decimal('33.9'), min(Decimal('41.9'), lng))
                
                reader.latitude = lat
                reader.longitude = lng
                reader.installation_date = timezone.now() - timedelta(days=random.randint(30, 730))
                reader.manufacturer = random.choice(manufacturers)
                reader.model = f"{random.choice(models)} RFID"
                reader.api_endpoint = f"https://api.kenha.ke/rfid/{i+1}/read"
                reader.mqtt_topic = f"rfid/reader_{i+1}"
                reader.status = random.choice(['active', 'active', 'active', 'inactive', 'maintenance'])
                reader.save()
                rfid_created += 1
            else:
                self.stdout.write(self.style.WARNING(f'RFID Reader {reader_id} already exists, skipping...'))
            
            rfid_readers.append(reader)
        
        # Create RFID Logs
        self.stdout.write(f'Creating {logs_count} RFID logs...')
        vehicle_tags = [f"TAG-{i:06d}" for i in range(1000, 2000)]
        vehicle_types = ['Saloon', 'SUV', 'Truck', 'Bus', 'Motorcycle', 'Van']
        vehicle_classes = ['Private', 'Commercial', 'PSV', 'Government']
        
        for i in range(logs_count):
            reader = random.choice(rfid_readers)
            log_time = timezone.now() - timedelta(
                hours=random.randint(0, 720),
                minutes=random.randint(0, 59)
            )
            
            RFIDLog.objects.create(
                reader=reader,
                vehicle_tag=random.choice(vehicle_tags),
                vehicle_registration=f"K{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])}{random.randint(100, 999)}{random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])}",
                timestamp=log_time,
                latitude=reader.latitude + Decimal(str(random.uniform(-0.001, 0.001))),
                longitude=reader.longitude + Decimal(str(random.uniform(-0.001, 0.001))),
                direction=random.choice(['North', 'South', 'East', 'West']),
                lane=random.randint(1, 4),
                speed=Decimal(random.uniform(40.0, 120.0)).quantize(Decimal('0.01')),
                vehicle_type=random.choice(vehicle_types),
                vehicle_class=random.choice(vehicle_classes),
            )
        
        # Create CCTV Cameras
        self.stdout.write(f'Creating {cctv_count} CCTV cameras...')
        cctv_cameras = []
        cctv_created = 0
        camera_types = ['PTZ', 'Fixed', 'Dome', 'Bullet', 'Thermal']
        
        for i in range(cctv_count):
            camera_id = f"CCTV-{i+1:04d}"
            
            # Check if camera already exists
            camera, created = CCTVCamera.objects.get_or_create(
                camera_id=camera_id,
                defaults={
                    'latitude': Decimal('-1.2921'),
                    'longitude': Decimal('36.8219'),
                    'status': 'active',
                }
            )
            
            if created:
                lat, lng = random.choice(kenya_coordinates)
                lat = Decimal(str(lat)) + Decimal(str(random.uniform(-0.02, 0.02)))
                lng = Decimal(str(lng)) + Decimal(str(random.uniform(-0.02, 0.02)))
                
                lat = max(Decimal('-4.7'), min(Decimal('5.5'), lat))
                lng = max(Decimal('33.9'), min(Decimal('41.9'), lng))
                
                camera.latitude = lat
                camera.longitude = lng
                camera.coverage_radius_meters = random.randint(100, 1000)
                camera.installation_date = timezone.now() - timedelta(days=random.randint(30, 730))
                camera.camera_type = random.choice(camera_types)
                camera.protocol = random.choice(protocols)
                camera.api_endpoint = f"https://api.kenha.ke/cctv/{i+1}/feed"
                camera.rtsp_url = f"rtsp://cctv.kenha.ke/camera_{i+1}"
                camera.status = random.choice(['active', 'active', 'active', 'inactive', 'maintenance'])
                camera.metadata = {
                    'resolution': random.choice(['720p', '1080p', '4K']),
                    'fps': random.choice([15, 25, 30]),
                    'night_vision': random.choice([True, False]),
                }
                camera.save()
                cctv_created += 1
            else:
                self.stdout.write(self.style.WARNING(f'CCTV Camera {camera_id} already exists, skipping...'))
            
            cctv_cameras.append(camera)
        
        # Create CCTV Feeds (link to incidents if available)
        incidents = list(Incident.objects.all()[:50])
        self.stdout.write(f'Creating CCTV feeds...')
        for i, camera in enumerate(cctv_cameras[:20]):  # Create feeds for first 20 cameras
            start_time = timezone.now() - timedelta(hours=random.randint(1, 168))
            end_time = start_time + timedelta(minutes=random.randint(5, 60))
            
            incident = random.choice(incidents) if incidents and random.choice([True, False]) else None
            
            CCTVFeed.objects.create(
                camera=camera,
                incident=incident,
                start_time=start_time,
                end_time=end_time,
                video_file_path=f"https://storage.kenha.ke/videos/cctv_{camera.camera_id}_{start_time.strftime('%Y%m%d%H%M%S')}.mp4",
                ai_analysis_result={
                    'objects_detected': random.randint(0, 10),
                    'vehicles': random.randint(0, 5),
                    'incident_detected': incident is not None,
                },
                incident_detected=incident is not None,
                confidence_score=Decimal(random.uniform(70.0, 95.0)).quantize(Decimal('0.01')) if incident else None,
                manual_review_status=random.choice(['pending', 'reviewed', 'approved', 'rejected']),
            )
        
        # Create Sensors
        self.stdout.write(f'Creating {sensor_count} sensors...')
        sensors = []
        sensor_created = 0
        sensor_types = ['traffic_flow', 'weather', 'road_surface', 'air_quality', 'vibration']
        
        for i in range(sensor_count):
            sensor_type = random.choice(sensor_types)
            sensor_id = f"SENSOR-{sensor_type.upper()}-{i+1:04d}"
            
            # Check if sensor already exists
            sensor, created = Sensor.objects.get_or_create(
                sensor_id=sensor_id,
                defaults={
                    'latitude': Decimal('-1.2921'),
                    'longitude': Decimal('36.8219'),
                    'sensor_type': sensor_type,
                    'status': 'active',
                }
            )
            
            if created:
                lat, lng = random.choice(kenya_coordinates)
                lat = Decimal(str(lat)) + Decimal(str(random.uniform(-0.02, 0.02)))
                lng = Decimal(str(lng)) + Decimal(str(random.uniform(-0.02, 0.02)))
                
                lat = max(Decimal('-4.7'), min(Decimal('5.5'), lat))
                lng = max(Decimal('33.9'), min(Decimal('41.9'), lng))
                
                sensor.latitude = lat
                sensor.longitude = lng
                sensor.installation_date = timezone.now() - timedelta(days=random.randint(30, 730))
                sensor.manufacturer = random.choice(manufacturers)
                sensor.model = f"{random.choice(models)} Sensor"
                sensor.api_endpoint = f"https://api.kenha.ke/sensors/{i+1}/read"
                sensor.mqtt_topic = f"sensors/{sensor_type}_{i+1}"
                sensor.status = random.choice(['active', 'active', 'active', 'inactive', 'maintenance'])
                sensor.metadata = {
                    'calibration_date': (timezone.now() - timedelta(days=random.randint(0, 180))).isoformat(),
                    'battery_level': random.randint(20, 100),
                }
                sensor.save()
                sensor_created += 1
            else:
                self.stdout.write(self.style.WARNING(f'Sensor {sensor_id} already exists, skipping...'))
            
            sensors.append(sensor)
        
        # Create Sensor Readings
        self.stdout.write(f'Creating {readings_count} sensor readings...')
        reading_types_map = {
            'traffic_flow': ['vehicle_count', 'speed', 'occupancy'],
            'weather': ['temperature', 'humidity', 'wind_speed', 'precipitation'],
            'road_surface': ['temperature', 'moisture', 'roughness'],
            'air_quality': ['pm25', 'pm10', 'no2', 'co2'],
            'vibration': ['amplitude', 'frequency'],
        }
        
        for i in range(readings_count):
            sensor = random.choice(sensors)
            reading_time = timezone.now() - timedelta(
                hours=random.randint(0, 720),
                minutes=random.randint(0, 59)
            )
            
            reading_types = reading_types_map.get(sensor.sensor_type, ['value'])
            reading_type = random.choice(reading_types)
            
            # Generate appropriate value based on type
            if reading_type in ['temperature', 'road_surface']:
                value = Decimal(random.uniform(15.0, 35.0)).quantize(Decimal('0.1'))
                unit = 'celsius'
            elif reading_type in ['humidity']:
                value = Decimal(random.uniform(30.0, 90.0)).quantize(Decimal('0.1'))
                unit = 'percent'
            elif reading_type in ['speed', 'wind_speed']:
                value = Decimal(random.uniform(0.0, 50.0)).quantize(Decimal('0.1'))
                unit = 'km/h'
            elif reading_type in ['vehicle_count']:
                value = random.randint(0, 200)
                unit = 'count'
            elif reading_type in ['pm25', 'pm10']:
                value = Decimal(random.uniform(10.0, 150.0)).quantize(Decimal('0.1'))
                unit = 'ug/m3'
            else:
                value = Decimal(random.uniform(0.0, 100.0)).quantize(Decimal('0.1'))
                unit = 'unit'
            
            SensorReading.objects.create(
                sensor=sensor,
                timestamp=reading_time,
                reading_type=reading_type,
                value={'value': float(value)},
                unit=unit,
                quality_score=Decimal(random.uniform(80.0, 100.0)).quantize(Decimal('0.01')),
                anomaly_detected=random.choice([True, False]) if random.random() < 0.1 else False,
            )
        
        # Create Incident Validations (link IoT data to incidents)
        self.stdout.write('Creating incident validations...')
        incidents_with_location = list(Incident.objects.all()[:30])
        validation_sources = ['rfid', 'cctv', 'sensor', 'ai']
        
        for incident in incidents_with_location:
            # Create validations from different sources
            for source in random.sample(validation_sources, random.randint(1, 3)):
                IncidentValidation.objects.create(
                    incident=incident,
                    validation_source=source,
                    confidence_score=Decimal(random.uniform(65.0, 95.0)).quantize(Decimal('0.01')),
                    validation_status=random.choice(['pending', 'confirmed', 'confirmed', 'contradicted']),
                    source_data={
                        'source': source,
                        'timestamp': incident.timestamp.isoformat(),
                        'location': {
                            'lat': float(incident.latitude),
                            'lng': float(incident.longitude),
                        },
                    },
                    correlation_details={
                        'match_score': random.uniform(70.0, 95.0),
                        'time_diff_seconds': random.randint(0, 300),
                        'distance_meters': random.randint(0, 500),
                    },
                )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded IoT devices: {rfid_created} new RFID readers, {cctv_created} new CCTV cameras, '
            f'{sensor_created} new sensors, {logs_count} RFID logs, {readings_count} sensor readings'
        ))

