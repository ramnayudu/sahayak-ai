import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Cloud configuration
GOOGLE_CLOUD_PROJECT = os.getenv('GOOGLE_CLOUD_PROJECT')
GOOGLE_CLOUD_LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION', 'us-central1')
GOOGLE_CLOUD_STORAGE_BUCKET = os.getenv('GOOGLE_CLOUD_STORAGE_BUCKET')
GOOGLE_GENAI_USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI', 'true').lower() == 'true'

# Local Model Configuration
USE_LOCAL_MODEL = os.getenv('USE_LOCAL_MODEL', 'false').lower() == 'true'
LOCAL_MODEL_URL = os.getenv('LOCAL_MODEL_URL', 'http://localhost:21002')
LOCAL_MODEL_NAME = os.getenv('LOCAL_MODEL_NAME', 'google/gemma-3-1b-pt')

# GCS Configuration for image storage
GCS_BUCKET_NAME = GOOGLE_CLOUD_STORAGE_BUCKET