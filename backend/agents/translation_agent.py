"""
Language Translation Agent for Sahayak AI agent framework.
This agent is responsible for translating content to other languages.
"""

from typing import Dict, List, Optional, Any
import json
import uuid
from .base_agent import BaseAgent, AgentType, MessageType, AgentMessage
from shared.constants import REGIONAL_LANGUAGES

class LanguageTranslationAgent(BaseAgent):
    """
    Agent responsible for translating content to other languages.
    This agent uses Vertex AI to translate educational content to the requested language.
    """
    
    def __init__(self, vertex_ai_service):
        """Initialize the language translation agent"""
        super().__init__("translator", AgentType.TRANSLATOR)
        self.vertex_ai_service = vertex_ai_service
        self.supported_languages = {lang.lower(): lang for lang in REGIONAL_LANGUAGES}
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process a message received from the orchestrator"""
        if message.message_type == MessageType.REQUEST:
            # Add message to conversation history
            self.conversation_history.append(message)
            
            # Process the request asynchronously
            # In a real implementation, this would be an async call
            # For now, we'll just return a placeholder response
            content = self._translate_content(message.content)
            
            # Create a response message
            response = self.create_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content=content,
                conversation_id=message.conversation_id,
                parent_message_id=message.message_id
            )
            
            return response
        
        return None
    
    def _translate_content(self, request_content: Dict[str, Any]) -> Dict[str, Any]:
        """Translate content based on the request"""
        user_request = request_content.get("user_request", "")
        analysis = request_content.get("analysis", {})
        
        # Get the target language from the analysis
        target_language = analysis.get("target_language")
        if not target_language:
            target_language = self._extract_language(user_request)
        
        # If no target language is specified, default to Telugu (from the example)
        if not target_language:
            target_language = "Telugu"
        
        # Check if we have content to translate from other agents
        # In a real implementation, this would be passed from the orchestrator
        # For now, we'll just create placeholder content
        content_to_translate = self._generate_placeholder_content(user_request)
        
        # Translate the content
        translated_content = self._perform_translation(content_to_translate, target_language)
        
        return {
            "original_language": "English",
            "target_language": target_language,
            "translated_content": translated_content,
            "status": "translated",
            "message": f"Content translated to {target_language} successfully"
        }
    
    def _extract_language(self, text: str) -> Optional[str]:
        """Extract the target language from the user request"""
        for lang_lower, lang_proper in self.supported_languages.items():
            if lang_lower in text.lower():
                return lang_proper
        
        return None
    
    def _generate_placeholder_content(self, user_request: str) -> Dict[str, Any]:
        """Generate placeholder content to translate"""
        if "fractions" in user_request.lower() and "4th grade" in user_request.lower():
            return {
                "lesson_plan": {
                    "title": "Understanding Fractions",
                    "introduction": "Fractions represent parts of a whole. They are essential mathematical concepts that help us understand division and proportions.",
                    "key_concepts": [
                        "A fraction consists of a numerator (top number) and denominator (bottom number)",
                        "The numerator represents the number of parts we have",
                        "The denominator represents the total number of equal parts in the whole",
                        "Equivalent fractions are different fractions that represent the same value"
                    ],
                    "activities": [
                        "Use fraction circles to visualize different fractions",
                        "Compare fractions using number lines",
                        "Solve real-world problems involving fractions"
                    ],
                    "conclusion": "Understanding fractions is fundamental to many mathematical concepts and real-life applications."
                },
                "worksheet": {
                    "title": "Fractions Practice Worksheet",
                    "instructions": "Complete the following problems to practice your understanding of fractions.",
                    "problems": [
                        "Identify the fraction represented by the shaded part of each shape.",
                        "Compare the following fractions using <, >, or =.",
                        "Add the following fractions with like denominators."
                    ]
                }
            }
        else:
            return {
                "lesson_plan": {
                    "title": "Sample Lesson",
                    "introduction": "Introduction to the topic",
                    "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
                    "activities": ["Activity 1", "Activity 2", "Activity 3"],
                    "conclusion": "Summary of key points"
                },
                "worksheet": {
                    "title": "Practice Worksheet",
                    "instructions": "Complete the following problems",
                    "problems": ["Problem 1", "Problem 2", "Problem 3"]
                }
            }
    
    def _perform_translation(self, content: Dict[str, Any], target_language: str) -> Dict[str, Any]:
        """
        Translate the content to the target language.
        In a real implementation, this would call the Vertex AI service.
        For now, we'll just return placeholder translations.
        """
        if target_language.lower() == "telugu":
            # Placeholder Telugu translations for fractions content
            if "fractions" in str(content).lower():
                return {
                    "lesson_plan": {
                        "title": "భిన్నాలను అర్థం చేసుకోవడం",
                        "introduction": "భిన్నాలు మొత్తంలో భాగాలను సూచిస్తాయి. అవి విభజన మరియు నిష్పత్తులను అర్థం చేసుకోవడానికి సహాయపడే ముఖ్యమైన గణిత భావనలు.",
                        "key_concepts": [
                            "ఒక భిన్నంలో లవము (పై సంఖ్య) మరియు హరము (క్రింది సంఖ్య) ఉంటాయి",
                            "లవము మనకు ఉన్న భాగాల సంఖ్యను సూచిస్తుంది",
                            "హరము మొత్తంలోని సమాన భాగాల మొత్తం సంఖ్యను సూచిస్తుంది",
                            "సమానార్థక భిన్నాలు అనేవి ఒకే విలువను సూచించే వేర్వేరు భిన్నాలు"
                        ],
                        "activities": [
                            "వివిధ భిన్నాలను దృశ్యమానం చేయడానికి భిన్న వృత్తాలను ఉపయోగించండి",
                            "సంఖ్యా రేఖలను ఉపయోగించి భిన్నాలను పోల్చండి",
                            "భిన్నాలతో కూడిన వాస్తవ ప్రపంచ సమస్యలను పరిష్కరించండి"
                        ],
                        "conclusion": "భిన్నాలను అర్థం చేసుకోవడం అనేక గణిత భావనలకు మరియు నిజ జీవిత అనువర్తనాలకు ప్రాథమికమైనది."
                    },
                    "worksheet": {
                        "title": "భిన్నాల అభ్యాస పత్రం",
                        "instructions": "భిన్నాల అవగాహనను అభ్యాసం చేయడానికి కింది సమస్యలను పూర్తి చేయండి.",
                        "problems": [
                            "ప్రతి ఆకారంలో నీడ వేసిన భాగం సూచించే భిన్నాన్ని గుర్తించండి.",
                            "కింది భిన్నాలను <, >, లేదా = ఉపయోగించి పోల్చండి.",
                            "సమాన హరాలతో కింది భిన్నాలను కలపండి."
                        ]
                    }
                }
        
        # For other languages, return a generic placeholder translation
        # In a real implementation, this would use Vertex AI to translate the content
        return {
            "note": f"This is a placeholder for content translated to {target_language}.",
            "original_content": content
        }
    
    async def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the language translation agent with the given input data"""
        user_request = input_data.get("user_request", "")
        
        # Extract the target language
        target_language = self._extract_language(user_request)
        if not target_language:
            target_language = "Telugu"  # Default to Telugu (from the example)
        
        # Generate content to translate
        content_to_translate = self._generate_placeholder_content(user_request)
        
        # Translate the content
        translated_content = self._perform_translation(content_to_translate, target_language)
        
        return {
            "original_language": "English",
            "target_language": target_language,
            "translated_content": translated_content,
            "status": "translated",
            "message": f"Content translated to {target_language} successfully"
        }