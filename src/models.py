"""
Data models for the Test Case Generator AI Agent
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class TestScenario(BaseModel):
    """Represents a single test scenario"""
    scenario_id: str = Field(description="Unique identifier for the test scenario")
    title: str = Field(description="Brief title describing the test scenario")
    description: str = Field(description="Detailed description of what to test")
    preconditions: List[str] = Field(description="Prerequisites for the test")
    test_steps: List[str] = Field(description="Step-by-step instructions")
    expected_result: str = Field(description="Expected outcome of the test")
    test_type: str = Field(description="Type of test (positive, negative, edge case)")
    priority: str = Field(description="Test priority (high, medium, low)")


class TestSuite(BaseModel):
    """Represents a complete test suite for a user story"""
    user_story: str = Field(description="Original user story")
    test_scenarios: List[TestScenario] = Field(description="Generated test scenarios")
    coverage_areas: List[str] = Field(description="Areas of functionality covered")
    total_scenarios: int = Field(description="Total number of test scenarios")


class UserStoryInput(BaseModel):
    """Input validation for user stories"""
    story: str = Field(min_length=10, description="User story description")
    acceptance_criteria: Optional[List[str]] = Field(default=None, description="Optional acceptance criteria")
    story_type: Optional[str] = Field(default="feature", description="Type of user story")