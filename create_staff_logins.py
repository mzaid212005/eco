import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecologic.settings')
django.setup()

from django.contrib.auth.models import User
from issues.models import UserProfile

def create_staff_logins():
    # Handle first staff user
    user1, created1 = User.objects.get_or_create(
        username='staff1',
        defaults={
            'password': 'password123',
            'email': 'staff1@example.com',
            'first_name': 'Staff',
            'last_name': 'One',
            'is_staff': True,
            'is_active': True
        }
    )
    if created1:
        user1.set_password('password123')  # Ensure password is hashed
        user1.save()
        print("Created staff user: staff1")
    else:
        print("Staff user staff1 already exists")

    # Ensure UserProfile exists for staff1
    profile1, profile_created1 = UserProfile.objects.get_or_create(
        user=user1,
        defaults={'role': 'Staff'}
    )
    if profile_created1:
        print("Created UserProfile for staff1")
    else:
        profile1.role = 'Staff'
        profile1.save()
        print("Updated UserProfile for staff1")

    # Handle second staff user
    user2, created2 = User.objects.get_or_create(
        username='staff2',
        defaults={
            'password': 'password123',
            'email': 'staff2@example.com',
            'first_name': 'Staff',
            'last_name': 'Two',
            'is_staff': True,
            'is_active': True
        }
    )
    if created2:
        user2.set_password('password123')  # Ensure password is hashed
        user2.save()
        print("Created staff user: staff2")
    else:
        print("Staff user staff2 already exists")

    # Ensure UserProfile exists for staff2
    profile2, profile_created2 = UserProfile.objects.get_or_create(
        user=user2,
        defaults={'role': 'Staff'}
    )
    if profile_created2:
        print("Created UserProfile for staff2")
    else:
        profile2.role = 'Staff'
        profile2.save()
        print("Updated UserProfile for staff2")

if __name__ == '__main__':
    create_staff_logins()