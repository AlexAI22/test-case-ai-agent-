# AI Test Case Generator (User Story → Structured Test Scenarios)

## Overview
This tool converts a plain agile user story (optionally with acceptance criteria) into a structured set of test scenarios covering:
- Core functional flows
- Data validation & field rules
- Boundary & edge cases
- Negative & error handling
- Security & privacy considerations
- Performance / resilience hints
- Risk-based prioritization

## Why This Helps QA
Manual scenario design is time-consuming and subject to coverage gaps. This agent accelerates initial design while maintaining structure and traceability to the source story.

## Features
- Validates user story format (title, narrative, criteria).
- Extracts actors, intentions, and core actions heuristically.
- Uses LLM to expand into categorized scenarios.
- Enforces deterministic JSON schema via Pydantic.
- Fallback heuristic generator if LLM output malformed.
- Produces both JSON and Markdown summary.
- CLI interface for quick usage.
- Extensible architecture (plug-in future analyzers).

## Quick Start

### 1. Requirements
Python 3.11+
OpenAI API Key (or Azure/OpenAI compatible endpoint)

### 2. Install
```bash
git clone https://github.com/AlexAI22/test-case-ai-agent-.git test-case-ai-agent
cd test-case-ai-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-***
```

### 3. Run
```bash
python main.py generate --story-file samples/story_login.md --output out/login_scenarios.json
```

### 4. Output
- JSON: Structured test scenario set
- Markdown: Summary file (if --markdown-out specified)

### Example
Input (story_login.md):
```
Title: User Login
As a registered user
I want to log into the system
So that I can access my personalized dashboard

Acceptance Criteria:
1. Valid username + password logs in
2. Invalid password shows error
3. Locked account prevents login
4. Rate limit after 5 failed attempts
```

CLI Output snippet (console):
```
[INFO] Parsed actors: ["registered user"]
[INFO] Generated 18 scenarios (High: 6 / Medium: 8 / Low: 4)
```

JSON (excerpt):
```json
{
  "metadata": {
    "story_title": "User Login",
    "actors": ["registered user"],
    "primary_goal": "log into the system",
    "acceptance_criteria_count": 4
  },
  "scenarios": [
    {
      "id": "FUNC-001",
      "category": "functional-core",
      "title": "Successful login with valid credentials",
      "steps": ["Open login page", "Enter valid username", "Enter valid password", "Submit", "Verify dashboard displayed"],
      "expected_result": "User is redirected to dashboard",
      "priority": "High",
      "risk_rationale": "Critical path to value delivery",
      "trace": ["AC1"]
    }
  ]
}
```

## CLI Options
```bash
python main.py generate \
  --story-file samples/story_login.md \
  --model gpt-4o-mini \
  --temperature 0.3 \
  --output out/login.json \
  --markdown-out out/login.md \
  --max-scenarios 25
```

| Flag | Description | Default |
|------|-------------|---------|
| --story-file | Path to user story text/markdown | REQUIRED |
| --model | OpenAI model name | gpt-4o-mini |
| --temperature | LLM creativity control | 0.3 |
| --max-scenarios | Upper bound scenarios | 30 |
| --output | JSON output path | out/scenarios.json |
| --markdown-out | Optional summary markdown | None |
| --dry-run | Skip LLM, only heuristic | False |

## Architecture
```
main.py (CLI) 
   -> agent.py (Orchestrator)
         -> story_parser.py (Extract structure)
         -> llm_chain.py (Prompt + LangChain call)
         -> postprocess.py (Validation, fallback)
         -> schemas.py (Pydantic models)
         -> prioritization.py (Risk scoring)
```

## Prompt Strategy
- System prompt sets QA context.
- User content contains normalized story plus extracted heuristics.
- Output forced to JSON schema (no prose).
- On validation failure → fallback heuristic scenarios enriched with smaller LLM calls or entirely rule-based if repeated failure.

## Error Handling
- Missing acceptance criteria: warns & proceeds.
- LLM non-JSON output: attempts cleaning; if still invalid → fallback.
- API failure: automatic retry (2 attempts w/backoff).
- Scenario deduplication by normalized title hash.

## Fallback Heuristic Logic (Summary)
1. Generate baseline: each acceptance criterion → one functional scenario.
2. Add negative scenario for each criterion involving validation.
3. Add boundary scenarios for numeric or count-based artifacts (e.g., rate limit).
4. Add security scenario if credentials or sessions involved.
5. Prioritize using weight map.

## Testing
Run basic tests:
```bash
pytest -q
```

## Limitations
- Complex multi-actor workflows may need manual refinement.
- Domain-specific validations (e.g., financial rounding) not auto-derived unless explicitly stated.
- Performance & load scenarios are high-level hints (not JMeter plans).

## Future Improvements
- Embeddings to compare new story against archived scenarios.
- Export to test management tools (TestRail, Xray) via adapters.
- Pairwise input combinatorics generator for form fields.
- Multi-language story parsing (currently English-focused).

## Contributing
1. Fork & branch: `feature/add-security-detection`
2. Add/modify module
3. PR with test updates

## License
MIT (Adjust as needed)