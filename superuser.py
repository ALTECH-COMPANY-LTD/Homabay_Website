import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.core.management import call_command

def create_superuser(username, email, password):
    User = get_user_model()
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f'Superuser {username} created successfully.')
    else:
        print(f'Superuser {username} already exists.')

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python create_superuser.py <username> <email> <password>")
    else:
        username, email, password = sys.argv[1], sys.argv[2], sys.argv[3]
        create_superuser(username, email, password)