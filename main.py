#!/usr/bin/env python3
"""
Command Line Interface for the Test Case Generator AI Agent
"""
import click
import sys
import os
from pathlib import Path
from typing import List, Optional

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.test_case_generator import TestCaseGenerator
from src.models import TestSuite


@click.group()
@click.version_option(version="1.0.0")
def cli():
    """Test Case Generator AI Agent - Generate comprehensive test scenarios from user stories."""
    pass


@cli.command()
@click.option('--story', '-s', required=True, help='User story to generate test cases for')
@click.option('--criteria', '-c', multiple=True, help='Acceptance criteria (can be specified multiple times)')
@click.option('--output', '-o', type=click.Choice(['console', 'json', 'markdown']), default='console', 
              help='Output format')
@click.option('--save', help='Save output to file')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def generate(story: str, criteria: tuple, output: str, save: Optional[str], verbose: bool):
    """Generate test cases from a user story."""
    
    try:
        if verbose:
            click.echo("🚀 Initializing Test Case Generator...")
        
        # Initialize the generator
        generator = TestCaseGenerator()
        
        if verbose:
            click.echo(f"📝 Processing user story: {story[:50]}...")
        
        # Convert criteria tuple to list
        acceptance_criteria = list(criteria) if criteria else None
        
        # Generate test cases
        test_suite = generator.generate_test_cases(story, acceptance_criteria)
        
        if verbose:
            click.echo(f"✅ Generated {test_suite.total_scenarios} test scenarios")
        
        # Format output
        formatted_output = generator.format_output(test_suite, output)
        
        # Display or save output
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(formatted_output)
            click.echo(f"💾 Output saved to: {save}")
        else:
            click.echo(formatted_output)
            
    except ValueError as e:
        click.echo(f"❌ Validation Error: {str(e)}", err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
@click.option('--example', '-e', type=click.Choice(['login', 'ecommerce', 'api', 'mobile']), 
              default='login', help='Example user story to demonstrate')
@click.option('--output', '-o', type=click.Choice(['console', 'json', 'markdown']), default='console',
              help='Output format')
def demo(example: str, output: str):
    """Run demo with predefined user stories."""
    
    examples = {
        'login': {
            'story': 'As a registered user, I want to log into my account using my email and password so that I can access my personalized dashboard.',
            'criteria': [
                'User can enter valid email and password',
                'System validates credentials against database',
                'User is redirected to dashboard on successful login',
                'Error message shown for invalid credentials',
                'Account locked after 3 failed attempts'
            ]
        },
        'ecommerce': {
            'story': 'As a customer, I want to add items to my shopping cart and proceed to checkout so that I can purchase products online.',
            'criteria': [
                'User can add products to cart',
                'Cart displays correct items and quantities',
                'User can modify cart contents',
                'Checkout process calculates total correctly',
                'Payment is processed securely'
            ]
        },
        'api': {
            'story': 'As a developer, I want to integrate with a REST API to retrieve user data so that I can display user profiles in my application.',
            'criteria': [
                'API returns user data in JSON format',
                'Authentication token is required',
                'Rate limiting is enforced',
                'Error responses are properly formatted',
                'Data includes all required user fields'
            ]
        },
        'mobile': {
            'story': 'As a mobile app user, I want to receive push notifications for important updates so that I stay informed about relevant activities.',
            'criteria': [
                'Notifications appear on device lock screen',
                'User can enable/disable notifications',
                'Notifications are categorized by importance',
                'Tapping notification opens relevant app section',
                'Notification history is maintained'
            ]
        }
    }
    
    selected_example = examples[example]
    
    click.echo(f"🎯 Running demo with '{example}' user story...")
    click.echo(f"Story: {selected_example['story']}")
    click.echo()
    
    # Use the generate command logic
    try:
        generator = TestCaseGenerator()
        test_suite = generator.generate_test_cases(
            selected_example['story'], 
            selected_example['criteria']
        )
        
        formatted_output = generator.format_output(test_suite, output)
        click.echo(formatted_output)
        
    except Exception as e:
        click.echo(f"❌ Demo Error: {str(e)}", err=True)
        sys.exit(1)


@cli.command()
def setup():
    """Setup the environment and check configuration."""
    
    click.echo("🔧 Test Case Generator Setup")
    click.echo("=" * 40)
    
    # Check for .env file
    env_file = Path(".env")
    if env_file.exists():
        click.echo("✅ .env file found")
    else:
        click.echo("❌ .env file not found")
        click.echo("Please copy .env.example to .env and add your OpenAI API key")
        return
    
    # Check for OpenAI API key
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            click.echo("✅ OpenAI API key configured")
        else:
            click.echo("❌ OpenAI API key not configured")
            click.echo("Please set OPENAI_API_KEY in your .env file")
            return
    except ImportError:
        click.echo("❌ Required packages not installed")
        click.echo("Please run: pip install -r requirements.txt")
        return
    
    # Test the generator
    try:
        generator = TestCaseGenerator()
        click.echo("✅ Test Case Generator initialized successfully")
        
        # Run a quick test
        test_story = "As a user, I want to test the system."
        result = generator.generate_test_cases(test_story)
        click.echo(f"✅ Test generation successful ({len(result.test_scenarios)} scenarios)")
        
    except Exception as e:
        click.echo(f"❌ Generator test failed: {str(e)}")
        return
    
    click.echo("\n🎉 Setup complete! You can now use the generator.")
    click.echo("Try: python main.py demo --example login")


@cli.command()
@click.argument('input_file', type=click.File('r'))
@click.option('--output', '-o', type=click.Choice(['console', 'json', 'markdown']), default='console')
@click.option('--save', help='Save output to file')
def batch(input_file, output: str, save: Optional[str]):
    """Process multiple user stories from a file."""
    
    click.echo("📦 Processing batch file...")
    
    try:
        import json as json_module
        
        # Read input file (expecting JSON format)
        data = json_module.load(input_file)
        
        if not isinstance(data, list):
            raise ValueError("Input file should contain a JSON array of user stories")
        
        generator = TestCaseGenerator()
        all_results = []
        
        for i, story_data in enumerate(data, 1):
            if isinstance(story_data, str):
                story = story_data
                criteria = None
            else:
                story = story_data.get('story', '')
                criteria = story_data.get('criteria', None)
            
            click.echo(f"Processing story {i}/{len(data)}...")
            
            test_suite = generator.generate_test_cases(story, criteria)
            all_results.append(test_suite)
        
        # Format combined output
        if output == 'json':
            combined_output = json_module.dumps([result.dict() for result in all_results], indent=2)
        else:
            combined_output = "\n\n".join([
                generator.format_output(result, output) for result in all_results
            ])
        
        # Display or save
        if save:
            with open(save, 'w', encoding='utf-8') as f:
                f.write(combined_output)
            click.echo(f"💾 Batch results saved to: {save}")
        else:
            click.echo(combined_output)
            
    except Exception as e:
        click.echo(f"❌ Batch processing error: {str(e)}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    cli()