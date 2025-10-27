"""
Simple Test Script - Validates Code Structure Without API Calls
This tests the basic functionality without requiring OpenAI API
"""
import sys
from pathlib import Path

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        from src.models import TestSuite, TestScenario, UserStoryInput
        print("✅ Models imported successfully")
        
        # Test UserStoryInput validation
        valid_story = UserStoryInput(
            story="As a user, I want to test the system functionality",
            acceptance_criteria=["Valid input required", "Error handling needed"]
        )
        print("✅ UserStoryInput validation works")
        print(f"   Story: {valid_story.story[:50]}...")
        print(f"   Criteria: {len(valid_story.acceptance_criteria)} items")
        
        # Test TestScenario creation
        test_scenario = TestScenario(
            scenario_id="TC001",
            title="Test login functionality",
            description="Verify user can login with valid credentials",
            preconditions=["User account exists", "Application is running"],
            test_steps=["Navigate to login", "Enter credentials", "Click login"],
            expected_result="User is logged in successfully",
            test_type="positive",
            priority="high"
        )
        print("✅ TestScenario creation works")
        print(f"   Scenario ID: {test_scenario.scenario_id}")
        print(f"   Title: {test_scenario.title}")
        print(f"   Type: {test_scenario.test_type}")
        
        # Test TestSuite creation
        test_suite = TestSuite(
            user_story="Test user story",
            test_scenarios=[test_scenario],
            coverage_areas=["Authentication", "UI"],
            total_scenarios=1
        )
        print("✅ TestSuite creation works")
        print(f"   Total scenarios: {test_suite.total_scenarios}")
        print(f"   Coverage areas: {', '.join(test_suite.coverage_areas)}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Validation error: {e}")
        return False

def test_cli_structure():
    """Test that CLI structure is valid"""
    try:
        import click
        print("✅ Click library available")
        
        # Read main.py to verify structure
        main_file = Path(__file__).parent / "main.py"
        if main_file.exists():
            content = main_file.read_text()
            
            # Check for key CLI components
            checks = [
                ("@click.group()", "CLI group decorator"),
                ("@cli.command()", "CLI commands"),
                ("def generate(", "Generate command function"),
                ("def demo(", "Demo command function"),
                ("def setup(", "Setup command function"),
                ("TestCaseGenerator", "Main generator class usage")
            ]
            
            for check, description in checks:
                if check in content:
                    print(f"✅ {description} found")
                else:
                    print(f"❌ {description} missing")
            
            return True
        else:
            print("❌ main.py not found")
            return False
            
    except ImportError:
        print("❌ Click library not available")
        return False
    except Exception as e:
        print(f"❌ CLI test error: {e}")
        return False

def test_project_structure():
    """Test that project has proper structure"""
    expected_files = [
        "main.py",
        "requirements.txt", 
        ".env.example",
        "src/__init__.py",
        "src/models.py",
        "src/test_case_generator.py",
        "tests/__init__.py",
        "tests/test_generator.py",
        "examples/sample_user_stories.json",
        "README.md",
        "LICENSE",
        ".gitignore"
    ]
    
    base_path = Path(__file__).parent
    missing_files = []
    
    for file_path in expected_files:
        if not (base_path / file_path).exists():
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Run all tests"""
    print("🧪 RUNNING SIMPLE VALIDATION TESTS")
    print("=" * 50)
    
    print("\n📁 Testing Project Structure:")
    structure_ok = test_project_structure()
    
    print("\n📦 Testing Module Imports:")
    imports_ok = test_imports()
    
    print("\n🖥️  Testing CLI Structure:")
    cli_ok = test_cli_structure()
    
    print("\n" + "=" * 50)
    if structure_ok and imports_ok and cli_ok:
        print("🎉 ALL TESTS PASSED - Project is ready!")
        print("💡 To run with real AI:")
        print("   1. Install Python and dependencies: pip install -r requirements.txt")
        print("   2. Add OpenAI API key to .env file")
        print("   3. Run: python main.py demo --example login")
    else:
        print("❌ Some tests failed - check output above")

if __name__ == "__main__":
    main()