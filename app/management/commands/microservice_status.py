"""
Django management command to check microservice status
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from app.services.service_manager import service_manager


class Command(BaseCommand):
    help = 'Check status of all microservices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--detailed',
            action='store_true',
            help='Show detailed status information',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🔍 Checking microservice status...\n')
        )
        
        # Check if microservices are enabled
        use_microservices = getattr(settings, 'USE_MICROSERVICES', True)
        self.stdout.write(f"Microservices enabled: {'✅ Yes' if use_microservices else '❌ No'}")
        
        if not use_microservices:
            self.stdout.write(
                self.style.WARNING('Microservices are disabled. Using local database only.')
            )
            return
        
        # Get service status
        if options['detailed']:
            status = service_manager.get_service_status()
            self.stdout.write('\n📊 Detailed Service Status:')
            self.stdout.write('=' * 50)
            
            for service_name, info in status.items():
                status_icon = '✅' if info['healthy'] else '❌'
                self.stdout.write(f"{status_icon} {service_name}")
                self.stdout.write(f"   URL: {info['url']}")
                self.stdout.write(f"   Available: {'Yes' if info['available'] else 'No'}")
                self.stdout.write(f"   Healthy: {'Yes' if info['healthy'] else 'No'}")
                self.stdout.write()
        else:
            health_status = service_manager.health_check_all()
            self.stdout.write('\n🏥 Service Health:')
            self.stdout.write('=' * 30)
            
            for service_name, is_healthy in health_status.items():
                status_icon = '✅' if is_healthy else '❌'
                self.stdout.write(f"{status_icon} {service_name}")
        
        # Summary
        health_status = service_manager.health_check_all()
        healthy_count = sum(health_status.values())
        total_count = len(health_status)
        
        self.stdout.write(f'\n📈 Summary: {healthy_count}/{total_count} services healthy')
        
        if healthy_count == total_count:
            self.stdout.write(
                self.style.SUCCESS('🎉 All services are healthy!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠️  {total_count - healthy_count} service(s) are unhealthy')
            )
