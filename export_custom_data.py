#!/usr/bin/env python
import os
import django
from django.core.management import call_command
from django.apps import apps
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

def export_custom_data():
    """
    Export only custom app data, excluding Django's built-in models
    that are automatically created during migrations.
    """
    print("🚀 Starting custom data export...")
    
    # Define custom apps (exclude Django built-in apps)
    custom_apps = [
        'beneficiaries',
        'business', 
        'core',
        'documents',
        'events',
        'letters',
        'news',
        'organization',
        'posyandu',
        'references',
        'village_profile'
    ]
    
    print(f"📋 Exporting data from {len(custom_apps)} custom apps...")
    
    try:
        # Create the export command - only custom apps
        apps_to_export = custom_apps
        
        with open('custom_data_export.json', 'w', encoding='utf-8') as f:
            call_command(
                'dumpdata',
                *apps_to_export,
                format='json',
                indent=2,
                stdout=f
            )
        
        print("✅ Custom data exported successfully to 'custom_data_export.json'")
        
        # Check file size
        file_size = os.path.getsize('custom_data_export.json')
        print(f"📊 Export file size: {file_size:,} bytes")
        
        # Count records
        with open('custom_data_export.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"📈 Total records exported: {len(data)}")
            
            # Show breakdown by app
            app_counts = {}
            for record in data:
                model = record['model']
                app_name = model.split('.')[0]
                app_counts[app_name] = app_counts.get(app_name, 0) + 1
            
            print("\n📋 Records by app:")
            for app, count in sorted(app_counts.items()):
                print(f"   • {app}: {count} records")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during export: {e}")
        return False

if __name__ == "__main__":
    print("📦 Custom Data Export Tool")
    print("==========================\n")
    
    if export_custom_data():
        print("\n🎉 Export completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Use 'python reset_database.py' to reset the database")
        print("   2. Load custom data: python manage.py loaddata custom_data_export.json")
        print("\n💡 This export excludes Django built-in models that are")
        print("   automatically created during migrations, preventing conflicts.")
    else:
        print("\n❌ Export failed. Please check the error messages above.")