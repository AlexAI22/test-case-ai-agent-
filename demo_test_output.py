"""
Demo Test Output - Test Case Generator AI Agent
This file shows what the actual output would look like when running the agent
"""

# Example Input User Story:
USER_STORY = """
As a registered user, I want to log into my account using my email and password 
so that I can access my personalized dashboard.
"""

ACCEPTANCE_CRITERIA = [
    "User can enter valid email and password",
    "System validates credentials against database", 
    "User is redirected to dashboard on successful login",
    "Error message shown for invalid credentials",
    "Account locked after 3 failed attempts"
]

# Expected Output (what the AI would generate):
EXPECTED_OUTPUT = """
================================================================================
TEST CASE GENERATOR RESULTS
================================================================================

User Story: As a registered user, I want to log into my account using my email and password so that I can access my personalized dashboard.
Total Test Scenarios: 6
Coverage Areas: Authentication, Input Validation, Security, User Interface, Error Handling

================================================================================

TEST SCENARIO 1: TC001
----------------------------------------
Title: Valid Login with Correct Credentials
Type: positive
Priority: high

Description: Verify that a registered user can successfully log in with valid email and password

Preconditions:
  • User account exists in the system
  • Application is accessible and running
  • User has valid email and password credentials

Test Steps:
  1. Navigate to the login page
  2. Enter valid email address in the email field
  3. Enter correct password in the password field
  4. Click the "Login" button

Expected Result: User is successfully authenticated and redirected to their personalized dashboard
----------------------------------------

TEST SCENARIO 2: TC002
----------------------------------------
Title: Invalid Email Format Validation
Type: negative
Priority: medium

Description: Verify that the system properly validates email format and shows appropriate error message

Preconditions:
  • User is on the login page
  • Application is running

Test Steps:
  1. Navigate to the login page
  2. Enter invalid email format (e.g., "invalid-email")
  3. Enter any password
  4. Click the "Login" button

Expected Result: System displays error message "Please enter a valid email address" and does not attempt authentication
----------------------------------------

TEST SCENARIO 3: TC003
----------------------------------------
Title: Empty Credentials Validation
Type: negative
Priority: medium

Description: Verify that the system validates required fields and prevents login with empty credentials

Preconditions:
  • User is on the login page
  • Application is running

Test Steps:
  1. Navigate to the login page
  2. Leave email field empty
  3. Leave password field empty
  4. Click the "Login" button

Expected Result: System displays validation errors for both required fields and prevents form submission
----------------------------------------

TEST SCENARIO 4: TC004
----------------------------------------
Title: Account Lockout After Failed Attempts
Type: security
Priority: high

Description: Verify that user account is locked after 3 consecutive failed login attempts

Preconditions:
  • Valid user account exists
  • Account is not currently locked
  • Application is running

Test Steps:
  1. Navigate to the login page
  2. Enter valid email address
  3. Enter incorrect password
  4. Click "Login" button
  5. Repeat steps 2-4 two more times (total 3 failed attempts)
  6. Attempt to login with correct credentials

Expected Result: After 3 failed attempts, account is locked and error message displays "Account has been locked due to multiple failed login attempts"
----------------------------------------

TEST SCENARIO 5: TC005
----------------------------------------
Title: SQL Injection Prevention
Type: security
Priority: high

Description: Verify that the login form is protected against SQL injection attacks

Preconditions:
  • User is on the login page
  • Application is running

Test Steps:
  1. Navigate to the login page
  2. Enter SQL injection payload in email field (e.g., "admin'; DROP TABLE users; --")
  3. Enter any password
  4. Click the "Login" button

Expected Result: System safely handles the malicious input without executing SQL commands and shows invalid credentials error
----------------------------------------

TEST SCENARIO 6: TC006
----------------------------------------
Title: Password Field Security
Type: security
Priority: medium

Description: Verify that password field masks input and prevents password visibility

Preconditions:
  • User is on the login page
  • Application is running

Test Steps:
  1. Navigate to the login page
  2. Click in the password field
  3. Type any password
  4. Observe the password field display
  5. Check browser developer tools for password visibility

Expected Result: Password characters are masked (shown as dots or asterisks) and password value is not visible in plain text
----------------------------------------
"""

print("🧪 TEST CASE GENERATOR AI AGENT - DEMO OUTPUT")
print("=" * 60)
print(f"Input User Story: {USER_STORY.strip()}")
print(f"Acceptance Criteria: {len(ACCEPTANCE_CRITERIA)} items")
print("\n" + "🤖 AI GENERATED OUTPUT:")
print(EXPECTED_OUTPUT)