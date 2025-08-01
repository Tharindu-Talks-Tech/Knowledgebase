"""
Certificate API Integration Module
Handles communication with the Certificate Validator API
"""

import requests
import json
import os
from datetime import datetime
from typing import Optional, Dict, Any
from pathlib import Path


def load_api_config(config_path: str = "data/emails/api_config.json") -> Dict[str, Any]:
    """Load API configuration from JSON file"""
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️  Warning: Could not load API config: {e}")
    
    # Return default configuration
    return {
        "api_enabled": True,
        "api_base_url": "https://verify.devopsacademy.online/validate/admin_dashboard/api.php",
        "api_key": "cert_api_2025_secure_key",
        "default_expiry_years": 3,
        "timeout_seconds": 30,
        "retry_attempts": 2
    }


class CertificateAPI:
    """Certificate API client for integrating with the web validation service"""
    
    def __init__(self, config_path: str = "data/emails/api_config.json"):
        self.config = load_api_config(config_path)
        self.base_url = self.config.get('api_base_url')
        self.api_key = self.config.get('api_key')
        self.timeout = self.config.get('timeout_seconds', 30)
        self.retry_attempts = self.config.get('retry_attempts', 2)
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': self.api_key
        }
    
    def is_enabled(self) -> bool:
        """Check if API integration is enabled"""
        return self.config.get('api_enabled', True)
    
    def create_certificate(self, cert_id: str, recipient_name: str, course_name: str, 
                          issue_date: str = None, expiry_date: str = None) -> Dict[str, Any]:
        """
        Create a new certificate in the web validation system
        
        Args:
            cert_id: Unique certificate identifier
            recipient_name: Full name of the certificate recipient
            course_name: Name of the course/program
            issue_date: Issue date (YYYY-MM-DD format), defaults to today
            expiry_date: Expiry date (YYYY-MM-DD format), auto-calculated if not provided
            
        Returns:
            API response dictionary
        """
        if not self.is_enabled():
            return {"success": True, "message": "API integration disabled", "skipped": True}
        
        if issue_date is None:
            issue_date = datetime.now().strftime('%Y-%m-%d')
        
        # Auto-calculate expiry date if not provided (2 years from issue date)
        if expiry_date is None:
            try:
                from datetime import datetime as dt, timedelta
                issue_date_obj = dt.strptime(issue_date, '%Y-%m-%d')
                # Add 2 years to the issue date
                expiry_date_obj = issue_date_obj.replace(year=issue_date_obj.year + 2)
                expiry_date = expiry_date_obj.strftime('%Y-%m-%d')
                print(f"📅 Auto-calculated expiry date: {expiry_date} (2 years from issue date)")
            except Exception as e:
                print(f"⚠️  Warning: Could not calculate expiry date: {e}")
                # Fallback: use default expiry years from config
                default_years = self.config.get('default_expiry_years', 2)
                expiry_date_obj = datetime.now().replace(year=datetime.now().year + default_years)
                expiry_date = expiry_date_obj.strftime('%Y-%m-%d')
                print(f"📅 Using fallback expiry date: {expiry_date} ({default_years} years from today)")
        
        certificate_data = {
            "certificate_id": cert_id,
            "recipient_name": recipient_name,
            "course_name": course_name,
            "issue_date": issue_date,
            "expiry_date": expiry_date
        }
        
        print(f"📋 Certificate validity: {issue_date} to {expiry_date}")
        
        # Attempt with retry logic
        for attempt in range(self.retry_attempts + 1):
            try:
                if attempt > 0:
                    print(f"🔄 Retry attempt {attempt}/{self.retry_attempts}")
                
                print(f"📤 Pushing certificate to web service: {cert_id}")
                response = requests.post(
                    self.base_url,
                    json=certificate_data,
                    headers=self.headers,
                    timeout=self.timeout
                )
                
                if response.status_code == 201:
                    result = response.json()
                    print(f"✅ Certificate successfully registered in web service")
                    return result
                elif response.status_code == 409:
                    # Certificate already exists, try to update it
                    print(f"⚠️  Certificate already exists, attempting to update...")
                    return self.update_certificate(cert_id, recipient_name, course_name, issue_date, expiry_date)
                else:
                    print(f"⚠️  API request failed with status {response.status_code}")
                    if attempt == self.retry_attempts:
                        return {"success": False, "message": f"HTTP {response.status_code}: {response.text}"}
                    
            except requests.exceptions.Timeout:
                print(f"⚠️  API request timed out")
                if attempt == self.retry_attempts:
                    return {"success": False, "message": "Request timed out after retries"}
            except requests.exceptions.ConnectionError:
                print(f"⚠️  Could not connect to API service")
                if attempt == self.retry_attempts:
                    return {"success": False, "message": "Connection error after retries"}
            except Exception as e:
                print(f"⚠️  API request failed: {str(e)}")
                if attempt == self.retry_attempts:
                    return {"success": False, "message": str(e)}
        
        return {"success": False, "message": "All retry attempts failed"}
    
    def update_certificate(self, cert_id: str, recipient_name: str = None, 
                          course_name: str = None, issue_date: str = None, 
                          expiry_date: str = None) -> Dict[str, Any]:
        """
        Update an existing certificate in the web validation system
        
        Args:
            cert_id: Certificate identifier to update
            recipient_name: Updated recipient name (optional)
            course_name: Updated course name (optional)
            issue_date: Updated issue date (optional)
            expiry_date: Updated expiry date (optional)
            
        Returns:
            API response dictionary
        """
        update_data = {"certificate_id": cert_id}
        
        if recipient_name:
            update_data["recipient_name"] = recipient_name
        if course_name:
            update_data["course_name"] = course_name
        if issue_date:
            update_data["issue_date"] = issue_date
        if expiry_date:
            update_data["expiry_date"] = expiry_date
        
        try:
            print(f"📤 Updating certificate in web service: {cert_id}")
            response = requests.put(
                self.base_url,
                json=update_data,
                headers=self.headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Certificate successfully updated in web service")
                return result
            else:
                print(f"⚠️  API update failed with status {response.status_code}")
                return {"success": False, "message": f"HTTP {response.status_code}: {response.text}"}
                
        except Exception as e:
            print(f"⚠️  API update failed: {str(e)}")
            return {"success": False, "message": str(e)}
    
    def get_certificate(self, cert_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a certificate from the web validation system
        
        Args:
            cert_id: Certificate identifier to retrieve
            
        Returns:
            Certificate data or None if not found
        """
        try:
            response = requests.get(
                f"{self.base_url}?certificate_id={cert_id}",
                headers={'X-API-Key': self.api_key},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    return result.get('data')
            
            return None
            
        except Exception as e:
            print(f"⚠️  Failed to retrieve certificate {cert_id}: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """
        Test connection to the API service
        
        Returns:
            True if connection is successful, False otherwise
        """
        if not self.is_enabled():
            return True  # If disabled, consider it "successful"
        
        try:
            response = requests.get(
                self.base_url,
                headers={'X-API-Key': self.api_key},
                timeout=10
            )
            return response.status_code in [200, 400]  # 400 is also ok (means API is responding)
        except:
            return False


def push_certificate_to_web_service(cert_id: str, recipient_name: str, course_name: str, 
                                  issue_date: str = None, config_path: str = "data/emails/api_config.json") -> Dict[str, Any]:
    """
    Convenience function to push certificate data to the web validation service
    with automatic 2-year expiry date calculation
    
    Args:
        cert_id: Unique certificate identifier
        recipient_name: Full name of the certificate recipient
        course_name: Name of the course/program
        issue_date: Issue date (YYYY-MM-DD format), defaults to today
        config_path: Path to API configuration file
        
    Returns:
        API response dictionary
    """
    api = CertificateAPI(config_path)
    
    # The create_certificate method will automatically calculate expiry date as 2 years from issue date
    return api.create_certificate(
        cert_id=cert_id,
        recipient_name=recipient_name,
        course_name=course_name,
        issue_date=issue_date  # Will default to today if None, expiry auto-calculated as +2 years
    )


def get_certificate_details(cert_id: str, config_path: str = "data/emails/api_config.json") -> Optional[Dict[str, Any]]:
    """
    Get certificate details from the web validation service
    
    Args:
        cert_id: Certificate identifier to retrieve
        config_path: Path to API configuration file
        
    Returns:
        Certificate data or None if not found
    """
    api = CertificateAPI(config_path)
    return api.get_certificate(cert_id)


def fetch_certificate_for_recipient(recipient_name: str, config_path: str = "data/emails/api_config.json") -> Optional[Dict[str, Any]]:
    """
    Fetch certificate details for a specific recipient by searching through the API
    
    Args:
        recipient_name: Name of the certificate recipient
        config_path: Path to API configuration file
        
    Returns:
        Certificate data or None if not found
    """
    api = CertificateAPI(config_path)
    
    if not api.is_enabled():
        return None
    
    try:
        # Search for certificates by recipient name
        response = requests.get(
            f"{api.base_url}?search={recipient_name}&limit=1",
            headers={'X-API-Key': api.api_key},
            timeout=api.timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success') and result.get('data') and len(result['data']) > 0:
                return result['data'][0]  # Return the first matching certificate
        
        return None
        
    except Exception as e:
        print(f"⚠️  Failed to fetch certificate for {recipient_name}: {str(e)}")
        return None


if __name__ == "__main__":
    # Test the API connection
    print("🧪 Testing Certificate API Integration...")
    api = CertificateAPI()
    
    if api.test_connection():
        print("✅ API connection successful!")
        
        # Test certificate creation
        test_result = api.create_certificate(
            cert_id="TEST-API-001",
            recipient_name="Test User",
            course_name="API Integration Test",
            expiry_date="2027-12-31"
        )
        
        print(f"Test result: {test_result}")
    else:
        print("❌ API connection failed!")
