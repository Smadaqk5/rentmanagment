from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a landlord user for the rental management system'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Username for the landlord')
        parser.add_argument('--email', type=str, help='Email for the landlord')
        parser.add_argument('--password', type=str, help='Password for the landlord')

    def handle(self, *args, **options):
        username = options['username'] or 'landlord'
        email = options['email'] or 'landlord@example.com'
        password = options['password'] or 'landlord123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created landlord user: {username}')
        )
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Email: {email}')
        self.stdout.write(f'Password: {password}')
