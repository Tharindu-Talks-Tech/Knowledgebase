import smtplib
import json
import os
import shutil
import csv
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

# Import the certificate API integration
try:
    from .certificate_api import push_certificate_to_web_service, get_certificate_details, fetch_certificate_for_recipient
    from ..utils.certificate_registry import get_registry, get_certificate_fields, update_certificate_status
except ImportError:
    # Fallback for when running as a script
    import sys
    import os
    
    # Add the current and parent directories to sys.path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    utils_dir = os.path.join(parent_dir, 'utils')
    sys.path.insert(0, current_dir)
    sys.path.insert(0, utils_dir)
    sys.path.insert(0, parent_dir)
    
    try:
        from certificate_api import push_certificate_to_web_service, get_certificate_details, fetch_certificate_for_recipient
        from utils.certificate_registry import get_registry, get_certificate_fields, update_certificate_status
    except ImportError as e:
        # Final fallback - import what we can and create stubs for what we can't
        try:
            from certificate_api import push_certificate_to_web_service, get_certificate_details, fetch_certificate_for_recipient
        except ImportError:
            print("⚠️  Warning: Certificate API not available")
            
        # Create stub functions for registry
        print("⚠️  Warning: Certificate registry not available")
        def get_registry():
            return None
        def get_certificate_fields(name):
            return {"name": name, "course_name": "Unknown Course", "cert_id": "Not Available"}
        def update_certificate_status(*args, **kwargs):
            pass


@dataclass
class SimpleEmailConfig:
    """Simple email configuration"""
    smtp_server: str
    smtp_port: int
    email: str
    password: str
    use_tls: bool = True


class SimpleEmailSender:
    def __init__(self, config: SimpleEmailConfig):
        self.config = config
        self.smtp_connection = None
    
    def connect(self):
        """Establish SMTP connection"""
        try:
            self.smtp_connection = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            if self.config.use_tls:
                self.smtp_connection.starttls()
            self.smtp_connection.login(self.config.email, self.config.password)
            print(f"✅ Connected to SMTP server: {self.config.smtp_server}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to SMTP server: {str(e)}")
            return False
    
    def disconnect(self):
        """Close SMTP connection"""
        if self.smtp_connection:
            self.smtp_connection.quit()
            print("📤 Disconnected from SMTP server")
    
    def create_message(self, to_email: str, subject: str, body: str, attachments: List[str] = None) -> MIMEMultipart:
        """Create email message"""
        msg = MIMEMultipart()
        msg['From'] = self.config.email
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body
        msg.attach(MIMEText(body, 'plain'))
        
        # Add attachments if provided
        if attachments:
            for file_path in attachments:
                if Path(file_path).exists():
                    self._attach_file(msg, file_path)
                else:
                    print(f"⚠️  Attachment not found: {file_path}")
        
        return msg
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach a file to the email message"""
        with open(file_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {Path(file_path).name}'
        )
        msg.attach(part)
    
    def send_same_email_to_multiple(
        self, 
        email_list: List[str], 
        subject: str, 
        body: str, 
        attachments: List[str] = None
    ) -> dict:
        """Send the same email to multiple recipients"""
        results = {"sent": 0, "failed": 0, "total": len(email_list), "failed_emails": []}
        
        if not self.connect():
            return results
        
        print(f"📧 Sending email to {len(email_list)} recipients...")
        print(f"📄 Subject: {subject}")
        print(f"📎 Attachments: {len(attachments) if attachments else 0}")
        print()
        
        for i, email in enumerate(email_list, 1):
            print(f"📤 Sending email {i}/{len(email_list)} to {email}...")
            
            try:
                msg = self.create_message(email, subject, body, attachments)
                self.smtp_connection.send_message(msg)
                results["sent"] += 1
                print(f"✅ Email sent successfully")
            except Exception as e:
                results["failed"] += 1
                results["failed_emails"].append(email)
                print(f"❌ Failed to send email: {str(e)}")
        
        self.disconnect()
        return results


def auto_copy_certificates_to_attachments():
    """Automatically copy certificates from output folder to email attachments folder"""
    try:
        # Define source and destination paths
        source_dir = Path("data/certificates/output")
        dest_dir = Path("data/emails/attachments")
        
        # Create destination directory if it doesn't exist
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if source directory exists
        if not source_dir.exists():
            print("ℹ️  No certificates output folder found, skipping auto-copy")
            return 0
        
        # Get all PDF files in source directory
        pdf_files = list(source_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("ℹ️  No certificates found in output folder, skipping auto-copy")
            return 0
        
        # Copy each PDF file
        copied_count = 0
        for pdf_file in pdf_files:
            dest_file = dest_dir / pdf_file.name
            try:
                shutil.copy2(pdf_file, dest_file)
                copied_count += 1
            except Exception as e:
                print(f"⚠️  Failed to copy {pdf_file.name}: {str(e)}")
        
        if copied_count > 0:
            print(f"📎 Auto-copied {copied_count} certificate(s) to attachments folder")
        
        return copied_count
        
    except Exception as e:
        print(f"⚠️  Error in auto-copy certificates: {str(e)}")
        return 0


def auto_cleanup_attachments_folder():
    """Automatically clean up certificate files from attachments folder after successful sending"""
    try:
        # Define attachments directory
        attachments_dir = Path("data/emails/attachments")
        
        # Check if directory exists
        if not attachments_dir.exists():
            return 0
        
        # Get all PDF files in attachments directory
        pdf_files = list(attachments_dir.glob("*.pdf"))
        
        if not pdf_files:
            return 0
        
        # Delete each PDF file
        deleted_count = 0
        for pdf_file in pdf_files:
            try:
                pdf_file.unlink()  # Delete the file
                deleted_count += 1
            except Exception as e:
                print(f"⚠️  Failed to delete {pdf_file.name}: {str(e)}")
        
        if deleted_count > 0:
            print(f"🧹 Auto-cleaned {deleted_count} certificate(s) from attachments folder")
        
        return deleted_count
        
    except Exception as e:
        print(f"⚠️  Error in auto-cleanup attachments: {str(e)}")
        return 0


def load_simple_config(config_path: str) -> SimpleEmailConfig:
    """Load email configuration from JSON file"""
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    return SimpleEmailConfig(
        smtp_server=config_data['smtp_server'],
        smtp_port=config_data['smtp_port'],
        email=config_data['email'],
        password=config_data['password'],
        use_tls=config_data.get('use_tls', True)
    )


def send_same_email_to_all(
    email_list: List[str], 
    subject: str, 
    body: str, 
    config_file: str = "data/email_config.json",
    attachments: List[str] = None
):
    """Send the same email to all recipients in the list"""
    try:
        # Load configuration
        config = load_simple_config(config_file)
        
        # Send emails
        sender = SimpleEmailSender(config)
        results = sender.send_same_email_to_multiple(email_list, subject, body, attachments)
        
        # Print summary
        print("\n📊 Email Sending Summary:")
        print(f"Total recipients: {results['total']}")
        print(f"✅ Successfully sent: {results['sent']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"📈 Success rate: {(results['sent']/results['total']*100):.1f}%")
        
        if results['failed_emails']:
            print(f"\n❌ Failed email addresses:")
            for email in results['failed_emails']:
                print(f"  - {email}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error in email sending: {str(e)}")
        return {"sent": 0, "failed": 0, "total": 0, "failed_emails": []}


def get_recipient_details(name: str, use_api: bool = True) -> tuple:
    """
    Get course name and certificate ID for a recipient with guaranteed data integrity
    Uses the certificate registry to ensure exact field matching across PDF, email, and API
    """
    try:
        # First, try to get from certificate registry (guaranteed integrity)
        registry_fields = get_certificate_fields(name)
        if registry_fields['cert_id'] != "Not Available":
            print(f"📝 Found certificate in registry for {name}")
            return (registry_fields['course_name'], registry_fields['cert_id'])
        
        # Second, try to fetch from API if enabled
        if use_api:
            try:
                api_cert = fetch_certificate_for_recipient(name)
                if api_cert:
                    print(f"🌐 Found certificate details in web service for {name}")
                    return (
                        api_cert.get('course_name', 'Unknown Course'),
                        api_cert.get('certificate_id', 'Not Available')
                    )
            except Exception as e:
                print(f"⚠️  API lookup failed for {name}: {e}")
        
        # Fallback to legacy local file lookup
        print(f"📁 Looking up local certificate details for {name}")
        
        # Try to get course name from recipients.txt
        recipients_file = "data/certificates/recipients.txt"
        course_name = "Unknown Course"
        
        if os.path.exists(recipients_file):
            with open(recipients_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        parts = line.split(',')
                        if len(parts) >= 2 and parts[0].strip().upper() == name.upper():
                            course_name = parts[1].strip()
                            break
        
        # Try to get certificate ID from the most recent generation log
        cert_id = "Not Available"
        log_file = "data/certificates/output/certificate_ids.log"
        
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # Read from the bottom to get the most recent entries
            for line in reversed(lines):
                if '|' in line and not line.startswith('='):
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 3 and parts[1].upper() == name.upper():
                        cert_id = parts[0]
                        break
        
        return course_name, cert_id
        
    except Exception as e:
        print(f"⚠️  Warning: Could not get details for {name}: {e}")
        return "Unknown Course", "Not Available"


def send_personalized_emails_with_certificates(
    email_list_file: str,
    subject: str,
    body_template: str,
    config_file: str,
    certificates_dir: str
) -> dict:
    """Send personalized emails with individual certificate attachments"""
    try:
        # Automatically copy certificates from output folder to attachments folder
        print("🔄 Auto-copying certificates from output folder...")
        auto_copy_certificates_to_attachments()
        
        # Load configuration
        config = load_simple_config(config_file)
        
        # Parse email list with names and emails (CSV format)
        recipients = []
        with open(email_list_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            header = next(csv_reader, None)  # Skip header row if present
            
            for row_num, row in enumerate(csv_reader, 2):  # Start from row 2 (after header)
                if len(row) >= 2:
                    name = row[0].strip()
                    email = row[1].strip()
                    if name and email:  # Ensure both name and email are not empty
                        recipients.append({'name': name, 'email': email})
                elif len(row) == 1 and row[0].strip():
                    # Handle case where only email is provided (fallback)
                    email = row[0].strip()
                    if '@' in email:
                        name = email.split('@')[0]  # Use email prefix as name
                        recipients.append({'name': name, 'email': email})
        
        if not recipients:
            print("❌ No valid recipients found in email list")
            return {"sent": 0, "failed": 0, "total": 0, "failed_emails": []}
        
        # Create name to certificate mapping
        certificate_files = {}
        certificates_path = Path(certificates_dir)
        if certificates_path.exists():
            for cert_file in certificates_path.glob("*.pdf"):
                certificate_files[cert_file.stem] = str(cert_file)
        
        print(f"📧 Found {len(recipients)} recipients")
        print(f"📎 Found {len(certificate_files)} certificate files")
        
        # Initialize results
        results = {"sent": 0, "failed": 0, "total": len(recipients), "failed_emails": [], "missing_certificates": []}
        
        # Connect to SMTP
        sender = SimpleEmailSender(config)
        if not sender.connect():
            return results
        
        print(f"📤 Sending personalized emails...")
        print()
        
        for i, recipient in enumerate(recipients, 1):
            name = recipient['name']
            email = recipient['email']
            
            print(f"📧 Processing {i}/{len(recipients)}: {name} ({email})")
            
            try:
                # Find matching certificate
                certificate_path = find_matching_certificate(name, certificate_files)
                
                if not certificate_path:
                    print(f"⚠️  No matching certificate found for {name}")
                    results["missing_certificates"].append(name)
                    # Still send email without certificate
                    attachments = []
                    course_name = "Unknown Course"
                    cert_id = "Not Available"
                else:
                    print(f"📎 Found certificate: {Path(certificate_path).name}")
                    attachments = [certificate_path]
                    
                    # Get course name and certificate ID for this recipient
                    course_name, cert_id = get_recipient_details(name)
                
                # Personalize email body with name, course_name, and cert_id
                personalized_body = body_template.format(
                    name=name, 
                    course_name=course_name, 
                    cert_id=cert_id
                )
                
                # Push certificate data to web validation service (if cert_id is available and not already in API)
                if cert_id != "Not Available" and course_name != "Unknown Course":
                    try:
                        print(f"🌐 Registering certificate in web validation service...")
                        
                        # Try to get existing certificate first to avoid duplicates
                        existing_cert = get_certificate_details(cert_id)
                        
                        if existing_cert:
                            print(f"✅ Certificate already exists in web service")
                        else:
                            # Create new certificate in web service
                            api_result = push_certificate_to_web_service(
                                cert_id=cert_id,
                                recipient_name=name,
                                course_name=course_name
                            )
                            
                            if api_result.get('success'):
                                print(f"✅ Certificate registered for web verification")
                            elif api_result.get('skipped'):
                                print(f"ℹ️  API integration disabled")
                            else:
                                print(f"⚠️  Web service registration failed: {api_result.get('message', 'Unknown error')}")
                                
                    except Exception as api_error:
                        print(f"⚠️  Web service registration error: {str(api_error)}")
                        # Continue with email sending even if API fails
                
                # Create and send email
                msg = sender.create_message(email, subject, personalized_body, attachments)
                sender.smtp_connection.send_message(msg)
                
                # Update certificate status in registry
                try:
                    update_certificate_status(
                        name=name,
                        email_sent=True,
                        api_registered=(cert_id != "Not Available"),
                        email_timestamp=datetime.now().isoformat()
                    )
                except Exception as e:
                    print(f"⚠️  Warning: Could not update certificate status: {e}")
                
                results["sent"] += 1
                print(f"✅ Email sent successfully")
                
            except Exception as e:
                results["failed"] += 1
                results["failed_emails"].append(email)
                print(f"❌ Failed to send email: {str(e)}")
            
            print()
        
        sender.disconnect()
        
        # Print summary
        print("📊 Email Sending Summary:")
        print(f"Total recipients: {results['total']}")
        print(f"✅ Successfully sent: {results['sent']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"⚠️  Missing certificates: {len(results['missing_certificates'])}")
        print(f"📈 Success rate: {(results['sent']/results['total']*100):.1f}%")
        
        if results['failed_emails']:
            print(f"\n❌ Failed email addresses:")
            for email in results['failed_emails']:
                print(f"  - {email}")
        
        if results['missing_certificates']:
            print(f"\n⚠️  Missing certificates for:")
            for name in results['missing_certificates']:
                print(f"  - {name}")
        
        # Auto-cleanup attachments folder if all emails were sent successfully
        if results['sent'] > 0 and results['failed'] == 0:
            print()  # Add blank line before cleanup message
            auto_cleanup_attachments_folder()
        
        return results
        
    except Exception as e:
        print(f"❌ Error in email sending: {str(e)}")
        return {"sent": 0, "failed": 0, "total": 0, "failed_emails": []}


def find_matching_certificate(name: str, certificate_files: dict) -> str:
    """Find matching certificate file for a given name"""
    # Normalize name for matching
    normalized_name = normalize_name_for_matching(name)
    
    # Try exact match first
    for cert_name, cert_path in certificate_files.items():
        if normalized_name in cert_name.lower():
            return cert_path
    
    # Try partial matching
    name_parts = normalized_name.split('_')
    for cert_name, cert_path in certificate_files.items():
        cert_name_lower = cert_name.lower()
        # Check if most name parts are in certificate name
        matches = sum(1 for part in name_parts if part in cert_name_lower and len(part) > 2)
        if matches >= max(1, len(name_parts) // 2):  # At least half the parts match
            return cert_path
    
    return None


def normalize_name_for_matching(name: str) -> str:
    """Normalize name for certificate matching"""
    import re
    # Remove special characters and normalize spacing
    normalized = re.sub(r'[^\w\s]', '', name)
    # Replace spaces with underscores and convert to lowercase
    normalized = re.sub(r'\s+', '_', normalized).lower()
    return normalized


def send_from_file(
    email_list_file: str,
    subject: str, 
    body_file: str,
    config_file: str,
    attachments_dir: str
) -> dict:
    """Send personalized emails from files with individual certificate attachments"""
    try:
        # Read email body from file
        with open(body_file, 'r', encoding='utf-8') as f:
            body_template = f.read()
        
        # Call the personalized email function
        return send_personalized_emails_with_certificates(
            email_list_file=email_list_file,
            subject=subject,
            body_template=body_template,
            config_file=config_file,
            certificates_dir=attachments_dir
        )
        
    except Exception as e:
        print(f"❌ Error reading files: {str(e)}")
        return {"sent": 0, "failed": 0, "total": 0, "failed_emails": []}


if __name__ == "__main__":
    print("Simple Email Sender")
    print("Use the main CLI to run this automation:")
    print("python src/main.py send_bulk_emails --subject 'Your Subject Here'")
