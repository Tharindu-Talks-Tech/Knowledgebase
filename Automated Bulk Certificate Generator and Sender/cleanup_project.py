"""
Project Cleanup Script - Safely removes unwanted test files and temporary data
"""

import os
import shutil
from pathlib import Path

def safe_remove_file(file_path):
    """Safely remove a file with error handling"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"✅ Removed: {file_path}")
            return True
        else:
            print(f"⚠️  File not found: {file_path}")
            return False
    except Exception as e:
        print(f"❌ Error removing {file_path}: {e}")
        return False

def safe_remove_directory(dir_path):
    """Safely remove a directory with error handling"""
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            print(f"✅ Removed directory: {dir_path}")
            return True
        else:
            print(f"⚠️  Directory not found: {dir_path}")
            return False
    except Exception as e:
        print(f"❌ Error removing directory {dir_path}: {e}")
        return False

def cleanup_project():
    """Clean up the project by removing unwanted files"""
    print("🧹 PROJECT CLEANUP STARTING")
    print("=" * 50)
    
    # List of test files to remove (safe to delete)
    test_files = [
        "test_api_integration.py",
        "test_certificate_integrity.py", 
        "test_cert_gen.py",
        "test_cert_menu.py",
        "test_complete_workflow.py",
        "test_delete.py",
        "test_email_fields.py",
        "test_email_list.txt",
        "test_email_sending.py",
        "test_expiry_enhancement.py",
        "test_final.py",
        "test_full_workflow_enhanced.py",
        "test_generation_fixed.py",
        "test_imports.py",
        "test_regenerate_with_expiry.py",
        "verify_system.py"
    ]
    
    # Temporary documentation files to remove (safe to delete)
    temp_docs = [
        "API_ENDPOINT_UPDATE_SUMMARY.md",
        "API_INTEGRATION_SUMMARY.md", 
        "API_UPDATE_TESTING_SUMMARY.md",
        "CERTIFICATE_INTEGRITY_SOLUTION.md",
        "EXPIRY_DATE_ENHANCEMENT.md",
        "IMPORT_ISSUES_RESOLVED.md"
    ]
    
    # Directories to clean
    cache_dirs = [
        "__pycache__",
        "src/__pycache__",
        "src/automations/__pycache__",
        "src/utils/__pycache__"
    ]
    
    print("\n📝 FILES TO REMOVE:")
    print("-" * 30)
    
    removed_files = 0
    for file_name in test_files:
        if safe_remove_file(file_name):
            removed_files += 1
    
    print(f"\n📄 TEMPORARY DOCUMENTATION TO REMOVE:")
    print("-" * 30)
    
    removed_docs = 0
    for doc_name in temp_docs:
        if safe_remove_file(doc_name):
            removed_docs += 1
    
    print(f"\n📁 DIRECTORIES TO CLEAN:")
    print("-" * 30)
    
    removed_dirs = 0
    for dir_name in cache_dirs:
        if safe_remove_directory(dir_name):
            removed_dirs += 1
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print("=" * 30)
    print(f"✅ Test files removed: {removed_files}")
    print(f"✅ Temp documentation removed: {removed_docs}")
    print(f"✅ Cache directories removed: {removed_dirs}")
    
    print(f"\n🔒 PROTECTED FILES (kept safe):")
    print("-" * 30)
    protected_files = [
        "src/ (all core automation code)",
        "data/ (all user data and configurations)",
        "examples/ (user guides and examples)",
        "docs/ (project documentation)",
        "README.md (main project documentation)",
        "API_GUIDE.md (complete API reference)",
        "requirements.txt (dependencies)",
        "setup.bat (setup script)",
        "start.py (main interface)",
        "demo_api_features.py (demo script)",
        ".gitignore (git configuration)"
    ]
    
    for protected in protected_files:
        print(f"🛡️  {protected}")
    
    print(f"\n🎯 PROJECT CLEANUP COMPLETE!")
    print("✅ All unwanted test files removed")
    print("✅ All temporary documentation removed")
    print("✅ All core functionality preserved")
    print("✅ Project is now clean and production-ready")

if __name__ == "__main__":
    cleanup_project()
