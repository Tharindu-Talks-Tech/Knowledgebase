"""
Certificate Registry Module
Ensures data integrity between certificate generation, email sending, and API integration
"""

import os
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class CertificateRegistry:
    """
    Central registry for managing certificate data with guaranteed integrity
    between PDF generation, email templates, and API requests
    """
    
    def __init__(self, base_dir: str = "data/certificates"):
        self.base_dir = base_dir
        self.registry_file = os.path.join(base_dir, "certificate_registry.json")
        self.recipients_file = os.path.join(base_dir, "recipients.txt")
        self.output_dir = os.path.join(base_dir, "output")
        
        # Ensure directories exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Load or initialize registry
        self.registry = self._load_registry()
    
    def _load_registry(self) -> Dict:
        """Load certificate registry from JSON file"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load registry: {e}")
        
        return {
            "certificates": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "version": "1.0"
            }
        }
    
    def _save_registry(self):
        """Save certificate registry to JSON file"""
        self.registry["metadata"]["last_updated"] = datetime.now().isoformat()
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warning: Could not save registry: {e}")
    
    def register_certificate(self, name: str, course: str, cert_id: str, 
                           issue_date: str = None, expiry_date: str = None, pdf_path: str = None) -> Dict:
        """
        Register a certificate with guaranteed data integrity
        
        Args:
            name: Recipient's full name (exactly as it should appear everywhere)
            course: Course name (exactly as it should appear everywhere)
            cert_id: Unique certificate ID (exactly as embedded in PDF)
            issue_date: Issue date in YYYY-MM-DD format
            expiry_date: Expiry date in YYYY-MM-DD format (auto-calculated if not provided)
            pdf_path: Path to generated PDF file
            
        Returns:
            Certificate record dictionary
        """
        if issue_date is None:
            issue_date = datetime.now().strftime('%Y-%m-%d')
            
        # Auto-calculate expiry date if not provided (2 years from issue date)
        if expiry_date is None:
            try:
                issue_date_obj = datetime.strptime(issue_date, '%Y-%m-%d')
                expiry_date_obj = issue_date_obj.replace(year=issue_date_obj.year + 2)
                expiry_date = expiry_date_obj.strftime('%Y-%m-%d')
            except Exception as e:
                print(f"⚠️  Warning: Could not calculate expiry date: {e}")
                # Fallback: 2 years from today
                expiry_date_obj = datetime.now().replace(year=datetime.now().year + 2)
                expiry_date = expiry_date_obj.strftime('%Y-%m-%d')
        
        # Create normalized key for lookup (case-insensitive, trimmed)
        lookup_key = name.strip().lower()
        
        # Create the certificate record
        cert_record = {
            "name": name.strip(),  # Exact name for display
            "course": course.strip(),  # Exact course name for display
            "certificate_id": cert_id,  # Exact cert ID embedded in PDF
            "issue_date": issue_date,
            "expiry_date": expiry_date,  # Auto-calculated 2 years from issue date
            "registration_timestamp": datetime.now().isoformat(),
            "pdf_generated": pdf_path is not None,
            "pdf_path": pdf_path,
            "email_sent": False,
            "api_registered": False
        }
        
        # Store in registry
        self.registry["certificates"][lookup_key] = cert_record
        self._save_registry()
        
        print(f"📝 Registered certificate: {cert_id} for {name} (valid until {expiry_date})")
        return cert_record
    
    def get_certificate(self, name: str) -> Optional[Dict]:
        """
        Get certificate record by recipient name with exact data integrity
        
        Args:
            name: Recipient name (case-insensitive lookup)
            
        Returns:
            Certificate record with exact field values or None
        """
        lookup_key = name.strip().lower()
        return self.registry["certificates"].get(lookup_key)
    
    def get_all_certificates(self) -> List[Dict]:
        """Get all certificate records"""
        return list(self.registry["certificates"].values())
    
    def update_certificate_status(self, name: str, **updates):
        """Update certificate status (email_sent, api_registered, etc.)"""
        lookup_key = name.strip().lower()
        if lookup_key in self.registry["certificates"]:
            self.registry["certificates"][lookup_key].update(updates)
            self._save_registry()
    
    def get_template_fields(self, name: str) -> Dict[str, str]:
        """
        Get template fields for email/API with guaranteed integrity
        
        Returns:
            Dictionary with keys: name, course_name, cert_id
            These values are guaranteed to match the PDF and API exactly
        """
        cert_record = self.get_certificate(name)
        if cert_record:
            return {
                "name": cert_record["name"],
                "course_name": cert_record["course"],
                "cert_id": cert_record["certificate_id"]
            }
        
        # Fallback to unknown values
        return {
            "name": name.strip(),
            "course_name": "Unknown Course",
            "cert_id": "Not Available"
        }
    
    def load_recipients_from_file(self) -> List[Dict]:
        """Load recipients from recipients.txt file"""
        recipients = []
        if not os.path.exists(self.recipients_file):
            return recipients
        
        try:
            with open(self.recipients_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 2:
                        recipients.append({
                            'name': parts[0].strip(),
                            'course': parts[1].strip()
                        })
                    else:
                        print(f"⚠️  Warning: Invalid format on line {line_num}")
        except Exception as e:
            print(f"⚠️  Error reading recipients file: {e}")
        
        return recipients
    
    def export_to_legacy_log(self):
        """Export registry to legacy certificate_ids.log format for compatibility"""
        log_file = os.path.join(self.output_dir, "certificate_ids.log")
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"{'='*60}\n")
                f.write(f"Certificate Registry Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"{'='*60}\n")
                
                for cert in self.get_all_certificates():
                    f.write(f"{cert['certificate_id']} | {cert['name']} | {cert['course']}\n")
                
                f.write(f"{'='*60}\n")
            
            print(f"📄 Exported registry to legacy log: {log_file}")
        except Exception as e:
            print(f"⚠️  Warning: Could not export to legacy log: {e}")
    
    def sync_with_legacy_log(self):
        """Import existing certificates from legacy certificate_ids.log"""
        log_file = os.path.join(self.output_dir, "certificate_ids.log")
        if not os.path.exists(log_file):
            return
        
        print("🔄 Syncing with legacy certificate log...")
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if '|' in line and not line.startswith('=') and not line.startswith('Certificate'):
                        parts = [p.strip() for p in line.split('|')]
                        if len(parts) >= 3:
                            cert_id, name, course = parts[0], parts[1], parts[2]
                            
                            # Only add if not already in registry
                            if not self.get_certificate(name):
                                self.register_certificate(
                                    name=name,
                                    course=course,
                                    cert_id=cert_id,
                                    issue_date=datetime.now().strftime('%Y-%m-%d')
                                )
            
            print("✅ Legacy log sync completed")
        except Exception as e:
            print(f"⚠️  Warning: Could not sync with legacy log: {e}")


# Global registry instance
_registry = None

def get_registry() -> CertificateRegistry:
    """Get the global certificate registry instance"""
    global _registry
    if _registry is None:
        _registry = CertificateRegistry()
        # Sync with existing data on first load
        _registry.sync_with_legacy_log()
    return _registry


def register_certificate(name: str, course: str, cert_id: str, **kwargs) -> Dict:
    """Convenience function to register a certificate"""
    return get_registry().register_certificate(name, course, cert_id, **kwargs)


def get_certificate_fields(name: str) -> Dict[str, str]:
    """Convenience function to get template fields for a recipient"""
    return get_registry().get_template_fields(name)


def update_certificate_status(name: str, **updates):
    """Convenience function to update certificate status"""
    return get_registry().update_certificate_status(name, **updates)
