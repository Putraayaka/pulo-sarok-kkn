#!/usr/bin/env python
import os
import django
from django.conf import settings
from django.db import connection
from django.core.management import execute_from_command_line
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

def reset_database():
    """
    Reset the database by dropping all tables and recreating them.
    This is useful when you have data conflicts during loaddata.
    """
    print("🔄 Starting database reset...")
    
    try:
        with connection.cursor() as cursor:
            # Get all table names
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE schemaname = 'public'
            """)
            tables = cursor.fetchall()
            
            if tables:
                print(f"📋 Found {len(tables)} tables to drop")
                
                # Disable foreign key checks
                cursor.execute("SET session_replication_role = replica;")
                
                # Drop all tables
                for table in tables:
                    table_name = table[0]
                    print(f"🗑️  Dropping table: {table_name}")
                    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}" CASCADE')
                
                # Re-enable foreign key checks
                cursor.execute("SET session_replication_role = DEFAULT;")
                
                print("✅ All tables dropped successfully")
            else:
                print("ℹ️  No tables found to drop")
                
    except Exception as e:
        print(f"❌ Error during table dropping: {e}")
        return False
    
    # Run migrations to recreate tables
    print("🔧 Running migrations to recreate database structure...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Database structure recreated successfully")
        return True
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        return False

def load_data():
    """
    Load the exported data into the clean database.
    """
    print("📥 Loading data from data_export.json...")
    try:
        execute_from_command_line(['manage.py', 'loaddata', 'data_export.json'])
        print("✅ Data loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Error during data loading: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Database Reset and Data Import Tool")
    print("=====================================\n")
    
    # Check if data_export.json exists
    if not os.path.exists('data_export.json'):
        print("❌ data_export.json not found!")
        print("Please run export_data.py first to create the data export.")
        sys.exit(1)
    
    # Ask for confirmation
    response = input("⚠️  This will DELETE ALL DATA in your Supabase database. Continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Operation cancelled")
        sys.exit(0)
    
    # Reset database
    if reset_database():
        print("\n" + "="*50)
        
        # Ask if user wants to load data
        load_response = input("📥 Load data from data_export.json? (yes/no): ")
        if load_response.lower() == 'yes':
            if load_data():
                print("\n🎉 Database reset and data import completed successfully!")
                print("\n📋 Summary:")
                print("   • Database tables dropped and recreated")
                print("   • Data imported from data_export.json")
                print("   • Ready for team collaboration")
            else:
                print("\n⚠️  Database reset completed, but data loading failed.")
                print("You can manually run: python manage.py loaddata data_export.json")
        else:
            print("\n✅ Database reset completed.")
            print("You can load data later with: python manage.py loaddata data_export.json")
    else:
        print("\n❌ Database reset failed. Please check the error messages above.")
        sys.exit(1)