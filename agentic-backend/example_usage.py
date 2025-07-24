"""
Example usage of Sahayak AI Agentic Backend
============================================

This file demonstrates how to use the Sahayak AI system for generating
educational content for rural multi-grade classrooms.
"""

import requests
import json

# API Base URL (adjust if running on different host/port)
BASE_URL = "http://localhost:8001"

def test_api_health():
    """Test if the API is running and healthy."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ API is healthy!")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def get_capabilities():
    """Get system capabilities."""
    try:
        response = requests.get(f"{BASE_URL}/capabilities")
        if response.status_code == 200:
            capabilities = response.json()
            print("📋 System Capabilities:")
            print(f"  Task Types: {capabilities['supported_task_types']}")
            print(f"  Languages: {capabilities['supported_languages']}")
            print(f"  Grade Range: {capabilities['grade_range']}")
            return capabilities
        else:
            print(f"❌ Failed to get capabilities: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting capabilities: {e}")
        return None

def generate_story_example():
    """Generate an educational story."""
    print("\n📖 Generating Educational Story...")
    
    request_data = {
        "task_type": "story",
        "topic": "importance of trees and forest conservation",
        "grade_level": "3-5",
        "subject": "environmental science",
        "language": "en",
        "context": "rural village setting with local trees and farming"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", json=request_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Story generated successfully!")
            print("\n📝 Generated Story:")
            print("-" * 50)
            print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
            print("-" * 50)
            print(f"📊 Metadata: {result['metadata']}")
            return result
        else:
            print(f"❌ Story generation failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error generating story: {e}")
        return None

def generate_worksheet_example():
    """Generate a differentiated worksheet."""
    print("\n📄 Generating Educational Worksheet...")
    
    request_data = {
        "task_type": "worksheet",
        "topic": "basic arithmetic operations",
        "grade_level": "2-4",
        "subject": "mathematics",
        "language": "hi",  # Hindi
        "additional_params": {
            "skills": "addition, subtraction, word problems"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", json=request_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Worksheet generated successfully!")
            print("\n📝 Generated Worksheet:")
            print("-" * 50)
            print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
            print("-" * 50)
            print(f"📊 Metadata: {result['metadata']}")
            return result
        else:
            print(f"❌ Worksheet generation failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error generating worksheet: {e}")
        return None

def generate_visual_aid_example():
    """Generate a visual aid description."""
    print("\n🎨 Generating Visual Aid...")
    
    request_data = {
        "task_type": "visual_aid",
        "topic": "water cycle",
        "grade_level": "4-6",
        "subject": "science",
        "language": "te",  # Telugu
        "additional_params": {
            "objective": "understand the stages of water cycle"
        }
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", json=request_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Visual aid generated successfully!")
            print("\n📝 Generated Visual Aid:")
            print("-" * 50)
            print(result['content'][:500] + "..." if len(result['content']) > 500 else result['content'])
            print("-" * 50)
            print(f"📊 Metadata: {result['metadata']}")
            return result
        else:
            print(f"❌ Visual aid generation failed: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"❌ Error generating visual aid: {e}")
        return None

def analyze_natural_input_example():
    """Analyze natural language input from a teacher."""
    print("\n🔍 Analyzing Natural Language Input...")
    
    examples = [
        "I need a story about honesty for my grade 3 students in Hindi",
        "Create math exercises for grades 2 to 4 on multiplication",
        "Help me draw a diagram showing parts of a flower for science class"
    ]
    
    for user_input in examples:
        print(f"\n📝 Input: '{user_input}'")
        
        request_data = {
            "user_input": user_input,
            "language": "en"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/analyze", json=request_data)
            if response.status_code == 200:
                result = response.json()
                if result['success']:
                    print("✅ Analysis successful!")
                    print(f"   Detected task: {result['task_request']}")
                else:
                    print("⚠️  Analysis needs improvement:")
                    print(f"   Suggestions: {result['suggestions']}")
            else:
                print(f"❌ Analysis failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Error analyzing input: {e}")

def get_language_support():
    """Get information about supported languages."""
    print("\n🌍 Language Support Information...")
    
    try:
        response = requests.get(f"{BASE_URL}/languages")
        if response.status_code == 200:
            lang_info = response.json()
            print("✅ Language information retrieved!")
            print(f"   Supported: {lang_info['supported_languages']}")
            print(f"   Default: {lang_info['default_language']}")
            for lang, details in lang_info['language_details'].items():
                print(f"   {lang}: {details['name']} ({details['script']} script)")
        else:
            print(f"❌ Failed to get language info: {response.status_code}")
    except Exception as e:
        print(f"❌ Error getting language info: {e}")

def get_task_templates():
    """Get example templates for different task types."""
    print("\n📋 Task Templates...")
    
    task_types = ["story", "worksheet", "visual_aid"]
    
    for task_type in task_types:
        try:
            response = requests.get(f"{BASE_URL}/tasks/{task_type}/template")
            if response.status_code == 200:
                template = response.json()
                print(f"\n📝 {task_type.title()} Template:")
                print(f"   Example Request: {template['example_request']}")
                print(f"   Expected Output: {template['expected_output']}")
            else:
                print(f"❌ Failed to get {task_type} template: {response.status_code}")
        except Exception as e:
            print(f"❌ Error getting {task_type} template: {e}")

def main():
    """Run all examples."""
    print("🎯 Sahayak AI Agentic Backend - Example Usage")
    print("=" * 60)
    
    # Test API health first
    if not test_api_health():
        print("\n❌ API is not available. Please start the server first:")
        print("   cd agentic-backend")
        print("   ./start.sh")
        return
    
    # Get system capabilities
    get_capabilities()
    
    # Get language support info
    get_language_support()
    
    # Get task templates
    get_task_templates()
    
    # Test content generation
    generate_story_example()
    generate_worksheet_example()
    generate_visual_aid_example()
    
    # Test natural language analysis
    analyze_natural_input_example()
    
    print("\n✅ Example usage complete!")
    print("\n📚 Next steps:")
    print("   - Integrate with your frontend application")
    print("   - Customize prompts for your specific needs")
    print("   - Add authentication and user management")
    print("   - Scale for production deployment")

if __name__ == "__main__":
    # Check if requests library is available
    try:
        import requests
    except ImportError:
        print("❌ 'requests' library not found. Install it with:")
        print("   pip install requests")
        exit(1)
    
    main()
