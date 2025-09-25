from django.core.management.base import BaseCommand
from rental_app.models import Tenant


class Command(BaseCommand):
    help = 'Reset all paid tenants for new month - add full rent to amount due'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm the reset operation'
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will reset all paid tenants for the new month. '
                    'Use --confirm to proceed.'
                )
            )
            return

        paid_tenants = Tenant.objects.filter(rent_status='Paid')
        reset_count = 0

        for tenant in paid_tenants:
            tenant.reset_for_new_month()
            reset_count += 1
            self.stdout.write(f'Reset {tenant.name} for new month')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully reset {reset_count} tenants for new month.'
            )
        )
