"""
Django management command to toggle microservices on/off
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Toggle microservices on/off'

    def add_arguments(self, parser):
        parser.add_argument(
            '--enable',
            action='store_true',
            help='Enable microservices',
        )
        parser.add_argument(
            '--disable',
            action='store_true',
            help='Disable microservices (use local database)',
        )
        parser.add_argument(
            '--status',
            action='store_true',
            help='Show current status',
        )

    def handle(self, *args, **options):
        settings_file = os.path.join(settings.BASE_DIR, 'SvoiCode', 'settings.py')
        
        if options['status']:
            current_status = getattr(settings, 'USE_MICROSERVICES', True)
            self.stdout.write(
                self.style.SUCCESS(f"Microservices are currently: {'✅ Enabled' if current_status else '❌ Disabled'}")
            )
            return
        
        if options['enable'] and options['disable']:
            self.stdout.write(
                self.style.ERROR('Cannot both enable and disable microservices. Choose one.')
            )
            return
        
        if not options['enable'] and not options['disable']:
            self.stdout.write(
                self.style.ERROR('Please specify --enable or --disable')
            )
            return
        
        # Read current settings file
        try:
            with open(settings_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Settings file not found: {settings_file}')
            )
            return
        
        # Determine new value
        if options['enable']:
            new_value = 'True'
            action = 'enabled'
        else:
            new_value = 'False'
            action = 'disabled'
        
        # Update the setting
        import re
        pattern = r'USE_MICROSERVICES\s*=\s*(True|False)'
        replacement = f'USE_MICROSERVICES = {new_value}'
        
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
        else:
            # Add the setting if it doesn't exist
            new_content = content + f'\n\n# Microservices toggle\nUSE_MICROSERVICES = {new_value}\n'
        
        # Write back to file
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            self.stdout.write(
                self.style.SUCCESS(f'✅ Microservices {action} successfully!')
            )
            self.stdout.write(
                self.style.WARNING('⚠️  You need to restart the Django server for changes to take effect.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Failed to update settings: {e}')
            )
