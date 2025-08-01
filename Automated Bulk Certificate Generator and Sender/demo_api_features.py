#!/usr/bin/env python3
"""
Demo script showing the enhanced API integration features
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.append('src')

def demo_dynamic_certificate_fetching():
    """Demonstrate dynamic certificate details fetching"""
    print("🎯 DYNAMIC CERTIFICATE DETAILS FETCHING DEMO")
    print("=" * 60)
    
    from automations.certificate_api import CertificateAPI, push_certificate_to_web_service
    from automations.send_same_email import get_recipient_details
    
    # Create a test certificate in the API
    print("1️⃣ Creating test certificate in web service...")
    test_id = f"DEMO-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    recipient_name = "John Demo Student"
    course_name = "Advanced Web Development"
    
    result = push_certificate_to_web_service(
        cert_id=test_id,
        recipient_name=recipient_name,
        course_name=course_name
    )
    
    if result.get('success'):
        print(f"✅ Created certificate: {test_id}")
        print(f"   Recipient: {recipient_name}")
        print(f"   Course: {course_name}")
        print(f"   Issue Date: {datetime.now().strftime('%Y-%m-%d')}")
    else:
        print(f"❌ Failed to create certificate: {result.get('message')}")
        return
    
    print("\n2️⃣ Demonstrating dynamic lookup...")
    
    # Demonstrate getting details with API enabled
    print(f"\n🔍 Looking up details for '{recipient_name}' with API enabled:")
    course, cert_id = get_recipient_details(recipient_name, use_api=True)
    print(f"   Course Name: {course}")
    print(f"   Certificate ID: {cert_id}")
    
    # Show how this would be used in email template
    print("\n3️⃣ Email template personalization example:")
    email_template = """
Dear {name},

Congratulations! You have successfully completed the {course_name} course.

Your certificate ID is: {cert_id}

You can verify your certificate online at:
https://verify.devopsacademy.online/validate/user_portal/

Best regards,
The Training Team
"""
    
    personalized_email = email_template.format(
        name=recipient_name,
        course_name=course,
        cert_id=cert_id
    )
    
    print("📧 Personalized email content:")
    print("-" * 40)
    print(personalized_email)
    print("-" * 40)
    
    print("\n4️⃣ Key benefits of this integration:")
    print("✅ Automatic certificate registration before email sending")
    print("✅ Dynamic field population using real certificate data")
    print("✅ Current date automatically set as issue_date")
    print("✅ Recipients can verify certificates online immediately")
    print("✅ Fallback to local files if API is unavailable")
    print("✅ Retry logic for robust operation")
    

def demo_api_configuration():
    """Demonstrate API configuration management"""
    print("\n\n🔧 API CONFIGURATION MANAGEMENT DEMO")
    print("=" * 60)
    
    from automations.certificate_api import load_api_config, CertificateAPI
    
    print("1️⃣ Current API configuration:")
    config = load_api_config()
    
    print(f"   API Enabled: {config.get('api_enabled', False)}")
    print(f"   Base URL: {config.get('api_base_url', 'Not configured')}")
    print(f"   Default Expiry: {config.get('default_expiry_years', 3)} years")
    print(f"   Timeout: {config.get('timeout_seconds', 30)} seconds")
    print(f"   Retry Attempts: {config.get('retry_attempts', 2)}")
    
    print("\n2️⃣ Testing API connection:")
    api = CertificateAPI()
    
    if api.is_enabled():
        if api.test_connection():
            print("✅ API connection successful!")
        else:
            print("❌ API connection failed!")
    else:
        print("⚠️  API integration is disabled")
    
    print("\n3️⃣ Configuration management:")
    print("   📁 Config file: data/emails/api_config.json")
    print("   🎛️  Interactive menu: python start.py → Option 7")
    print("   🧪 Test suite: python test_api_integration.py")


def demo_workflow():
    """Demonstrate the complete workflow"""
    print("\n\n🔄 COMPLETE WORKFLOW DEMO")
    print("=" * 60)
    
    print("📋 Typical workflow with API integration:")
    print()
    print("1️⃣ Generate certificates:")
    print("   • Unique 20-character IDs auto-generated")
    print("   • Certificate details logged locally")
    print("   • PDF files created in output folder")
    print()
    print("2️⃣ Send emails with API integration:")
    print("   • For each recipient:")
    print("     - Lookup certificate details (API first, then local)")
    print("     - Register certificate in web service")
    print("     - Set current date as issue_date")
    print("     - Personalize email with {name}, {course_name}, {cert_id}")
    print("     - Send email with certificate attachment")
    print()
    print("3️⃣ Certificate verification:")
    print("   • Recipients receive certificates immediately")
    print("   • Can verify online at web portal")
    print("   • Admin can manage via dashboard")
    print()
    print("✨ Benefits:")
    print("   • Seamless integration with external validation service")
    print("   • Real-time certificate verification")
    print("   • Professional certificate management")
    print("   • Robust error handling and fallbacks")


def main():
    """Run all demos"""
    try:
        demo_dynamic_certificate_fetching()
        demo_api_configuration()
        demo_workflow()
        
        print("\n\n🎉 DEMO COMPLETE!")
        print("=" * 60)
        print("Ready to use the enhanced API integration features!")
        print()
        print("📚 Next steps:")
        print("• Run: python start.py (Interactive menu)")
        print("• Test: python test_api_integration.py")
        print("• Read: API_GUIDE.md (Complete API documentation)")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
        print("Make sure all dependencies are installed and API is accessible.")


if __name__ == "__main__":
    main()
