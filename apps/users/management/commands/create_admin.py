from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class Command(BaseCommand):
    help = 'Create an admin user for Global Cool-Light admin dashboard'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Admin email address')
        parser.add_argument('--password', type=str, help='Admin password')
        parser.add_argument('--first-name', type=str, help='Admin first name')
        parser.add_argument('--last-name', type=str, help='Admin last name')

    def handle(self, *args, **options):
        email = options.get('email') or input('Enter admin email: ')
        first_name = options.get('first_name') or input('Enter first name: ')
        last_name = options.get('last_name') or input('Enter last name: ')
        
        if options.get('password'):
            password = options['password']
        else:
            import getpass
            password = getpass.getpass('Enter password: ')
            password_confirm = getpass.getpass('Confirm password: ')
            
            if password != password_confirm:
                self.stdout.write(
                    self.style.ERROR('Passwords do not match!')
                )
                return

        # Validate password
        try:
            validate_password(password)
        except ValidationError as e:
            self.stdout.write(
                self.style.ERROR(f'Password validation failed: {", ".join(e.messages)}')
            )
            return

        # Check if user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(f'User with email {email} already exists!')
            )
            return

        # Create username from email
        username = email.split('@')[0]
        counter = 1
        original_username = username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Create admin user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_staff=True,
                is_superuser=True
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully created admin user: {user.email} (username: {user.username})'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'You can now login at: http://127.0.0.1:8001/users/admin/login/'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )
