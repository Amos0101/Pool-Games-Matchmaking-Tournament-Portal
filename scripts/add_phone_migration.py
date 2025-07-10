#!/usr/bin/env python3
"""
Script to create and run migration for adding phone_number field to User model
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pool_portal.settings')
django.setup()

from django.core.management import execute_from_command_line


def main():
    print("Creating migration for phone_number field...")

    try:
        # Create migration
        execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
        print("✅ Migration created successfully!")

        # Apply migration
        print("Applying migration...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migration applied successfully!")

        print("\n🎉 Phone number field has been added to the User model!")
        print("Users can now add their phone numbers during registration.")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


if __name__ == '__main__':
    main()
