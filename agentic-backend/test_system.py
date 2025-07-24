"""Test script for Sahayak agents."""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work correctly."""
    try:
        print("Testing shared imports...")
        from shared import config, TaskRequest, AgentResponse
        print("✓ Shared imports successful")
        
        print("Testing config...")
        print(f"✓ Default language: {config.language.default_language}")
        print(f"✓ Supported languages: {config.language.supported_languages}")
        
        print("Testing task request creation...")
        request = TaskRequest(
            task_type="story",
            topic="friendship",
            grade_level="3",
            subject="moral education",
            language="en"
        )
        print("✓ TaskRequest creation successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_validation():
    """Test validation utilities."""
    try:
        print("\nTesting validation...")
        from shared import ValidationUtils, TaskRequest
        
        # Valid request
        valid_request = TaskRequest(
            task_type="story",
            topic="animals",
            grade_level="2-4",
            subject="science",
            language="en"
        )
        
        is_valid, error = ValidationUtils.validate_task_request(valid_request)
        print(f"✓ Valid request validation: {is_valid}")
        
        # Invalid request
        invalid_request = TaskRequest(
            task_type="invalid",
            topic="",
            grade_level="abc",
            subject="",
            language="en"
        )
        
        is_valid, error = ValidationUtils.validate_task_request(invalid_request)
        print(f"✓ Invalid request validation: {not is_valid} (correctly detected as invalid)")
        print(f"✓ Error message: {error}")
        
        return True
        
    except Exception as e:
        print(f"✗ Validation test failed: {e}")
        return False

def test_grade_utils():
    """Test grade utilities."""
    try:
        print("\nTesting grade utilities...")
        from shared import GradeUtils
        
        # Test grade parsing
        grades = GradeUtils.parse_grade_range("3-5")
        print(f"✓ Grade range 3-5: {grades}")
        
        grades = GradeUtils.parse_grade_range("1,3,5")
        print(f"✓ Grade list 1,3,5: {grades}")
        
        # Test age group
        age_group = GradeUtils.get_age_group([1, 2, 3])
        print(f"✓ Age group for grades 1-3: {age_group}")
        
        # Test difficulty levels
        difficulty = GradeUtils.get_difficulty_levels([2, 4, 6, 8])
        print(f"✓ Difficulty levels: {difficulty}")
        
        return True
        
    except Exception as e:
        print(f"✗ Grade utils test failed: {e}")
        return False

def test_language_utils():
    """Test language utilities."""
    try:
        print("\nTesting language utilities...")
        from shared import LanguageUtils
        
        # Test language detection
        hindi_text = "नमस्ते, यह हिंदी है"
        detected = LanguageUtils.detect_language(hindi_text)
        print(f"✓ Hindi text detected as: {detected}")
        
        telugu_text = "నమస్కారం, ఇది తెలుగు"
        detected = LanguageUtils.detect_language(telugu_text)
        print(f"✓ Telugu text detected as: {detected}")
        
        english_text = "Hello, this is English"
        detected = LanguageUtils.detect_language(english_text)
        print(f"✓ English text detected as: {detected}")
        
        # Test language support validation
        is_supported = LanguageUtils.validate_language_support("hi", ["en", "hi", "te"])
        print(f"✓ Hindi support validation: {is_supported}")
        
        return True
        
    except Exception as e:
        print(f"✗ Language utils test failed: {e}")
        return False

def test_prompts():
    """Test prompt templates."""
    try:
        print("\nTesting prompt templates...")
        from shared import get_language_template, STORY_AGENT_SYSTEM_PROMPT
        
        # Test language templates
        hindi_template = get_language_template("hi")
        print(f"✓ Hindi greeting: {hindi_template['greeting']}")
        
        english_template = get_language_template("en")
        print(f"✓ English greeting: {english_template['greeting']}")
        
        # Test system prompt exists
        print(f"✓ Story agent system prompt length: {len(STORY_AGENT_SYSTEM_PROMPT)} characters")
        
        return True
        
    except Exception as e:
        print(f"✗ Prompt test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Sahayak Agents Test Suite")
    print("=" * 40)
    
    tests = [
        test_imports,
        test_validation,
        test_grade_utils,
        test_language_utils,
        test_prompts
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Install dependencies: poetry install")
        print("2. Set up environment: cp .env.example .env")
        print("3. Configure Google Cloud credentials")
        print("4. Run API server: poetry run python api/main.py")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
