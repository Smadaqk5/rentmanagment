from django.core.management.base import BaseCommand
from django.utils import timezone
from rental_app.models import Tenant
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Update tenant payment statuses based on due dates and overdue periods'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days after due date to mark as overdue (default: 30)'
        )

    def handle(self, *args, **options):
        days_overdue = options['days']
        self.stdout.write(f'Updating payment statuses (overdue after {days_overdue} days)...')
        
        updated_count = 0
        overdue_count = 0
        
        for tenant in Tenant.objects.all():
            old_status = tenant.rent_status
            
            # Update status based on current state
            tenant.update_status()
            
            # Check if tenant should be marked as overdue
            if tenant.rent_status != 'Paid' and tenant.is_overdue():
                # Check if it's been more than the specified days since due date
                next_due = tenant.get_next_due_date()
                days_since_due = (timezone.now().date() - next_due.date()).days
                
                if days_since_due >= days_overdue:
                    tenant.rent_status = 'Overdue'
                    tenant.save()
                    overdue_count += 1
                    self.stdout.write(
                        f'Marked {tenant.name} as overdue (due: {next_due.date()}, {days_since_due} days late)'
                    )
            
            if old_status != tenant.rent_status:
                updated_count += 1
                self.stdout.write(
                    f'Updated {tenant.name}: {old_status} -> {tenant.rent_status}'
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully updated {updated_count} tenants. {overdue_count} marked as overdue.'
            )
        )
