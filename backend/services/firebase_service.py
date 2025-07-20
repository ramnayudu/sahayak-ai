import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import List, Optional, Dict
import json
import os
from datetime import datetime

class FirebaseService:
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        if not firebase_admin._apps:
            # Initialize with service account key or default credentials
            if os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"):
                cred = credentials.Certificate(
                    json.loads(os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"))
                )
            else:
                cred = credentials.ApplicationDefault()
            
            firebase_admin.initialize_app(cred)
        
        self.db = firestore.client()
    
    async def health_check(self) -> bool:
        """Check Firebase connection"""
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
            
            self.db.collection('lesson_plans').document(lesson_id).update(
                lesson_plan
            )
            
            return await self.get_lesson_plan(lesson_id)
        except Exception as e:
            raise Exception(f"Failed to update lesson plan: {str(e)}")
    
    async def delete_lesson_plan(self, lesson_id: str) -> bool:
        """Delete a lesson plan"""
        try:
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
            doc = self.db.collection('user_preferences').document(user_id).get()
            if doc.exists:
                return doc.to_dict()
            return {}
        except Exception as e:
            raise Exception(f"Failed to get preferences: {str(e)}")
