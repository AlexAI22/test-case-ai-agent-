"""
Test Case Generator AI Agent
Main class that handles the AI processing and test case generation
"""
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.output_parsers import PydanticOutputParser
import json
import re

from .models import TestSuite, TestScenario, UserStoryInput


class TestCaseGenerator:
    """AI Agent for generating test cases from user stories"""
    
    def __init__(self):
        """Initialize the Test Case Generator"""
        load_dotenv()
        
        # Validate environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI model
        self.model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        self.temperature = float(os.getenv("TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=self.api_key
        )
        
        # Set up output parser
        self.output_parser = PydanticOutputParser(pydantic_object=TestSuite)
    
    def validate_user_story(self, user_story: str, acceptance_criteria: List[str] = None) -> UserStoryInput:
        """Validate user story input"""
        try:
            return UserStoryInput(
                story=user_story,
                acceptance_criteria=acceptance_criteria
            )
        except Exception as e:
            raise ValueError(f"Invalid user story input: {str(e)}")
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for the AI agent"""
        return """You are an expert QA engineer and test case generator. Your task is to analyze user stories and generate comprehensive test scenarios.

For each user story, you should:
1. Identify all testable aspects and edge cases
2. Create positive, negative, and boundary test scenarios
3. Include proper test steps, preconditions, and expected results
4. Prioritize tests based on risk and importance
5. Ensure good test coverage

Generate test scenarios that cover:
- Happy path scenarios (positive testing)
- Error scenarios (negative testing)
- Boundary conditions and edge cases
- Integration points
- User experience aspects
- Performance considerations (when relevant)
- Security aspects (when relevant)

Each test scenario should be:
- Clear and unambiguous
- Executable by any QA tester
- Include specific steps and expected outcomes
- Properly categorized by type and priority"""

    def _create_user_prompt(self, validated_input: UserStoryInput) -> str:
        """Create the user prompt with the user story"""
        prompt = f"""Please generate comprehensive test scenarios for the following user story:

**User Story:** {validated_input.story}
"""
        
        if validated_input.acceptance_criteria:
            prompt += f"""
**Acceptance Criteria:**
{chr(10).join(f"- {criteria}" for criteria in validated_input.acceptance_criteria)}
"""
        
        prompt += f"""
Please provide a complete test suite in the following JSON format:
{self.output_parser.get_format_instructions()}

Generate 5-8 diverse test scenarios covering different testing aspects (positive, negative, edge cases, etc.).
Make sure each scenario has a unique ID, clear steps, and specific expected results."""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> TestSuite:
        """Parse the AI response into structured test suite"""
        try:
            # Try to extract JSON from the response if it's wrapped in markdown
            json_match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
            if json_match:
                json_text = json_match.group(1)
            else:
                json_text = response_text
            
            # Parse the JSON
            parsed_data = json.loads(json_text)
            
            # Create TestSuite object
            return TestSuite(**parsed_data)
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            raise ValueError(f"Failed to create TestSuite object: {str(e)}")
    
    def generate_test_cases(self, user_story: str, acceptance_criteria: List[str] = None) -> TestSuite:
        """
        Generate test cases for a given user story
        
        Args:
            user_story: The user story to generate test cases for
            acceptance_criteria: Optional list of acceptance criteria
            
        Returns:
            TestSuite object containing all generated test scenarios
            
        Raises:
            ValueError: If input validation fails or AI response is invalid
            Exception: If API call fails
        """
        try:
            # Validate input
            validated_input = self.validate_user_story(user_story, acceptance_criteria)
            
            # Create prompts
            system_prompt = self._create_system_prompt()
            user_prompt = self._create_user_prompt(validated_input)
            
            # Create messages
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            
            # Get AI response
            response = self.llm.invoke(messages)
            
            # Parse response
            test_suite = self._parse_ai_response(response.content)
            
            # Add metadata
            test_suite.total_scenarios = len(test_suite.test_scenarios)
            
            return test_suite
            
        except Exception as e:
            raise Exception(f"Failed to generate test cases: {str(e)}")
    
    def format_output(self, test_suite: TestSuite, output_format: str = "console") -> str:
        """
        Format the test suite output for different formats
        
        Args:
            test_suite: The generated test suite
            output_format: Format type ("console", "json", "markdown")
            
        Returns:
            Formatted string representation
        """
        if output_format == "json":
            return test_suite.model_dump_json(indent=2)
        
        elif output_format == "markdown":
            return self._format_markdown(test_suite)
        
        else:  # console format
            return self._format_console(test_suite)
    
    def _format_console(self, test_suite: TestSuite) -> str:
        """Format output for console display"""
        output = []
        output.append("=" * 80)
        output.append("TEST CASE GENERATOR RESULTS")
        output.append("=" * 80)
        output.append(f"\nUser Story: {test_suite.user_story}")
        output.append(f"Total Test Scenarios: {test_suite.total_scenarios}")
        output.append(f"Coverage Areas: {', '.join(test_suite.coverage_areas)}")
        output.append("\n" + "=" * 80)
        
        for i, scenario in enumerate(test_suite.test_scenarios, 1):
            output.append(f"\nTEST SCENARIO {i}: {scenario.scenario_id}")
            output.append("-" * 40)
            output.append(f"Title: {scenario.title}")
            output.append(f"Type: {scenario.test_type}")
            output.append(f"Priority: {scenario.priority}")
            output.append(f"\nDescription: {scenario.description}")
            
            output.append(f"\nPreconditions:")
            for precond in scenario.preconditions:
                output.append(f"  • {precond}")
            
            output.append(f"\nTest Steps:")
            for step_num, step in enumerate(scenario.test_steps, 1):
                output.append(f"  {step_num}. {step}")
            
            output.append(f"\nExpected Result: {scenario.expected_result}")
            output.append("-" * 40)
        
        return "\n".join(output)
    
    def _format_markdown(self, test_suite: TestSuite) -> str:
        """Format output as Markdown"""
        output = []
        output.append("# Test Case Generator Results")
        output.append(f"\n**User Story:** {test_suite.user_story}")
        output.append(f"**Total Test Scenarios:** {test_suite.total_scenarios}")
        output.append(f"**Coverage Areas:** {', '.join(test_suite.coverage_areas)}")
        
        for i, scenario in enumerate(test_suite.test_scenarios, 1):
            output.append(f"\n## Test Scenario {i}: {scenario.scenario_id}")
            output.append(f"**Title:** {scenario.title}")
            output.append(f"**Type:** {scenario.test_type}")
            output.append(f"**Priority:** {scenario.priority}")
            output.append(f"\n**Description:** {scenario.description}")
            
            output.append(f"\n**Preconditions:**")
            for precond in scenario.preconditions:
                output.append(f"- {precond}")
            
            output.append(f"\n**Test Steps:**")
            for step_num, step in enumerate(scenario.test_steps, 1):
                output.append(f"{step_num}. {step}")
            
            output.append(f"\n**Expected Result:** {scenario.expected_result}")
        
        return "\n".join(output)