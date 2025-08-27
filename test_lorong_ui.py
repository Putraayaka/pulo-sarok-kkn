import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
django.setup()

from references.models import Dusun, Lorong
from references.forms import LorongForm

try:
    # Get first dusun
    dusun = Dusun.objects.first()
    print(f'Found dusun: {dusun}')
    
    if not dusun:
        print('No dusun found in database')
        exit(1)
    
    # Test form data
    form_data = {
        'name': 'Test Lorong UI',
        'dusun': dusun.id,
        'description': 'Test from UI functionality'
    }
    
    # Create and validate form
    form = LorongForm(form_data)
    print(f'Form valid: {form.is_valid()}')
    
    if form.is_valid():
        # Save lorong
        lorong = form.save()
        print(f'Created lorong: {lorong.name} in {lorong.dusun.name}')
        
        # Check if it exists in database
        saved_lorong = Lorong.objects.filter(name='Test Lorong UI').first()
        if saved_lorong:
            print(f'Lorong successfully saved to database with ID: {saved_lorong.id}')
            # Clean up
            saved_lorong.delete()
            print('Test lorong deleted successfully')
        else:
            print('ERROR: Lorong not found in database after save')
    else:
        print(f'Form errors: {form.errors}')
        
except Exception as e:
    print(f'Error occurred: {e}')
    import traceback
    traceback.print_exc()