# Automations

This is a Python automation project with organized data folders for easy use.

## Quick Start

1. **Clone and setup:**

   ```bash
   git clone https://github.com/pruthivithejan/automations.git
   cd automations
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ````bash
   pip install -r requirements.txt
   ```.

   ````

4. **Set up data folder structure:**

   ```bash
   # Linux/Mac
   ./setup.sh

   # Windows
   setup.bat
   ```

5. **Configure your settings:**
   - Edit configuration files in `data/` folders with your credentials
   - Add your data (email lists, certificates, phone numbers)
   - See `examples/SETUP_GUIDE.md` for detailed instructions

## Available Automations

### 📞 Contact Card Generator

Converts phone numbers to VCF contact files for importing into your phone.

**Steps:**

1. **Paste your phone numbers** into `data/phone_numbers/numbers.txt` (one per line)
2. **Run the automation:**
   ```bash
   python src/main.py generate_contacts
   ```
3. **Find your VCF file** in `data/phone_numbers/` directory

**Example:**

```bash
# Generate contacts with custom prefix
python src/main.py generate_contacts --prefix "Workshop Participant"
```

**Supported Phone Formats:**

- 0712345678 (Sri Lankan)
- +94712345678 (International)
- 071 234 5678 (With spaces)

---

### 📧 Bulk Email Sender

Sends the same email to multiple recipients with enhanced deliverability.

**Steps:**

1. **Setup email configuration** in `data/emails/email_config.json`:

   ```json
   {
     "smtp_server": "smtp.gmail.com",
     "smtp_port": 587,
     "email": "your_email@gmail.com",
     "password": "your_app_password",
     "sender_name": "Your Name",
     "organization": "Your Organization"
   }
   ```

2. **Paste your email addresses** into `data/emails/email_list.txt` (one per line)

3. **Paste your email message** into `data/emails/email.txt`

4. **Add attachments** (optional) to `data/emails/attachments/`

5. **Run the automation:**
   ```bash
   python src/main.py send_bulk_emails --subject "Your Email Subject"
   ```

**Example:**

```bash
python src/main.py send_bulk_emails --subject "Workshop Invitation - Join Us Today!"
```

**Features:**

- ✅ Anti-spam headers and formatting
- ✅ Rate limiting to protect sender reputation
- ✅ Professional organization footer
- ✅ Attachment support
- ✅ Detailed delivery reporting

---

### 📬 Outlook Email with Individual Attachments

Sends personalized emails with individual attachments to each recipient via Outlook.

**Steps:**

1. **Setup Outlook configuration** in `data/outlook/email_config.json`:

   ```json
   {
     "smtp_server": "smtp.office365.com",
     "smtp_port": 587,
     "sender_email": "your_email@outlook.com",
     "password": "your_app_password",
     "subject": "Your Certificate"
   }
   ```

2. **Add recipients with their attachments** in `data/outlook/recipients.txt`:

   ```
   Student One,student1@outlook.com,student1.pdf
   Student Two,student2@outlook.com,student2.pdf
   ```

3. **Create email template** in `data/outlook/email.txt` (use `{name}` for personalization):

   ```
   Hi {name},

   Please find your certificate attached.

   Best regards,
   Your Name
   ```

4. **Add certificate files** to `data/outlook/certificates/` folder

5. **Run the automation:**
   ```bash
   python src/main.py send_outlook_emails
   ```

**Features:**

- ✅ Personalized emails with recipient names
- ✅ Individual attachments per recipient
- ✅ Outlook/Office365 SMTP support
- ✅ Certificate file validation
- ✅ Detailed sending reports

---

### 📄 Certificate Generator

Fills blank PDF certificate templates with recipient information and generates personalized certificates.

**Steps:**

1. **Create or obtain a blank certificate PDF template** and place it in `data/certificates/templates/`

2. **Configure field positions** in `data/certificates/config.json`:

   ```json
   {
     "template_pdf": "templates/certificate_template.pdf",
     "output_directory": "output",
     "fields": {
       "name": {
         "x": 396,
         "y": 370,
         "font_size": 28,
         "font_weight": "bold",
         "color": [0, 0, 139],
         "alignment": "center"
       },
       "course": {
         "x": 396,
         "y": 270,
         "font_size": 20,
         "font_weight": "bold",
         "color": [0, 0, 0],
         "alignment": "center"
       },
       "certificate_id": {
         "x": 396,
         "y": 200,
         "font_size": 12,
         "font_weight": "normal",
         "color": [100, 100, 100],
         "alignment": "center"
       }
     }
   }
   ```

3. **Add recipients** in `data/certificates/recipients.txt`:

   ```
   John Smith,Workshop on AI
   Jane Doe,Data Science Bootcamp
   ```

4. **Run the automation:**

   ```bash
   python src/main.py fill_certificates
   ```

5. **Find generated certificates** in `data/certificates/output/`

**Features:**

- ✅ PDF template overlay with precise positioning
- ✅ Customizable fonts, sizes, colors, and alignment
- ✅ Support for multiple data fields (name, course, certificate_id)
- ✅ **Auto-generated unique 20-character certificate IDs**
- ✅ **Certificate ID tracking log file (certificate_ids.log)**
- ✅ Automatic filename generation from recipient names
- ✅ Batch processing with detailed progress reports

## 🎯 Quick Start - Interactive Menu

The easiest way to use this system is through the interactive menu:

```bash
# Option 1: Python command
python start.py

# Option 2: Windows batch file (double-click)
start.bat
```

This will launch an interactive menu where you can:

- 📜 **Generate Certificates** - Create personalized certificates from templates
- 📧 **Send Certificates via Email** - Email certificates to recipients
- 📞 **Generate Contact Cards** - Create VCF files from phone numbers
- 📊 **View System Status** - Check if all required files are configured
- 📚 **Help & Documentation** - Get detailed usage instructions

The interactive menu guides you through each process step-by-step! 🎉

---

## Project Structure

```
examples/                    # Example configurations (safe to commit)
├── SETUP_GUIDE.md          # Complete setup instructions
├── README.md               # Examples documentation
├── emails/                 # Email automation examples
│   ├── email_config.json.example
│   ├── email_list.txt.example
│   └── email.txt.example
├── outlook/                # Outlook automation examples
├── certificates/           # Certificate generation examples
└── phone_numbers/          # Contact generation examples

data/                       # Your local data (excluded from git)
├── attachments/            # General attachments
├── certificates/           # Certificate generation assets
│   ├── config.json        # Field positions and styling
│   ├── recipients.txt     # Recipients with course/achievement data
│   ├── recipients_ex.txt  # Example recipients file
│   ├── templates/         # Blank PDF certificate templates
│   │   ├── CryptX.pdf    # Certificate template
│   │   └── Participants.pdf # Alternative template
│   └── output/            # Generated personalized certificates
├── email_config.json      # Global email configuration
├── email_config_enhanced.json # Enhanced email settings
├── email_config_template.md # Email config template/documentation
├── email_lists/           # Email list files
│   ├── icts_participants.txt # Workshop participants
│   └── icts_workshop_emails.csv # CSV format email lists
├── email_templates/       # Email template files
│   ├── icts_workshop_body.txt # Workshop email body
│   └── icts_workshop_enhanced.txt # Enhanced email template
├── emails/                # Bulk email automation assets
│   ├── email_config.json # Your Gmail/email settings
│   ├── email_list.txt    # Paste email addresses here (tab-separated name\temail)
│   ├── email.txt         # Paste email message here (supports {name} placeholder)
│   └── attachments/      # Individual certificate files for personalized sending
├── outlook/              # Outlook email automation assets
│   ├── email_config.json # Your Outlook settings
│   ├── recipients.txt    # Recipients with attachment filenames
│   ├── email.txt         # Email template with {name} placeholder
│   └── certificates/     # Individual attachment files
└── phone_numbers/        # Contact generation assets
    ├── numbers.txt       # Paste phone numbers here
    ├── sample_numbers.txt # Example phone numbers
    ├── envision_contacts.vcf # Generated contact files
    ├── numbers_contacts.vcf # Generated contact files
    └── *.vcf             # Other generated contact files

src/
├── automations/          # Automation scripts
│   ├── fill_certificates.py # Certificate generation
│   ├── generate_contacts.py # Contact VCF generation
│   ├── send_emails_outlook.py # Outlook email sending
│   └── send_same_email.py # Bulk/personalized email sending
└── main.py               # Main CLI interface

docs/                     # Documentation
├── email_deliverability_guide.md # Email best practices
└── PROJECT_SUMMARY.md    # Project overview

setup.bat                # Windows setup script
```

## Security Notes

- **Gmail Users:** Use App Passwords instead of regular passwords
- **Outlook Users:** Enable 2FA and create App Passwords for email sending
- **Data folder is excluded from git:** The entire `data/` folder is in `.gitignore` to protect sensitive information like email addresses, certificates, and configuration files
- **Never commit** config files with real credentials to version control
- **Test first** with a small recipient list before running bulk operations

## Getting Help

- **Complete setup guide:** See `examples/SETUP_GUIDE.md` for detailed instructions
- **Example configurations:** Check the `examples/` folder for template files
- **Command help:** Run any automation without arguments to see available options:

```bash
python src/main.py generate_contacts --help
python src/main.py send_bulk_emails --help
python src/main.py send_outlook_emails --help
python src/main.py fill_certificates --help
```

- **Quick setup:** Run `./setup.sh` (Linux/Mac) or `setup.bat` (Windows) to create the data folder structure

---

## 🌐 Certificate Validator API Integration

This system integrates with an external Certificate Validator API for automatic certificate verification and web portal access.

### 📋 Features

- ✅ **Automatic certificate registration** during email sending
- ✅ **Dynamic certificate lookup** from web service
- ✅ **Real-time certificate validation** via web portal
- ✅ **Retry logic and error handling** for robust operation
- ✅ **Configurable API settings** with enable/disable toggle
- ✅ **Certificate expiry management** with automatic date calculation

### ⚙️ Configuration

API settings are configured in `data/emails/api_config.json`:

```json
{
  "api_enabled": true,
  "api_base_url": "https://verify.devopsacademy.online/validate/admin_dashboard/api.php",
  "api_key": "cert_api_2025_secure_key",
  "default_expiry_years": 2,
  "timeout_seconds": 30,
  "retry_attempts": 2
}
```

### 🚀 How It Works

1. **Certificate Generation**: When certificates are generated, unique 20-character IDs are created
2. **Email Sending**: Before sending each email, the system:
   - Fetches recipient details (name, course, cert_id) from local files or API
   - Registers the certificate in the web validation service
   - Includes current date as issue_date and **automatic 2-year expiry date**
   - Sends personalized email with dynamic fields: `{name}`, `{course_name}`, `{cert_id}`
3. **Web Verification**: Recipients can verify certificates at the public portal

### 📅 **Certificate Expiry Management**

- ✅ **Automatic Expiry Calculation**: All certificates automatically expire **2 years from issue date**
- ✅ **Example**: Certificate issued on 2025-07-07 expires on 2027-07-07
- ✅ **API Integration**: Both issue_date and expiry_date are sent to web validation service
- ✅ **Registry Tracking**: Certificate registry stores expiry dates for all certificates
- ✅ **Configurable**: Default expiry years can be changed in `api_config.json`

### 🔧 API Management

Use the interactive menu to manage API settings:

```bash
python start.py
# Select option 7: API Configuration
```

**Available API operations:**

- Test API connection
- Toggle API enable/disable
- View current configuration
- Test certificate creation
- View API documentation

### 🌍 Web Resources

- **Admin Dashboard**: `https://verify.devopsacademy.online/validate/admin_dashboard/admin-dashboard.php`
- **User Verification Portal**: `https://verify.devopsacademy.online/validate/user_portal/`
- **API Documentation**: See `API_GUIDE.md` for complete API reference

### 🧪 Testing

Run the comprehensive API test suite:

```bash
python test_api_integration.py
```

This tests all API functionality including configuration, connection, certificate creation, and email integration.
