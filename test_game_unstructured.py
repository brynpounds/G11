# test_game.py

import redis
import json
import random
from normalize import normalize_sentence
from unstructured_llm_grading import evaluate_unstructured_from_root_cause

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_random_network_issue():
    data = r.get("game_data")
    if not data:
        print("❌ Could not find 'game_data' in Redis.")
        return None

    game_data = json.loads(data)
    issues = game_data.get("network_issues", [])

    if not issues:
        print("❌ No network issues found in Redis.")
        return None

    return random.choice(issues)

def display_issue(issue):
    print("\n🌐 Network Issue")
    print(f"ID:          {issue['id']}")
    print(f"Issue:       {issue['issue']}")
    print(f"Root Cause:  {issue['root_cause']}")
    print(f"Scoring:     {issue['scoring']}")

def main():
    issue = get_random_network_issue()
    if not issue:
        return

    display_issue(issue)

    user_input = input("\n🧠 Enter your troubleshooting response: ").strip()
    if not user_input:
        print("⚠️ No response entered.")
        return

    normalized = normalize_sentence(user_input)

    print("\n✅ Normalized Response:")
    print(normalized)

    print("\n🧠 Submitting to LLM for unstructured grading...")
    root_cause = issue.get("root_cause", "")
    score, reason = evaluate_unstructured_from_root_cause(root_cause, normalized)

    print(f"\n🏁 Score: {score}")
    print(f"📝 Feedback: {reason}")

if __name__ == "__main__":
    main()

