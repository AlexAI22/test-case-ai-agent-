"""
Unit tests for the Test Case Generator AI Agent
"""
import unittest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from src.test_case_generator import TestCaseGenerator
from src.models import TestSuite, TestScenario, UserStoryInput


class TestUserStoryInput(unittest.TestCase):
    """Test the UserStoryInput validation"""
    
    def test_valid_user_story(self):
        """Test valid user story input"""
        story = "As a user, I want to login to my account"
        criteria = ["Valid credentials required", "Error handling for invalid login"]
        
        input_obj = UserStoryInput(story=story, acceptance_criteria=criteria)
        
        self.assertEqual(input_obj.story, story)
        self.assertEqual(input_obj.acceptance_criteria, criteria)
        self.assertEqual(input_obj.story_type, "feature")
    
    def test_invalid_short_story(self):
        """Test validation fails for too short story"""
        with self.assertRaises(Exception):
            UserStoryInput(story="Short")
    
    def test_optional_criteria(self):
        """Test that acceptance criteria is optional"""
        story = "As a user, I want to test the system functionality"
        input_obj = UserStoryInput(story=story)
        
        self.assertEqual(input_obj.story, story)
        self.assertIsNone(input_obj.acceptance_criteria)


class TestTestCaseGenerator(unittest.TestCase):
    """Test the main TestCaseGenerator class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_response = Mock()
        self.mock_response.content = '''
        {
            "user_story": "Test story",
            "test_scenarios": [
                {
                    "scenario_id": "TC001",
                    "title": "Valid login test",
                    "description": "Test successful login with valid credentials",
                    "preconditions": ["User account exists", "Application is running"],
                    "test_steps": ["Enter valid email", "Enter valid password", "Click login"],
                    "expected_result": "User is logged in successfully",
                    "test_type": "positive",
                    "priority": "high"
                }
            ],
            "coverage_areas": ["Authentication", "User Interface"],
            "total_scenarios": 1
        }
        '''
    
    def test_validate_user_story_valid(self):
        """Test user story validation with valid input"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            
            result = generator.validate_user_story(
                "As a user, I want to login to my account",
                ["Valid credentials required"]
            )
            
            self.assertIsInstance(result, UserStoryInput)
            self.assertEqual(result.story, "As a user, I want to login to my account")
            self.assertEqual(result.acceptance_criteria, ["Valid credentials required"])
    
    def test_validate_user_story_invalid(self):
        """Test user story validation with invalid input"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            
            with self.assertRaises(ValueError):
                generator.validate_user_story("Short")
    
    def test_environment_validation(self):
        """Test that environment variables are properly validated"""
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError) as context:
                TestCaseGenerator()
            
            self.assertIn("OPENAI_API_KEY not found", str(context.exception))
    
    @patch('src.test_case_generator.ChatOpenAI')
    def test_generate_test_cases_success(self, mock_chat_openai):
        """Test successful test case generation"""
        # Mock the OpenAI response
        mock_llm = Mock()
        mock_llm.invoke.return_value = self.mock_response
        mock_chat_openai.return_value = mock_llm
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            
            result = generator.generate_test_cases(
                "As a user, I want to login to my account",
                ["Valid credentials required"]
            )
            
            self.assertIsInstance(result, TestSuite)
            self.assertEqual(result.user_story, "Test story")
            self.assertEqual(len(result.test_scenarios), 1)
            self.assertEqual(result.test_scenarios[0].scenario_id, "TC001")
    
    def test_format_output_console(self):
        """Test console output formatting"""
        test_scenario = TestScenario(
            scenario_id="TC001",
            title="Test login",
            description="Test user login",
            preconditions=["User exists"],
            test_steps=["Enter credentials", "Click login"],
            expected_result="User logged in",
            test_type="positive",
            priority="high"
        )
        
        test_suite = TestSuite(
            user_story="Test story",
            test_scenarios=[test_scenario],
            coverage_areas=["Authentication"],
            total_scenarios=1
        )
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            output = generator.format_output(test_suite, "console")
            
            self.assertIn("TEST CASE GENERATOR RESULTS", output)
            self.assertIn("Test story", output)
            self.assertIn("TC001", output)
            self.assertIn("Test login", output)
    
    def test_format_output_json(self):
        """Test JSON output formatting"""
        test_scenario = TestScenario(
            scenario_id="TC001",
            title="Test login",
            description="Test user login",
            preconditions=["User exists"],
            test_steps=["Enter credentials", "Click login"],
            expected_result="User logged in",
            test_type="positive",
            priority="high"
        )
        
        test_suite = TestSuite(
            user_story="Test story",
            test_scenarios=[test_scenario],
            coverage_areas=["Authentication"],
            total_scenarios=1
        )
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            output = generator.format_output(test_suite, "json")
            
            self.assertIn('"user_story": "Test story"', output)
            self.assertIn('"scenario_id": "TC001"', output)
    
    def test_format_output_markdown(self):
        """Test Markdown output formatting"""
        test_scenario = TestScenario(
            scenario_id="TC001",
            title="Test login",
            description="Test user login",
            preconditions=["User exists"],
            test_steps=["Enter credentials", "Click login"],
            expected_result="User logged in",
            test_type="positive",
            priority="high"
        )
        
        test_suite = TestSuite(
            user_story="Test story",
            test_scenarios=[test_scenario],
            coverage_areas=["Authentication"],
            total_scenarios=1
        )
        
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'}):
            generator = TestCaseGenerator()
            output = generator.format_output(test_suite, "markdown")
            
            self.assertIn("# Test Case Generator Results", output)
            self.assertIn("**User Story:** Test story", output)
            self.assertIn("## Test Scenario 1: TC001", output)


if __name__ == '__main__':
    unittest.main()