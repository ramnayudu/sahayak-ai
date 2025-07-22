import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import List, Optional, Dict, Union, Any
import json
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FirebaseService:
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        # Always try to use Firebase, fallback gracefully if not available
        self.db: Optional[Any] = None
        
        if not firebase_admin._apps:
            # Initialize with service account key or default credentials
            service_account_key = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
            if service_account_key:
                try:
                    cred = credentials.Certificate(
                        json.loads(service_account_key)
                    )
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                except Exception as e:
                    print(f"Failed to initialize Firebase with service account: {e}")
            else:
                try:
                    cred = credentials.ApplicationDefault()
                    firebase_admin.initialize_app(cred)
                    self.db = firestore.client()
                except Exception as e:
                    print(f"Failed to initialize Firebase with default credentials: {e}")
        else:
            try:
                self.db = firestore.client()
            except Exception as e:
                print(f"Failed to get Firestore client: {e}")
    
    async def health_check(self) -> bool:
        """Check Firebase connection"""
        if self.db is None:
            return False  # Firebase not available
            
        try:
            # Try to read from a collection
            self.db.collection('health_check').limit(1).get()
            return True
        except Exception:
            return False
    
    async def save_lesson_plan(self, lesson_plan: Dict) -> Dict:
        """Save a lesson plan to Firestore"""
        try:
            lesson_plan['created_at'] = datetime.utcnow().isoformat()
            lesson_plan['updated_at'] = datetime.utcnow().isoformat()
            
            if self.db is None:
                # Firebase not available, generate a mock ID and return
                lesson_plan['id'] = str(uuid.uuid4())
                print("Firebase not available, returning lesson plan with mock ID")
                return lesson_plan
            
            doc_ref = self.db.collection('lesson_plans').add(lesson_plan)
            lesson_plan['id'] = doc_ref[1].id
            
            return lesson_plan
        except Exception as e:
            raise Exception(f"Failed to save lesson plan: {str(e)}")
    
    async def get_lesson_plans(
        self, 
        subject: Optional[str] = None, 
        grade: Optional[int] = None,
        user_id: Optional[str] = None
    ) -> List[Dict]:
        """Get lesson plans with optional filtering"""
        try:
            if self.db is None:
                # Return mock data in dev mode
                mock_lesson = {
                    'id': 'mock-lesson-1',
                    'subject': subject or 'Math',
                    'grades': [grade] if grade else [5],
                    'topic': 'Sample Topic',
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
                return [mock_lesson]
            
            query = self.db.collection('lesson_plans')
            
            if subject:
                query = query.where('subject', '==', subject)
            if grade:
                query = query.where('grades', 'array_contains', grade)
            if user_id:
                query = query.where('user_id', '==', user_id)
            
            docs = query.get()
            lesson_plans = []
            
            for doc in docs:
                plan = doc.to_dict()
                plan['id'] = doc.id
                lesson_plans.append(plan)
            
            return lesson_plans
        except Exception as e:
            raise Exception(f"Failed to get lesson plans: {str(e)}")
    
    async def get_lesson_plan(self, lesson_id: str) -> Optional[Dict]:
        """Get a specific lesson plan by ID"""
        try:
            if self.db is None:
                # Return mock data in dev mode
                return {
                    'id': lesson_id,
                    'subject': 'Math',
                    'grades': [5],
                    'topic': 'Sample Topic',
                    'created_at': datetime.utcnow().isoformat(),
                    'updated_at': datetime.utcnow().isoformat()
                }
            
            doc = self.db.collection('lesson_plans').document(lesson_id).get()
            if doc.exists:
                plan = doc.to_dict()
                plan['id'] = doc.id
                return plan
            return None
        except Exception as e:
            raise Exception(f"Failed to get lesson plan: {str(e)}")
    
    async def create_lesson_plan(self, lesson_plan: Dict) -> Dict:
        """Create a new lesson plan"""
        return await self.save_lesson_plan(lesson_plan)
    
    async def update_lesson_plan(
        self, 
        lesson_id: str, 
        lesson_plan: Dict
    ) -> Dict:
        """Update an existing lesson plan"""
        try:
            lesson_plan['updated_at'] = datetime.utcnow().isoformat()
            
            if self.db is None:
                # In dev mode, return the updated plan with ID
                lesson_plan['id'] = lesson_id
                return lesson_plan
            
            self.db.collection('lesson_plans').document(lesson_id).update(
                lesson_plan
            )
            
            updated_plan = await self.get_lesson_plan(lesson_id)
            if updated_plan is None:
                raise Exception("Lesson plan not found after update")
            return updated_plan
        except Exception as e:
            raise Exception(f"Failed to update lesson plan: {str(e)}")
    
    async def delete_lesson_plan(self, lesson_id: str) -> bool:
        """Delete a lesson plan"""
        try:
            if self.db is None:
                # In dev mode, always return success
                return True
            
            self.db.collection('lesson_plans').document(lesson_id).delete()
            return True
        except Exception as e:
            raise Exception(f"Failed to delete lesson plan: {str(e)}")
    
    async def save_user_preferences(
        self, 
        user_id: str, 
        preferences: Dict
    ) -> bool:
        """Save user preferences"""
        try:
            if self.db is None:
                # In dev mode, always return success
                return True
            
            self.db.collection('user_preferences').document(user_id).set(
                preferences, 
                merge=True
            )
            return True
        except Exception as e:
            raise Exception(f"Failed to save preferences: {str(e)}")
    
    async def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences"""
        try:
            if self.db is None:
                # Return default preferences in dev mode
                return {
                    'theme': 'light',
                    'language': 'en',
                    'default_subject': 'Math',
                    'default_grade': 5
                }
            
            doc = self.db.collection('user_preferences').document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return {}
        except Exception as e:
            raise Exception(f"Failed to get preferences: {str(e)}")
