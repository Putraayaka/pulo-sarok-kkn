#!/usr/bin/env python
import json
import os

def filter_custom_data():
    """
    Filter the original data_export.json to only include custom app data,
    excluding Django built-in models that cause conflicts.
    """
    print("🔍 Filtering custom data from data_export.json...")
    
    # Check if source file exists
    if not os.path.exists('data_export.json'):
        print("❌ data_export.json not found!")
        return False
    
    # Define custom apps to include
    custom_apps = {
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
    }
    
    # Also include some user-created data from Django apps
    allowed_models = {
        'auth.user',  # User accounts
        'auth.group',  # User groups (if any custom ones)
    }
    
    try:
        # Load the original data
        with open('data_export.json', 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        print(f"📊 Original data contains {len(all_data)} records")
        
        # Filter data
        filtered_data = []
        app_counts = {}
        
        for record in all_data:
            model = record['model']
            app_name = model.split('.')[0]
            
            # Include if it's from a custom app or an allowed model
            if app_name in custom_apps or model in allowed_models:
                filtered_data.append(record)
                app_counts[model] = app_counts.get(model, 0) + 1
        
        # Save filtered data
        with open('filtered_custom_data.json', 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Filtered data saved to 'filtered_custom_data.json'")
        print(f"📈 Filtered data contains {len(filtered_data)} records")
        
        # Show breakdown
        if app_counts:
            print("\n📋 Records by model:")
            for model, count in sorted(app_counts.items()):
                print(f"   • {model}: {count} records")
        else:
            print("\n📋 No custom data found in the export")
        
        # Check file size
        file_size = os.path.getsize('filtered_custom_data.json')
        print(f"📊 Filtered file size: {file_size:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during filtering: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Custom Data Filter Tool")
    print("===========================\n")
    
    if filter_custom_data():
        print("\n🎉 Filtering completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Load filtered data: python manage.py loaddata filtered_custom_data.json")
        print("   2. This should load without conflicts since Django built-in models are excluded")
        print("\n💡 The filtered file contains only your custom application data.")
    else:
        print("\n❌ Filtering failed. Please check the error messages above.")