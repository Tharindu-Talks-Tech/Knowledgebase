# Certificate Validator API - Complete Guide

## 📋 Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Base URL](#base-url)
- [Response Format](#response-format)
- [Error Handling](#error-handling)
- [CRUD Operations](#crud-operations)
  - [Create Certificate](#1-create-certificate-post)
  - [Read Certificate](#2-read-certificate-get)
  - [Update Certificate](#3-update-certificate-put)
  - [Delete Certificate](#4-delete-certificate-delete)
  - [List All Certificates](#5-list-all-certificates-get)
- [Bulk Operations](#bulk-operations)
- [Code Examples](#code-examples)
- [Testing](#testing)
- [Best Practices](#best-practices)

---

## Overview

The Certificate Validator API provides a RESTful interface for managing certificates. It supports full CRUD (Create, Read, Update, Delete) operations with authentication and error handling.

### Features

- ✅ Create, read, update, and delete certificates
- ✅ Bulk certificate operations
- ✅ Pagination and search
- ✅ API key authentication
- ✅ Comprehensive error handling
- ✅ JSON responses

---

## Authentication

All API requests require an API key in the request header:

```http
X-API-Key: cert_api_2025_secure_key
```

### Getting Your API Key

The default API key is: `cert_api_2025_secure_key`

**⚠️ Security Note:** Change this key in production by modifying the `$valid_api_key` variable in `api.php`.

---

## Base URL

```
https://verify.devopsacademy.online/validate/admin_dashboard/api.php
```

---

## Response Format

All responses are returned in JSON format:

### Success Response Structure

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    /* Response data */
  },
  "timestamp": "2025-07-07T12:00:00Z"
}
```

### Error Response Structure

```json
{
  "success": false,
  "message": "Error description",
  "error_code": "ERROR_CODE",
  "timestamp": "2025-07-07T12:00:00Z"
}
```

---

## Error Handling

### HTTP Status Codes

| Code | Description                             |
| ---- | --------------------------------------- |
| 200  | OK - Request successful                 |
| 201  | Created - Resource created successfully |
| 400  | Bad Request - Invalid parameters        |
| 401  | Unauthorized - Invalid API key          |
| 404  | Not Found - Resource doesn't exist      |
| 409  | Conflict - Resource already exists      |
| 500  | Internal Server Error                   |

### Common Error Codes

| Error Code              | Description                    |
| ----------------------- | ------------------------------ |
| `INVALID_API_KEY`       | API key is missing or invalid  |
| `VALIDATION_ERROR`      | Request data validation failed |
| `DUPLICATE_CERTIFICATE` | Certificate ID already exists  |
| `CERTIFICATE_NOT_FOUND` | Certificate doesn't exist      |
| `DATABASE_ERROR`        | Database operation failed      |

---

## CRUD Operations

### 1. Create Certificate (POST)

Create a new certificate in the system.

**Endpoint:** `POST /api.php`

**Headers:**

```http
Content-Type: application/json
X-API-Key: cert_api_2025_secure_key
```

**Request Body:**

```json
{
  "certificate_id": "WELLNESS-2025-001",
  "recipient_name": "John Doe",
  "course_name": "Yoga Instructor Certification",
  "issue_date": "2025-07-07",
  "expiry_date": "2028-07-07"
}
```

**Parameters:**

| Parameter        | Type   | Required | Description                        |
| ---------------- | ------ | -------- | ---------------------------------- |
| `certificate_id` | string | ✅ Yes   | Unique certificate identifier      |
| `recipient_name` | string | ✅ Yes   | Full name of certificate recipient |
| `course_name`    | string | ✅ Yes   | Name of the course/program         |
| `issue_date`     | string | ✅ Yes   | Date issued (YYYY-MM-DD format)    |
| `expiry_date`    | string | ❌ No    | Expiry date (YYYY-MM-DD format)    |

**Success Response (201 Created):**

```json
{
  "success": true,
  "message": "Certificate added successfully",
  "data": {
    "id": "123",
    "certificate_id": "WELLNESS-2025-001",
    "recipient_name": "John Doe",
    "course_name": "Yoga Instructor Certification",
    "issue_date": "2025-07-07",
    "expiry_date": "2028-07-07",
    "created_at": "2025-07-07T12:00:00",
    "updated_at": "2025-07-07T12:00:00"
  }
}
```

**Example Commands:**

**cURL:**

```bash
curl -X POST "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cert_api_2025_secure_key" \
  -d '{
    "certificate_id": "WELLNESS-2025-001",
    "recipient_name": "John Doe",
    "course_name": "Yoga Instructor Certification",
    "issue_date": "2025-07-07",
    "expiry_date": "2028-07-07"
  }'
```

**PowerShell:**

```powershell
$body = @{
    certificate_id = "WELLNESS-2025-001"
    recipient_name = "John Doe"
    course_name = "Yoga Instructor Certification"
    issue_date = "2025-07-07"
    expiry_date = "2028-07-07"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "cert_api_2025_secure_key"
}

Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" -Method POST -Body $body -Headers $headers
```

---

### 2. Read Certificate (GET)

Retrieve a specific certificate by its ID.

**Endpoint:** `GET /api.php?certificate_id={certificate_id}`

**Headers:**

```http
X-API-Key: cert_api_2025_secure_key
```

**Parameters:**

| Parameter        | Type   | Required | Description                   |
| ---------------- | ------ | -------- | ----------------------------- |
| `certificate_id` | string | ✅ Yes   | Unique certificate identifier |

**Success Response (200 OK):**

```json
{
  "success": true,
  "data": {
    "id": "123",
    "certificate_id": "WELLNESS-2025-001",
    "recipient_name": "John Doe",
    "course_name": "Yoga Instructor Certification",
    "issue_date": "2025-07-07",
    "expiry_date": "2028-07-07",
    "created_at": "2025-07-07T12:00:00",
    "updated_at": "2025-07-07T12:00:00"
  }
}
```

**Example Commands:**

**cURL:**

```bash
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=WELLNESS-2025-001" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**PowerShell:**

```powershell
$headers = @{"X-API-Key" = "cert_api_2025_secure_key"}
Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=WELLNESS-2025-001" -Headers $headers
```

---

### 3. Update Certificate (PUT)

Update an existing certificate.

**Endpoint:** `PUT /api.php`

**Headers:**

```http
Content-Type: application/json
X-API-Key: cert_api_2025_secure_key
```

**Request Body:**

```json
{
  "certificate_id": "WELLNESS-2025-001",
  "recipient_name": "John Smith",
  "course_name": "Advanced Yoga Instructor Certification",
  "expiry_date": "2029-07-07"
}
```

**Parameters:**

| Parameter        | Type   | Required | Description                           |
| ---------------- | ------ | -------- | ------------------------------------- |
| `certificate_id` | string | ✅ Yes   | Certificate ID to update (identifier) |
| `recipient_name` | string | ❌ No    | Updated recipient name                |
| `course_name`    | string | ❌ No    | Updated course name                   |
| `issue_date`     | string | ❌ No    | Updated issue date                    |
| `expiry_date`    | string | ❌ No    | Updated expiry date                   |

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Certificate updated successfully",
  "data": {
    "id": "123",
    "certificate_id": "WELLNESS-2025-001",
    "recipient_name": "John Smith",
    "course_name": "Advanced Yoga Instructor Certification",
    "issue_date": "2025-07-07",
    "expiry_date": "2029-07-07",
    "created_at": "2025-07-07T12:00:00",
    "updated_at": "2025-07-07T13:30:00"
  }
}
```

**Example Commands:**

**cURL:**

```bash
curl -X PUT "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cert_api_2025_secure_key" \
  -d '{
    "certificate_id": "WELLNESS-2025-001",
    "recipient_name": "John Smith",
    "course_name": "Advanced Yoga Instructor Certification",
    "expiry_date": "2029-07-07"
  }'
```

**PowerShell:**

```powershell
$body = @{
    certificate_id = "WELLNESS-2025-001"
    recipient_name = "John Smith"
    course_name = "Advanced Yoga Instructor Certification"
    expiry_date = "2029-07-07"
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
    "X-API-Key" = "cert_api_2025_secure_key"
}

Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" -Method PUT -Body $body -Headers $headers
```

---

### 4. Delete Certificate (DELETE)

Delete a certificate from the system.

**Endpoint:** `DELETE /api.php?certificate_id={certificate_id}`

**Headers:**

```http
X-API-Key: cert_api_2025_secure_key
```

**Parameters:**

| Parameter        | Type   | Required | Description              |
| ---------------- | ------ | -------- | ------------------------ |
| `certificate_id` | string | ✅ Yes   | Certificate ID to delete |

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Certificate deleted successfully",
  "data": {
    "certificate_id": "WELLNESS-2025-001",
    "deleted_at": "2025-07-07T14:00:00Z"
  }
}
```

**Example Commands:**

**cURL:**

```bash
curl -X DELETE "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=WELLNESS-2025-001" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**PowerShell:**

```powershell
$headers = @{"X-API-Key" = "cert_api_2025_secure_key"}
Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=WELLNESS-2025-001" -Method DELETE -Headers $headers
```

---

### 5. List All Certificates (GET)

Retrieve all certificates with pagination and search capabilities.

**Endpoint:** `GET /api.php`

**Headers:**

```http
X-API-Key: cert_api_2025_secure_key
```

**Query Parameters:**

| Parameter | Type    | Required | Default | Description                                              |
| --------- | ------- | -------- | ------- | -------------------------------------------------------- |
| `page`    | integer | ❌ No    | 1       | Page number for pagination                               |
| `limit`   | integer | ❌ No    | 10      | Records per page (max 100)                               |
| `search`  | string  | ❌ No    | -       | Search in recipient name, course name, or certificate ID |

**Success Response (200 OK):**

```json
{
  "success": true,
  "data": [
    {
      "id": "123",
      "certificate_id": "WELLNESS-2025-001",
      "recipient_name": "John Doe",
      "course_name": "Yoga Instructor Certification",
      "issue_date": "2025-07-07",
      "expiry_date": "2028-07-07",
      "created_at": "2025-07-07T12:00:00",
      "updated_at": "2025-07-07T12:00:00"
    },
    {
      "id": "124",
      "certificate_id": "WELLNESS-2025-002",
      "recipient_name": "Jane Smith",
      "course_name": "Meditation Guide Training",
      "issue_date": "2025-07-06",
      "expiry_date": "2027-07-06",
      "created_at": "2025-07-06T15:30:00",
      "updated_at": "2025-07-06T15:30:00"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 25,
    "total_pages": 3
  }
}
```

**Example Commands:**

**Get all certificates (first page):**

```bash
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**Get certificates with pagination:**

```bash
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?page=2&limit=5" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**Search certificates:**

```bash
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?search=yoga" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**PowerShell Examples:**

```powershell
$headers = @{"X-API-Key" = "cert_api_2025_secure_key"}

# Get all certificates
Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" -Headers $headers

# Get with pagination
Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?page=2&limit=5" -Headers $headers

# Search certificates
Invoke-RestMethod -Uri "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?search=yoga" -Headers $headers
```

---

## Bulk Operations

### Bulk Upload via CSV

For bulk operations, use the admin dashboard's bulk upload feature:

1. **Access the admin dashboard:** `https://verify.devopsacademy.online/validate/admin_dashboard/admin-dashboard.php`
2. **Go to the "Bulk Upload" tab**
3. **Download the sample CSV template**
4. **Fill in your certificate data**
5. **Upload the CSV file**

**Sample CSV Format:**

```csv
certificate_id,recipient_name,course_name,issue_date,expiry_date
WELLNESS-BULK-001,Alice Johnson,Wellness Coach Certification,2025-07-07,2028-07-07
WELLNESS-BULK-002,Bob Wilson,Nutrition Specialist Training,2025-07-07,2027-07-07
WELLNESS-BULK-003,Carol Davis,Fitness Instructor Course,2025-07-07,2026-07-07
```

---

## Code Examples

### JavaScript (Node.js/Browser)

```javascript
class CertificateAPI {
  constructor(baseUrl, apiKey) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
    this.headers = {
      "Content-Type": "application/json",
      "X-API-Key": apiKey,
    };
  }

  // Create certificate
  async createCertificate(certificateData) {
    try {
      const response = await fetch(this.baseUrl, {
        method: "POST",
        headers: this.headers,
        body: JSON.stringify(certificateData),
      });
      return await response.json();
    } catch (error) {
      console.error("Error creating certificate:", error);
      throw error;
    }
  }

  // Get certificate
  async getCertificate(certificateId) {
    try {
      const response = await fetch(
        `${this.baseUrl}?certificate_id=${certificateId}`,
        {
          method: "GET",
          headers: { "X-API-Key": this.apiKey },
        }
      );
      return await response.json();
    } catch (error) {
      console.error("Error getting certificate:", error);
      throw error;
    }
  }

  // Update certificate
  async updateCertificate(certificateData) {
    try {
      const response = await fetch(this.baseUrl, {
        method: "PUT",
        headers: this.headers,
        body: JSON.stringify(certificateData),
      });
      return await response.json();
    } catch (error) {
      console.error("Error updating certificate:", error);
      throw error;
    }
  }

  // Delete certificate
  async deleteCertificate(certificateId) {
    try {
      const response = await fetch(
        `${this.baseUrl}?certificate_id=${certificateId}`,
        {
          method: "DELETE",
          headers: { "X-API-Key": this.apiKey },
        }
      );
      return await response.json();
    } catch (error) {
      console.error("Error deleting certificate:", error);
      throw error;
    }
  }

  // List certificates
  async listCertificates(page = 1, limit = 10, search = "") {
    try {
      let url = `${this.baseUrl}?page=${page}&limit=${limit}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;

      const response = await fetch(url, {
        method: "GET",
        headers: { "X-API-Key": this.apiKey },
      });
      return await response.json();
    } catch (error) {
      console.error("Error listing certificates:", error);
      throw error;
    }
  }
}

// Usage Example
const api = new CertificateAPI(
  "https://verify.devopsacademy.online/validate/admin_dashboard/api.php",
  "cert_api_2025_secure_key"
);

// Create a certificate
api
  .createCertificate({
    certificate_id: "WELLNESS-JS-001",
    recipient_name: "Alice Johnson",
    course_name: "JavaScript Wellness App Development",
    issue_date: "2025-07-07",
    expiry_date: "2028-07-07",
  })
  .then((result) => {
    console.log("Certificate created:", result);
  })
  .catch((error) => {
    console.error("Failed to create certificate:", error);
  });
```

### Python

```python
import requests
import json
from datetime import datetime

class CertificateAPI:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }

    def create_certificate(self, certificate_data):
        """Create a new certificate"""
        try:
            response = requests.post(
                self.base_url,
                json=certificate_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error creating certificate: {e}")
            raise

    def get_certificate(self, certificate_id):
        """Get a certificate by ID"""
        try:
            response = requests.get(
                f"{self.base_url}?certificate_id={certificate_id}",
                headers={'X-API-Key': self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error getting certificate: {e}")
            raise

    def update_certificate(self, certificate_data):
        """Update an existing certificate"""
        try:
            response = requests.put(
                self.base_url,
                json=certificate_data,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error updating certificate: {e}")
            raise

    def delete_certificate(self, certificate_id):
        """Delete a certificate"""
        try:
            response = requests.delete(
                f"{self.base_url}?certificate_id={certificate_id}",
                headers={'X-API-Key': self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error deleting certificate: {e}")
            raise

    def list_certificates(self, page=1, limit=10, search=None):
        """List certificates with pagination"""
        params = {'page': page, 'limit': limit}
        if search:
            params['search'] = search

        try:
            response = requests.get(
                self.base_url,
                params=params,
                headers={'X-API-Key': self.api_key}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error listing certificates: {e}")
            raise

# Usage Example
if __name__ == "__main__":
    api = CertificateAPI(
        base_url="https://verify.devopsacademy.online/validate/admin_dashboard/api.php",
        api_key="cert_api_2025_secure_key"
    )

    # Create a certificate
    cert_data = {
        "certificate_id": "WELLNESS-PY-001",
        "recipient_name": "Bob Wilson",
        "course_name": "Python for Wellness Analytics",
        "issue_date": "2025-07-07",
        "expiry_date": "2028-07-07"
    }

    try:
        # Create
        result = api.create_certificate(cert_data)
        print("Certificate created:", result)

        # Read
        cert = api.get_certificate("WELLNESS-PY-001")
        print("Certificate retrieved:", cert)

        # Update
        update_data = {
            "certificate_id": "WELLNESS-PY-001",
            "course_name": "Advanced Python for Wellness Analytics"
        }
        updated = api.update_certificate(update_data)
        print("Certificate updated:", updated)

        # List
        certificates = api.list_certificates(page=1, limit=5, search="python")
        print("Certificates list:", certificates)

        # Delete
        # deleted = api.delete_certificate("WELLNESS-PY-001")
        # print("Certificate deleted:", deleted)

    except Exception as e:
        print(f"API operation failed: {e}")
```

### PHP

```php
<?php
class CertificateAPI {
    private $baseUrl;
    private $apiKey;

    public function __construct($baseUrl, $apiKey) {
        $this->baseUrl = $baseUrl;
        $this->apiKey = $apiKey;
    }

    private function makeRequest($method, $endpoint = '', $data = null) {
        $url = $this->baseUrl . $endpoint;

        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'Content-Type: application/json',
            'X-API-Key: ' . $this->apiKey
        ]);

        switch ($method) {
            case 'POST':
                curl_setopt($ch, CURLOPT_POST, true);
                if ($data) {
                    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
                }
                break;
            case 'PUT':
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'PUT');
                if ($data) {
                    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
                }
                break;
            case 'DELETE':
                curl_setopt($ch, CURLOPT_CUSTOMREQUEST, 'DELETE');
                break;
        }

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        return [
            'status_code' => $httpCode,
            'data' => json_decode($response, true)
        ];
    }

    public function createCertificate($certificateData) {
        return $this->makeRequest('POST', '', $certificateData);
    }

    public function getCertificate($certificateId) {
        return $this->makeRequest('GET', "?certificate_id=$certificateId");
    }

    public function updateCertificate($certificateData) {
        return $this->makeRequest('PUT', '', $certificateData);
    }

    public function deleteCertificate($certificateId) {
        return $this->makeRequest('DELETE', "?certificate_id=$certificateId");
    }

    public function listCertificates($page = 1, $limit = 10, $search = null) {
        $params = "?page=$page&limit=$limit";
        if ($search) {
            $params .= "&search=" . urlencode($search);
        }
        return $this->makeRequest('GET', $params);
    }
}

// Usage Example
$api = new CertificateAPI(
    'https://verify.devopsacademy.online/validate/admin_dashboard/api.php',
    'cert_api_2025_secure_key'
);

try {
    // Create certificate
    $result = $api->createCertificate([
        'certificate_id' => 'WELLNESS-PHP-001',
        'recipient_name' => 'Carol Davis',
        'course_name' => 'PHP Wellness Application Development',
        'issue_date' => '2025-07-07',
        'expiry_date' => '2028-07-07'
    ]);

    echo "Certificate created: " . json_encode($result) . "\n";

    // Get certificate
    $cert = $api->getCertificate('WELLNESS-PHP-001');
    echo "Certificate retrieved: " . json_encode($cert) . "\n";

    // Update certificate
    $updated = $api->updateCertificate([
        'certificate_id' => 'WELLNESS-PHP-001',
        'course_name' => 'Advanced PHP Wellness Application Development'
    ]);
    echo "Certificate updated: " . json_encode($updated) . "\n";

    // List certificates
    $list = $api->listCertificates(1, 5, 'php');
    echo "Certificates list: " . json_encode($list) . "\n";

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
?>
```

---

## Testing

### Test Your API Endpoints

**1. Quick connectivity test:**

```bash
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

**2. Complete CRUD test sequence:**

```bash
# 1. Create a certificate
curl -X POST "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cert_api_2025_secure_key" \
  -d '{
    "certificate_id": "TEST-2025-001",
    "recipient_name": "Test User",
    "course_name": "API Testing Course",
    "issue_date": "2025-07-07",
    "expiry_date": "2026-07-07"
  }'

# 2. Read the certificate
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=TEST-2025-001" \
  -H "X-API-Key: cert_api_2025_secure_key"

# 3. Update the certificate
curl -X PUT "https://verify.devopsacademy.online/validate/admin_dashboard/api.php" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: cert_api_2025_secure_key" \
  -d '{
    "certificate_id": "TEST-2025-001",
    "course_name": "Advanced API Testing Course"
  }'

# 4. List all certificates
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?page=1&limit=5" \
  -H "X-API-Key: cert_api_2025_secure_key"

# 5. Delete the certificate
curl -X DELETE "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?certificate_id=TEST-2025-001" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

### Test Script

Run the provided test script to validate all functionality:

```bash
# If you have the test script
php test-api.php
```

---

## Best Practices

### 1. **Always Use HTTPS**

```bash
# ✅ Good
https://verify.devopsacademy.online/validate/admin_dashboard/api.php

# ❌ Bad
http://verify.devopsacademy.online/validate/admin_dashboard/api.php
```

### 2. **Include API Key in Headers**

```bash
# ✅ Good
-H "X-API-Key: cert_api_2025_secure_key"

# ❌ Bad
?api_key=cert_api_2025_secure_key
```

### 3. **Handle Errors Gracefully**

```javascript
try {
  const result = await api.createCertificate(data);
  if (result.success) {
    console.log("Success:", result.data);
  } else {
    console.error("API Error:", result.message);
  }
} catch (error) {
  console.error("Network Error:", error);
}
```

### 4. **Use Pagination for Large Datasets**

```bash
# Get first 20 certificates
curl -X GET "https://verify.devopsacademy.online/validate/admin_dashboard/api.php?page=1&limit=20" \
  -H "X-API-Key: cert_api_2025_secure_key"
```

### 5. **Validate Data Before Sending**

```javascript
function validateCertificateData(data) {
  const errors = [];

  if (!data.certificate_id) errors.push("Certificate ID is required");
  if (!data.recipient_name) errors.push("Recipient name is required");
  if (!data.course_name) errors.push("Course name is required");
  if (!data.issue_date) errors.push("Issue date is required");

  return errors;
}
```

### 6. **Use Descriptive Certificate IDs**

```bash
# ✅ Good
"certificate_id": "WELLNESS-YOGA-2025-001"
"certificate_id": "NUTRITION-BASIC-2025-JAN-001"

# ❌ Less descriptive
"certificate_id": "CERT001"
"certificate_id": "12345"
```

---

## Rate Limiting

The API implements rate limiting to prevent abuse:

- **Standard requests:** 100 requests per minute
- **Bulk operations:** 10 requests per minute

**Rate limit headers:**

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 85
X-RateLimit-Reset: 1625673600
```

---

## Support & Resources

### 📚 **Additional Documentation**

- **Complete API Documentation:** `API_DOCUMENTATION.md`
- **Test Script:** `test-api.php`
- **Integration Example:** `api-integration-example.html`

### 🔧 **Admin Dashboard**

- **URL:** `https://verify.devopsacademy.online/validate/admin_dashboard/admin-dashboard.php`
- **Features:** Web interface for certificate management, bulk upload, API management

### 🌐 **User Portal**

- **URL:** `https://verify.devopsacademy.online/user_portal/`
- **Features:** Public certificate verification

### 🚨 **Troubleshooting**

**Common Issues:**

1. **401 Unauthorized:**

   - Check API key in headers
   - Verify API key value

2. **404 Not Found:**

   - Verify endpoint URL
   - Check certificate ID exists

3. **409 Conflict:**

   - Certificate ID already exists
   - Use different certificate ID

4. **500 Internal Server Error:**
   - Check database connection
   - Review server logs

**Contact Support:**

- For technical issues, check the error logs in your hosting control panel
- For API questions, refer to this documentation or the examples provided

---

## Changelog

### Version 1.0.0 (2025-07-07)

- ✅ Initial API release
- ✅ Full CRUD operations
- ✅ API key authentication
- ✅ Pagination support
- ✅ Search functionality
- ✅ Bulk upload via CSV
- ✅ Comprehensive error handling
- ✅ Multiple programming language examples

---

**🎉 Your Certificate Validator API is now ready for production use!**

For any questions or additional features, refer to the examples above or test the API using the provided commands.
