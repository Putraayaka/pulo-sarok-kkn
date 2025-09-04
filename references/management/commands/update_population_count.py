from django.core.management.base import BaseCommand
from references.models import Dusun


class Command(BaseCommand):
    help = 'Update population count for all dusun based on active residents'

    def handle(self, *args, **options):
        self.stdout.write('Starting population count update...')
        
        updated_count = 0
        for dusun in Dusun.objects.all():
            old_count = dusun.population_count
            dusun.update_population_count()
            new_count = dusun.population_count
            
            if old_count != new_count:
                self.stdout.write(
                    f'Updated {dusun.name}: {old_count} -> {new_count}'
                )
                updated_count += 1
            else:
                self.stdout.write(
                    f'No change for {dusun.name}: {new_count}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} dusun population counts'
            )
        )