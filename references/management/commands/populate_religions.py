from django.core.management.base import BaseCommand
from references.models import ReligionReference

class Command(BaseCommand):
    help = 'Populate default religion data'

    def handle(self, *args, **options):
        religions = [
            {'name': 'Islam', 'code': 'ISL'},
            {'name': 'Kristen Protestan', 'code': 'KRP'},
            {'name': 'Kristen Katolik', 'code': 'KRK'},
            {'name': 'Hindu', 'code': 'HND'},
            {'name': 'Buddha', 'code': 'BUD'},
            {'name': 'Konghucu', 'code': 'KHU'},
            {'name': 'Kepercayaan', 'code': 'KPC'},
        ]
        
        for religion_data in religions:
            religion, created = ReligionReference.objects.get_or_create(
                code=religion_data['code'],
                defaults={'name': religion_data['name']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created religion: {religion.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Religion already exists: {religion.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated religion data')
        )