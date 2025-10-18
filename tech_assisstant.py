#!/usr/bin/env python3
"""
Test script for System Diagnostic Assistant
Run this to verify everything works before the demo
"""

import requests
import json
import time

API_BASE = "http://localhost:5000"

def test_health():
    """Test if backend is running"""
    print("\n🔍 Testing backend health...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print("❌ Backend returned error:", response.status_code)
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to backend: {e}")
        print("   Make sure to run: python app.py")
        return False

def test_system_info():
    """Test system info endpoint"""
    print("\n🔍 Testing system info collection...")
    try:
        response = requests.get(f"{API_BASE}/api/system-info", timeout=10)
        data = response.json()
        
        if data.get('success'):
            print("✅ System info collected successfully")
            print(f"   OS: {data['system']['os']}")
            print(f"   Platform: {data['system']['platform']}")
            print(f"   CPU: {data['resources']['cpu_percent']}%")
            print(f"   Memory: {data['resources']['memory_percent']:.1f}%")
            return True
        else:
            print("❌ Failed to get system info")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_diagnosis():
    """Test the main diagnosis endpoint"""
    print("\n🔍 Testing AI diagnosis (this will take 15-30 seconds)...")
    
    test_problem = "I'm getting a 'command not found' error when trying to run npm"
    
    try:
        response = requests.post(
            f"{API_BASE}/api/diagnose",
            json={
                "problem": test_problem,
                "commands": ["npm", "node", "nvm"]
            },
            timeout=60
        )
        
        data = response.json()
        
        if data.get('success'):
            print("✅ Diagnosis completed successfully")
            print(f"\n📊 Results:")
            print(f"   Problem: {data['problem']}")
            print(f"   System: {data['system_info']['os']}")
            print(f"   Tokens used: {data['token_usage']['input_tokens'] + data['token_usage']['output_tokens']}")
            print(f"\n📝 Analysis preview (first 200 chars):")
            print(f"   {data['diagnosis'][:200]}...")
            return True
        else:
            print("❌ Diagnosis failed:", data.get('error'))
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("="*60)
    print("🛠️  SYSTEM DIAGNOSTIC ASSISTANT - TEST SUITE")
    print("="*60)
    
    # Run tests
    health_ok = test_health()
    if not health_ok:
        print("\n⚠️  Backend is not running. Start it first with: python app.py")
        return
    
    time.sleep(1)
    
    info_ok = test_system_info()
    time.sleep(1)
    
    diag_ok = test_diagnosis()
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"System Info:  {'✅ PASS' if info_ok else '❌ FAIL'}")
    print(f"AI Diagnosis: {'✅ PASS' if diag_ok else '❌ FAIL'}")
    
    if health_ok and info_ok and diag_ok:
        print("\n🎉 All tests passed! System is ready for demo.")
        print("\n📝 Next steps:")
        print("   1. Open frontend/index.html in your browser")
        print("   2. Try describing a real technical problem")
        print("   3. Watch it analyze your actual system state!")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()