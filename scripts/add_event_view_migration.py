#!/usr/bin/env python3
"""
Script to create and run migration for EventView model
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
    print("Creating migration for EventView model...")

    try:
        # Create migration
        execute_from_command_line(['manage.py', 'makemigrations', 'events'])
        print("✅ Migration created successfully!")

        # Apply migration
        print("Applying migration...")
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migration applied successfully!")

        print("\n🎉 EventView model has been created!")
        print("The system can now track which events users have viewed.")

    except Exception as e:
        print(f"❌ Error: {e}")
        return False

    return True


if __name__ == '__main__':
    main()
