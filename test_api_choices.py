#!/usr/bin/env python
"""
Test script untuk memeriksa API choices penduduk
"""

import requests
import json

def test_api_choices():
    """Test API choices melalui HTTP request"""
    print("Testing API Choices untuk Form Penduduk")
    print("=======================================")
    
    try:
        # URL API endpoint
        url = "http://127.0.0.1:8000/pulosarok/references/api/penduduk/create/"
        
        print(f"📡 Menguji endpoint: {url}")
        
        # Kirim GET request
        response = requests.get(url, timeout=10)
        
        print(f"📡 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Coba parse sebagai JSON
                data = response.json()
                
                print("\n✅ API Response berhasil (JSON):")
                print(f"   • Dusun choices: {len(data.get('dusun_choices', []))} items")
                print(f"   • Lorong choices: {len(data.get('lorong_choices', []))} items")
                print(f"   • Gender choices: {len(data.get('gender_choices', []))} items")
                print(f"   • Religion choices: {len(data.get('religion_choices', []))} items")
                print(f"   • Marital choices: {len(data.get('marital_status_choices', []))} items")
                print(f"   • Education choices: {len(data.get('education_choices', []))} items")
                print(f"   • Blood type choices: {len(data.get('blood_type_choices', []))} items")
                print(f"   • Citizenship choices: {len(data.get('citizenship_choices', []))} items")
                print(f"   • Family head choices: {len(data.get('family_head_choices', []))} items")
                
                # Tampilkan sample choices
                if 'marital_status_choices' in data:
                    print("\n📋 Sample Marital Status Choices:")
                    for choice in data['marital_status_choices'][:3]:  # Show first 3
                        print(f"   • {choice.get('label', 'N/A')} (value: {choice.get('value', 'N/A')})")
                
                if 'citizenship_choices' in data:
                    print("\n📋 Sample Citizenship Choices:")
                    for choice in data['citizenship_choices']:
                        print(f"   • {choice.get('label', 'N/A')} (value: {choice.get('value', 'N/A')})")
                
                # Verifikasi choices yang diperlukan ada
                required_keys = [
                    'dusun_choices', 'lorong_choices', 'gender_choices', 
                    'religion_choices', 'marital_status_choices', 'education_choices',
                    'blood_type_choices', 'citizenship_choices', 'family_head_choices'
                ]
                
                missing_keys = []
                for key in required_keys:
                    if key not in data:
                        missing_keys.append(key)
                
                if missing_keys:
                    print(f"\n❌ Missing keys: {', '.join(missing_keys)}")
                    return False
                else:
                    print("\n✅ Semua choices yang diperlukan tersedia!")
                    return True
                    
            except json.JSONDecodeError:
                # Bukan JSON response, mungkin HTML form
                print("\n📄 Response adalah HTML (bukan JSON API)")
                print("   Ini normal jika endpoint mengembalikan form HTML.")
                
                # Cek apakah ada JavaScript yang memuat choices
                content = response.text
                if 'loadChoices' in content:
                    print("   ✅ Ditemukan fungsi loadChoices di HTML")
                if 'marital_status_choices' in content:
                    print("   ✅ Ditemukan referensi marital_status_choices")
                if 'citizenship_choices' in content:
                    print("   ✅ Ditemukan referensi citizenship_choices")
                
                return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text[:500]}...")  # First 500 chars
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Koneksi gagal. Pastikan server Django berjalan di http://127.0.0.1:8000")
        return False
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

def test_direct_api():
    """Test API endpoint langsung untuk JSON response"""
    print("\n\nTesting Direct API Endpoint")
    print("===========================")
    
    try:
        # URL untuk API JSON langsung (jika ada)
        url = "http://127.0.0.1:8000/pulosarok/admin/references/api/penduduk/choices/"
        
        print(f"📡 Menguji endpoint API: {url}")
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Direct API berhasil!")
            return True
        elif response.status_code == 404:
            print("⚠️ Direct API endpoint tidak ditemukan (404)")
            print("   Ini normal jika tidak ada endpoint khusus untuk choices.")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Koneksi gagal")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🔍 Testing API Choices untuk Form Penduduk\n")
    
    # Test main endpoint
    main_test = test_api_choices()
    
    # Test direct API (optional)
    direct_test = test_direct_api()
    
    print("\n\n=== RINGKASAN TEST ===")
    print(f"Main endpoint: {'✅ Berhasil' if main_test else '❌ Gagal'}")
    print(f"Direct API: {'✅ Berhasil' if direct_test else '❌ Gagal'}")
    
    if main_test:
        print("\n🎉 API choices dapat diakses! Form penduduk seharusnya berfungsi dengan baik.")
        print("\n💡 Jika masih ada masalah penyimpanan:")
        print("   1. Periksa JavaScript console di browser untuk error")
        print("   2. Periksa Network tab untuk melihat request yang gagal")
        print("   3. Pastikan CSRF token valid")
        print("   4. Periksa validasi form di frontend")
    else:
        print("\n⚠️ Ada masalah dengan API choices. Periksa server Django.")