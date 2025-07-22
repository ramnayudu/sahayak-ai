#!/usr/bin/env python3
"""
Test Firebase Admin SDK import and setup
"""

# Test if we can import firebase_admin
try:
    import firebase_admin
    print("✅ firebase_admin imported successfully")
    print(f"Firebase Admin SDK version: {firebase_admin.__version__}")
    print(f"Firebase Admin SDK location: {firebase_admin.__file__}")
except ImportError as e:
    print(f"❌ Failed to import firebase_admin: {e}")

# Test if we can import firebase_admin submodules
try:
    from firebase_admin import credentials, firestore, auth
    print("✅ Firebase Admin submodules imported successfully")
except ImportError as e:
    print(f"❌ Failed to import firebase_admin submodules: {e}")

# Test our FirebaseService
try:
    import sys
    import os
    
    # Add the parent directory to the path so we can import from services
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from services.firebase_service import FirebaseService
    
    fs = FirebaseService()
    print("✅ FirebaseService initialized successfully")
    print(f"Development mode: {fs.dev_mode}")
    print(f"Database client: {type(fs.db)}")
    
except Exception as e:
    print(f"❌ Failed to initialize FirebaseService: {e}")
    import traceback
    traceback.print_exc()
