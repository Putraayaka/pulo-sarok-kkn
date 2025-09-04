#!/usr/bin/env python
# Test script untuk verifikasi endpoint API

import requests
import json
from datetime import datetime

def test_endpoint(url, description):
    """Test single endpoint and return status"""
    try:
        response = requests.get(url, timeout=10)
        status = "✓ PASS" if response.status_code == 200 else f"✗ FAIL ({response.status_code})"
        print(f"{status} - {description}: {url}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"✗ ERROR - {description}: {url} - {str(e)}")
        return False

def main():
    print("=" * 60)
    print("TESTING PULO SAROK ENDPOINTS")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test endpoints
    endpoints = [
        # Main pages
        (f"{base_url}/", "Homepage"),
        (f"{base_url}/admin/", "Admin Login"),
        
        # Public API endpoints
        (f"{base_url}/public/api/news/", "Public News API"),
        (f"{base_url}/public/api/village-profile/", "Village Profile API"),
        (f"{base_url}/public/api/contact/", "Contact API"),
        
        # Admin module endpoints (corrected URLs)
        (f"{base_url}/pulosarok/business/business-view/", "Business Management View"),
        (f"{base_url}/pulosarok/letters/letters-view/", "Letters Management View"),
        (f"{base_url}/pulosarok/documents/documents-view/", "Documents Management View"),
        (f"{base_url}/pulosarok/references/references-view/", "References Management View"),
        
        # Organization API
        (f"{base_url}/pulosarok/organization/perangkat-desa/", "Perangkat Desa API"),
        
        # News module
        (f"{base_url}/pulosarok/news/", "News Module"),
        
        # Tourism API
        (f"{base_url}/pulosarok/tourism/api/destinations/", "Tourism Destinations API"),
        
        # Business API
        (f"{base_url}/pulosarok/business/api/businesses/", "Business Units API"),
        
        # Additional Business endpoints
        (f"{base_url}/pulosarok/business/api/koperasi/", "Koperasi API"),
        (f"{base_url}/pulosarok/business/api/bumg/", "BUMG API"),
        (f"{base_url}/pulosarok/business/api/ukm/admin/", "UKM Admin API"),
    ]
    
    passed = 0
    total = len(endpoints)
    
    print("\nTesting endpoints...\n")
    
    for url, description in endpoints:
        if test_endpoint(url, description):
            passed += 1
        print()  # Empty line for readability
    
    print("=" * 60)
    print(f"HASIL TEST: {passed}/{total} endpoints berhasil")
    print(f"Success Rate: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 Semua endpoint berfungsi dengan baik!")
    elif passed > total * 0.7:
        print("⚠️  Sebagian besar endpoint berfungsi, ada beberapa yang perlu diperbaiki")
    else:
        print("❌ Banyak endpoint yang bermasalah, perlu investigasi lebih lanjut")
    
    print("=" * 60)

if __name__ == "__main__":
    main()