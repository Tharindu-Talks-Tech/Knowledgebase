#!/usr/bin/env python3
"""
Interactive Menu System for Automations
Run with: python start.py
"""

import os
import sys
import subprocess
from pathlib import Path

def get_safe_char(unicode_char, fallback):
    """Get Unicode character with fallback for Windows console encoding issues"""
    try:
        # Test if the character can be encoded/displayed
        unicode_char.encode(sys.stdout.encoding or 'utf-8')
        return unicode_char
    except (UnicodeEncodeError, AttributeError):
        return fallback

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print the application header"""
    rocket = get_safe_char("🚀", ">>")
    print("=" * 60)
    print(f"{rocket} AUTOMATION CONTROL CENTER")
    print("=" * 60)
    print("Welcome to the Certificate & Email Automation System")
    print("-" * 60)

def print_main_menu():
    """Print the main menu options"""
    print("\n📋 Main Menu:")
    print("1️⃣  Generate Certificates")
    print("2️⃣  Send Certificates via Email")
    print("3️⃣  Generate Contact Cards from Phone Numbers")
    print("4️⃣  View System Status")
    print("5️⃣  Help & Documentation")
    print("6️⃣  Delete All Generated Certificates")
    print("7️⃣  API Configuration")
    print("9️⃣  Debug Certificate Generation")
    print("0️⃣  Exit")
    print("-" * 60)

def check_files_exist():
    """Check if required files exist"""
    status = {
        "certificates_config": Path("data/certificates/config.json").exists(),
        "certificates_recipients": Path("data/certificates/recipients.txt").exists(),
        "email_config": Path("data/emails/email_config.json").exists(),
        "email_list": Path("data/emails/email_list.csv").exists(),
        "email_template": Path("data/emails/email.txt").exists()
    }
    return status

def show_system_status():
    """Show system status and file availability"""
    clear_screen()
    print_header()
    print("\n📊 System Status:")
    print("-" * 40)
    
    status = check_files_exist()
    
    print(f"📄 Certificate Config:     {'✅' if status['certificates_config'] else '❌'}")
    print(f"👥 Certificate Recipients: {'✅' if status['certificates_recipients'] else '❌'}")
    print(f"📧 Email Configuration:    {'✅' if status['email_config'] else '❌'}")
    print(f"📋 Email List (CSV):       {'✅' if status['email_list'] else '❌'}")
    print(f"📝 Email Template:         {'✅' if status['email_template'] else '❌'}")
    
    # Check for generated certificates
    cert_output_dir = Path("data/certificates/output")
    if cert_output_dir.exists():
        cert_files = list(cert_output_dir.glob("*.pdf"))
        print(f"📜 Generated Certificates: {len(cert_files)} files")
    else:
        print(f"📜 Generated Certificates: 0 files")
    
    # Check API status
    print("\n🌐 Certificate Validator API:")
    print("-" * 40)
    api_status = check_api_status()
    
    if api_status.get('config_exists'):
        print(f"⚙️  API Config:             {'✅' if api_status['config_exists'] else '❌'}")
        print(f"🔌 API Enabled:            {'✅' if api_status['enabled'] else '❌'}")
        print(f"🌐 API Connection:         {'✅' if api_status['connected'] else '❌'}")
        print(f"🔗 API Base URL:           {api_status['base_url']}")
        
        if not api_status['enabled']:
            print("   ℹ️  API integration is disabled")
        elif not api_status['connected']:
            print("   ⚠️  Cannot connect to API service")
    else:
        print(f"⚙️  API Config:             ❌")
        print(f"   Error: {api_status.get('error', 'Unknown error')}")
    
    print("\n💡 Tips:")
    if not status['certificates_recipients']:
        print("   - Add recipients to data/certificates/recipients.txt")
    if not status['email_list']:
        print("   - Add email addresses to data/emails/email_list.csv")
    if not status['email_config']:
        print("   - Configure email settings in data/emails/email_config.json")
    if api_status.get('enabled') and not api_status.get('connected'):
        print("   - Check internet connection and API settings")
    
    input("\n🔙 Press Enter to return to main menu...")

def debug_certificate_generation():
    """Debug certificate generation with detailed output"""
    print("\n🔍 Debug Mode - Certificate Generation")
    print("-" * 50)
    
    # Check all required components
    print("📁 Checking file structure...")
    
    config_path = Path("data/certificates/config.json")
    recipients_path = Path("data/certificates/recipients.txt")
    template_dir = Path("data/certificates/templates")
    output_dir = Path("data/certificates/output")
    
    print(f"   Config file: {'OK' if config_path.exists() else 'MISSING'} {config_path}")
    print(f"   Recipients file: {'OK' if recipients_path.exists() else 'MISSING'} {recipients_path}")
    print(f"   Templates directory: {'OK' if template_dir.exists() else 'MISSING'} {template_dir}")
    print(f"   Output directory: {'OK' if output_dir.exists() else 'MISSING'} {output_dir}")
    
    if template_dir.exists():
        template_files = list(template_dir.glob("*.pdf"))
        print(f"   Template files found: {len(template_files)}")
        for tf in template_files:
            print(f"      - {tf.name}")
    
    print("\nChecking configuration...")
    try:
        import json
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"   Template PDF: {config.get('template_pdf', 'NOT SET')}")
        print(f"   Output directory: {config.get('output_directory', 'NOT SET')}")
        print(f"   Fields configured: {len(config.get('fields', {}))}")
    except Exception as e:
        print(f"   ERROR reading config: {e}")
    
    print("\nChecking recipients...")
    try:
        with open(recipients_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        print(f"   Total recipient lines: {len(lines)}")
        for i, line in enumerate(lines[:3], 1):
            parts = line.split(',')
            print(f"   {i}. {parts[0] if parts else 'INVALID'} - {parts[1] if len(parts) > 1 else 'NO COURSE'}")
        if len(lines) > 3:
            print(f"   ... and {len(lines) - 3} more")
    except Exception as e:
        print(f"   ❌ Error reading recipients: {e}")
    
    print("\n🚀 Running certificate generation...")
    try:
        sys.path.insert(0, 'src')
        from automations.fill_certificates import fill_certificates_from_file
        
        results = fill_certificates_from_file()
        
        print(f"Return code: 0 (success)")
        print(f"\n� Results:")
        print(f"   Total recipients: {results['total']}")
        print(f"   Successfully generated: {results['generated']}")
        print(f"   Failed: {results['failed']}")
        print(f"   Output directory: {results['output_directory']}")
        
        if results['errors']:
            print(f"\n❌ Errors:")
            for error in results['errors']:
                print(f"   - {error}")
        
    except Exception as e:
        print(f"❌ Error running command: {e}")
        import traceback
        print("Full error details:")
        traceback.print_exc()
    
    input("\n🔙 Press Enter to return...")

def generate_certificates():
    """Generate certificates workflow"""
    clear_screen()
    print_header()
    print("\n📜 Generate Certificates")
    print("-" * 40)
    
    # Check if required files exist
    if not Path("data/certificates/config.json").exists():
        print("❌ Certificate configuration not found!")
        print("   Please ensure data/certificates/config.json exists")
        input("\n🔙 Press Enter to return...")
        return
    
    if not Path("data/certificates/recipients.txt").exists():
        print("❌ Recipients file not found!")
        print("   Please ensure data/certificates/recipients.txt exists")
        input("\n🔙 Press Enter to return...")
        return
    
    print("📋 Current recipients:")
    try:
        with open("data/certificates/recipients.txt", 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]  # Show first 5 lines
            for i, line in enumerate(lines, 1):
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) >= 2:
                        print(f"   {i}. {parts[0]} - {parts[1]}")
            
            total_lines = len([l for l in f.readlines() if l.strip()]) + len(lines)
            if total_lines > 5:
                print(f"   ... and {total_lines - 5} more recipients")
    except Exception as e:
        print(f"   Error reading recipients: {e}")
    
    print(f"\n🎯 Ready to generate certificates!")
    confirm = input("   Continue? (y/N): ").lower()
    
    if confirm in ['y', 'yes']:
        print("\n🔄 Generating certificates...")
        try:
            # Import and run directly to avoid encoding issues
            sys.path.insert(0, 'src')
            from automations.fill_certificates import fill_certificates_from_file
            
            results = fill_certificates_from_file()
            
            print("SUCCESS: Certificates generated successfully!")
            print(f"RESULTS: {results['generated']}/{results['total']} certificates generated")
            
            if results['failed'] > 0:
                print(f"WARNING: {results['failed']} certificates failed to generate")
                if results['errors']:
                    print("Errors:")
                    for error in results['errors']:
                        print(f"  - {error}")
            
            if results['generated'] > 0:
                print(f"OUTPUT: {results['output_directory']}")
                
        except Exception as e:
            print(f"ERROR: Error generating certificates: {e}")
            import traceback
            print("Full error details:")
            traceback.print_exc()
    
    input("\n🔙 Press Enter to return...")

def send_certificates():
    """Send certificates via email workflow"""
    clear_screen()
    print_header()
    print("\n📧 Send Certificates via Email")
    print("-" * 40)
    
    # Check required files
    status = check_files_exist()
    missing_files = []
    
    if not status['email_config']:
        missing_files.append("Email configuration (data/emails/email_config.json)")
    if not status['email_list']:
        missing_files.append("Email list (data/emails/email_list.csv)")
    if not status['email_template']:
        missing_files.append("Email template (data/emails/email.txt)")
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        input("\n🔙 Press Enter to return...")
        return
    
    # Show email list preview
    print("📋 Current email list:")
    try:
        with open("data/emails/email_list.csv", 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if len(lines) > 1:  # Skip header
                for i, line in enumerate(lines[1:6], 1):  # Show first 5 data rows
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            print(f"   {i}. {parts[0]} - {parts[1]}")
                
                total_recipients = len([l for l in lines[1:] if l.strip()])
                if total_recipients > 5:
                    print(f"   ... and {total_recipients - 5} more recipients")
                print(f"\n📊 Total recipients: {total_recipients}")
            else:
                print("   No recipients found")
                input("\n🔙 Press Enter to return...")
                return
    except Exception as e:
        print(f"   Error reading email list: {e}")
        input("\n🔙 Press Enter to return...")
        return
    
    # Get email subject
    print("\n📝 Email Configuration:")
    subject = input("   Enter email subject: ").strip()
    
    if not subject:
        print("❌ Email subject is required!")
        input("\n🔙 Press Enter to return...")
        return
    
    print(f"\n📧 Email Subject: {subject}")
    print("📄 Email template will be used from data/emails/email.txt")
    
    confirm = input("\n🎯 Ready to send emails? (y/N): ").lower()
    
    if confirm in ['y', 'yes']:
        print("\n🔄 Sending emails...")
        try:
            # Import and run directly to avoid encoding issues
            sys.path.insert(0, 'src')
            from automations.send_same_email import send_from_file
            
            results = send_from_file(
                'data/emails/email_list.csv', 
                subject, 
                'data/emails/email.txt', 
                'data/emails/email_config.json',
                'data/emails/attachments'
            )
            
            print("SUCCESS: Emails sent successfully!")
            print(f"RESULTS: {results['sent']}/{results['total']} emails sent")
            
            if results['failed'] > 0:
                print(f"WARNING: {results['failed']} emails failed to send")
                if results.get('errors'):
                    print("Errors:")
                    for error in results['errors']:
                        print(f"  - {error}")
                        
        except Exception as e:
            print(f"ERROR: Error sending emails: {e}")
            import traceback
            print("Full error details:")
            traceback.print_exc()
    
    input("\n🔙 Press Enter to return...")

def generate_contacts():
    """Generate contact cards workflow"""
    clear_screen()
    print_header()
    print("\n📞 Generate Contact Cards")
    print("-" * 40)
    
    numbers_file = Path("data/phone_numbers/numbers.txt")
    
    if not numbers_file.exists():
        print("❌ Phone numbers file not found!")
        print("   Please add phone numbers to data/phone_numbers/numbers.txt")
        print("   One number per line (e.g., 0712345678)")
        input("\n🔙 Press Enter to return...")
        return
    
    # Show preview of numbers
    print("📋 Current phone numbers:")
    try:
        with open(numbers_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:5]  # Show first 5 lines
            for i, line in enumerate(lines, 1):
                if line.strip():
                    print(f"   {i}. {line.strip()}")
            
            total_lines = len([l for l in f.readlines() if l.strip()]) + len(lines)
            if total_lines > 5:
                print(f"   ... and {total_lines - 5} more numbers")
    except Exception as e:
        print(f"   Error reading numbers: {e}")
    
    prefix = input(f"\n📝 Enter contact name prefix (default: 'Contact'): ").strip()
    if not prefix:
        prefix = "Contact"
    
    print(f"\n🎯 Ready to generate contact cards with prefix '{prefix}'!")
    confirm = input("   Continue? (y/N): ").lower()
    
    if confirm in ['y', 'yes']:
        print("\n🔄 Generating contact cards...")
        try:
            # Import and run directly to avoid encoding issues
            sys.path.insert(0, 'src')
            from automations.generate_contacts import generate_vcf_from_file
            
            results = generate_vcf_from_file(
                'data/phone_numbers/numbers.txt',
                None,  # Use auto-generated output filename
                prefix
            )
            
            print("SUCCESS: Contact cards generated successfully!")
            print(f"RESULTS:")
            print(f"   Total numbers: {results['total']}")
            print(f"   Valid numbers added: {results['valid']}")
            print(f"   Duplicates removed: {results['duplicates']}")
            print(f"   Invalid numbers: {results['invalid']}")
            print(f"   Output file: {results['output_file']}")
                        
        except Exception as e:
            print(f"ERROR: Error generating contact cards: {e}")
            import traceback
            print("Full error details:")
            traceback.print_exc()
    
    input("\n🔙 Press Enter to return...")

def delete_certificates():
    """Delete all generated certificates from output folder"""
    clear_screen()
    print_header()
    print("\nDELETE Generated Certificates")
    print("-" * 40)
    
    output_dir = Path("data/certificates/output")
    
    if not output_dir.exists():
        print("ERROR: Certificates output directory not found!")
        print("   Directory: data/certificates/output")
        input("\nPress Enter to return...")
        return
    
    # Find all PDF files in output directory
    pdf_files = list(output_dir.glob("*.pdf"))
    
    if not pdf_files:
        print("INFO: No certificates found in output directory.")
        print("   Directory: data/certificates/output")
        input("\nPress Enter to return...")
        return
    
    print(f"Found {len(pdf_files)} certificate(s) to delete:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"   {i}. {pdf_file.name}")
    
    print(f"\nWARNING: This will permanently delete all {len(pdf_files)} certificate file(s)!")
    print("   This action cannot be undone.")
    
    confirm = input("\nAre you sure you want to delete all certificates? (y/N): ").lower()
    
    if confirm in ['y', 'yes']:
        print("\nDeleting certificates...")
        
        deleted_count = 0
        failed_count = 0
        errors = []
        
        for pdf_file in pdf_files:
            try:
                pdf_file.unlink()  # Delete the file
                deleted_count += 1
                print(f"  SUCCESS: Deleted {pdf_file.name}")
            except Exception as e:
                failed_count += 1
                error_msg = f"Failed to delete {pdf_file.name}: {str(e)}"
                errors.append(error_msg)
                print(f"  ERROR: {error_msg}")
        
        print(f"\n{'='*50}")
        print("DELETION SUMMARY")
        print(f"{'='*50}")
        print(f"Total files found: {len(pdf_files)}")
        print(f"Successfully deleted: {deleted_count}")
        print(f"Failed to delete: {failed_count}")
        
        if errors:
            print(f"\nErrors:")
            for error in errors:
                print(f"  - {error}")
        
        if deleted_count > 0:
            print(f"\nSUCCESS: Successfully cleaned up {deleted_count} certificate file(s)!")
        
    else:
        print("\nOperation cancelled. No files were deleted.")
    
    input("\nPress Enter to return...")

def show_help():
    """Show help and documentation"""
    clear_screen()
    print_header()
    print("\n📚 Help & Documentation")
    print("-" * 40)
    print("\n🎯 Quick Start Guide:")
    print("1. First time setup:")
    print("   - Run setup.bat to create folder structure")
    print("   - Edit configuration files in data/ folders")
    print()
    print("2. Generate Certificates:")
    print("   - Add recipients to data/certificates/recipients.txt")
    print("   - Format: Name,Course")
    print("   - Configure positions in data/certificates/config.json")
    print("   - Unique 20-character certificate IDs are auto-generated")
    print("   - Certificate IDs are logged to certificate_ids.log")
    print()
    print("3. Send Emails:")
    print("   - Add recipients to data/emails/email_list.csv")
    print("   - Format: Name,Email")
    print("   - Configure SMTP in data/emails/email_config.json")
    print("   - Edit email template in data/emails/email.txt")
    print("   - Email template supports dynamic fields: {name}, {course_name}, {cert_id}")
    print("   - Course names and certificate IDs are automatically populated")
    print()
    print("4. Delete Certificates:")
    print("   - Use menu option 6 to safely delete all generated certificates")
    print("   - This cleans up data/certificates/output/ folder")
    print("   - Useful for testing or clearing old certificates")
    print()
    print("📁 Important Folders:")
    print("   - data/certificates/output/     - Generated certificates")
    print("   - data/certificates/output/certificate_ids.log - Certificate ID tracking")
    print("   - data/emails/attachments/      - Certificate attachments")
    print("   - examples/                     - Example configuration files")
    print()
    print("🔧 Manual Commands:")
    print("   - python src/main.py --help")
    print("   - python src/main.py fill_certificates")
    print("   - python src/main.py send_bulk_emails --subject 'Your Subject'")
    print("   - python src/main.py generate_contacts")
    
    input("\n🔙 Press Enter to return...")

def check_api_status():
    """Check API connection status"""
    try:
        # Import API module
        import sys
        sys.path.append('src')
        from automations.certificate_api import CertificateAPI, load_api_config
        
        config = load_api_config()
        api = CertificateAPI()
        
        return {
            "enabled": config.get('api_enabled', False),
            "connected": api.test_connection() if config.get('api_enabled', False) else False,
            "base_url": config.get('api_base_url', 'Not configured'),
            "config_exists": True
        }
    except Exception as e:
        return {
            "enabled": False,
            "connected": False,
            "base_url": 'Not configured',
            "config_exists": False,
            "error": str(e)
        }
    return status

def api_configuration_menu():
    """API Configuration and Management Menu"""
    while True:
        clear_screen()
        print_header()
        print("\n🌐 Certificate Validator API Configuration")
        print("-" * 60)
        
        # Show current API status
        api_status = check_api_status()
        
        print("\n📊 Current API Status:")
        if api_status.get('config_exists'):
            print(f"⚙️  Configuration:      {'✅ Found' if api_status['config_exists'] else '❌ Missing'}")
            print(f"🔌 API Enabled:         {'✅ Yes' if api_status['enabled'] else '❌ No'}")
            print(f"🌐 Connection:          {'✅ Connected' if api_status['connected'] else '❌ Failed'}")
            print(f"🔗 Base URL:            {api_status['base_url']}")
        else:
            print(f"⚙️  Configuration:      ❌ Missing or Error")
            print(f"   Error: {api_status.get('error', 'Unknown error')}")
        
        print("\n📋 API Management Options:")
        print("1️⃣  Test API Connection")
        print("2️⃣  Toggle API Enable/Disable")
        print("3️⃣  View API Configuration")
        print("4️⃣  Edit API Settings")
        print("5️⃣  Test Certificate Creation")
        print("6️⃣  View API Documentation")
        print("0️⃣  Back to Main Menu")
        print("-" * 60)
        
        choice = input("\n🎯 Select an option: ").strip()
        
        if choice == "1":
            test_api_connection()
        elif choice == "2":
            toggle_api_status()
        elif choice == "3":
            view_api_configuration()
        elif choice == "4":
            edit_api_settings()
        elif choice == "5":
            test_certificate_creation()
        elif choice == "6":
            view_api_documentation()
        elif choice == "0":
            break
        else:
            print("❌ Invalid option. Please try again.")
            input("Press Enter to continue...")


def test_api_connection():
    """Test API connection"""
    print("\n🧪 Testing API Connection...")
    print("-" * 40)
    
    try:
        import sys
        sys.path.append('src')
        from automations.certificate_api import CertificateAPI
        
        api = CertificateAPI()
        
        if not api.is_enabled():
            print("⚠️  API integration is disabled")
            print("   Enable it in the configuration to test connection")
        else:
            print(f"🌐 Testing connection to: {api.base_url}")
            
            if api.test_connection():
                print("✅ API connection successful!")
            else:
                print("❌ API connection failed!")
                print("   - Check internet connection")
                print("   - Verify API URL and key")
                print("   - Check firewall settings")
    
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
    
    input("\n🔙 Press Enter to continue...")


def toggle_api_status():
    """Toggle API enabled/disabled status"""
    print("\n🔧 Toggle API Status...")
    print("-" * 40)
    
    try:
        import json
        config_path = "data/emails/api_config.json"
        
        # Load current config
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
        else:
            print("❌ API configuration file not found!")
            input("Press Enter to continue...")
            return
        
        current_status = config.get('api_enabled', False)
        new_status = not current_status
        
        config['api_enabled'] = new_status
        
        # Save updated config
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        status_text = "enabled" if new_status else "disabled"
        print(f"✅ API integration {status_text} successfully!")
        
    except Exception as e:
        print(f"❌ Error toggling API status: {str(e)}")
    
    input("\n🔙 Press Enter to continue...")


def view_api_configuration():
    """View current API configuration"""
    print("\n📄 API Configuration:")
    print("-" * 40)
    
    try:
        import json
        config_path = "data/emails/api_config.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            print(f"API Enabled:        {config.get('api_enabled', False)}")
            print(f"Base URL:          {config.get('api_base_url', 'Not set')}")
            print(f"API Key:           {'*' * 20 if config.get('api_key') else 'Not set'}")
            print(f"Default Expiry:    {config.get('default_expiry_years', 3)} years")
            print(f"Timeout:           {config.get('timeout_seconds', 30)} seconds")
            print(f"Retry Attempts:    {config.get('retry_attempts', 2)}")
            
        else:
            print("❌ API configuration file not found!")
            print("   Default configuration will be used")
    
    except Exception as e:
        print(f"❌ Error reading configuration: {str(e)}")
    
    input("\n🔙 Press Enter to continue...")


def edit_api_settings():
    """Edit API settings"""
    print("\n✏️  Edit API Settings:")
    print("-" * 40)
    print("⚠️  This feature is not implemented yet.")
    print("   You can manually edit: data/emails/api_config.json")
    print("\n📄 Example configuration:")
    print("""{
  "api_enabled": true,
  "api_base_url": "https://verify.devopsacademy.online/validate/admin_dashboard/api.php",
  "api_key": "cert_api_2025_secure_key",
  "default_expiry_years": 3,
  "timeout_seconds": 30,
  "retry_attempts": 2
}""")
    
    input("\n🔙 Press Enter to continue...")


def test_certificate_creation():
    """Test certificate creation via API"""
    print("\n🧪 Test Certificate Creation:")
    print("-" * 40)
    
    try:
        import sys
        sys.path.append('src')
        from automations.certificate_api import CertificateAPI
        from datetime import datetime
        
        api = CertificateAPI()
        
        if not api.is_enabled():
            print("⚠️  API integration is disabled")
            input("Press Enter to continue...")
            return
        
        # Create test certificate
        test_id = f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        print(f"Creating test certificate: {test_id}")
        
        result = api.create_certificate(
            cert_id=test_id,
            recipient_name="Test User",
            course_name="API Test Course",
            expiry_date="2027-12-31"
        )
        
        if result.get('success'):
            print("✅ Test certificate created successfully!")
            print(f"   Certificate ID: {test_id}")
        else:
            print(f"❌ Test failed: {result.get('message', 'Unknown error')}")
    
    except Exception as e:
        print(f"❌ Error testing certificate creation: {str(e)}")
    
    input("\n🔙 Press Enter to continue...")


def view_api_documentation():
    """View API documentation"""
    print("\n📚 API Documentation:")
    print("-" * 40)
    print("📄 Full documentation available in: API_GUIDE.md")
    print("\n🌐 Web Resources:")
    print("   • API Endpoint: https://verify.devopsacademy.online/validate/admin_dashboard/api.php")
    print("   • Admin Dashboard: https://verify.devopsacademy.online/validate/admin_dashboard/admin-dashboard.php")
    print("   • User Portal: https://verify.devopsacademy.online/validate/user_portal/")
    print("\n🔑 API Features:")
    print("   • Create, read, update, delete certificates")
    print("   • Search and pagination")
    print("   • Automatic certificate validation")
    print("   • Bulk upload support")
    print("   • Web verification portal")
    
    input("\n🔙 Press Enter to continue...")

def main():
    """Main application loop"""
    while True:
        clear_screen()
        print_header()
        print_main_menu()
        
        try:
            choice = input("👉 Select an option (0-7, 9): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using the Automation System!")
                print("🎉 Have a great day!")
                break
            elif choice == '1':
                generate_certificates()
            elif choice == '2':
                send_certificates()
            elif choice == '3':
                generate_contacts()
            elif choice == '4':
                show_system_status()
            elif choice == '5':
                show_help()
            elif choice == '6':
                delete_certificates()
            elif choice == '7':
                api_configuration_menu()
            elif choice == '9':
                debug_certificate_generation()
            else:
                print(f"\n❌ Invalid option: {choice}")
                print("Please select a number from 0-7 or 9")
                input("\n🔙 Press Enter to try again...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}")
            input("\n🔙 Press Enter to continue...")

if __name__ == "__main__":
    main()
