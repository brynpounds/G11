# test_game.py

import redis
import json
import random
from normalize import normalize_sentence
from sentence_transformer import calculate_cosine_similarity
from structured_llm_grading import llm_grade

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_random_ticket():
    data = r.get("game_data")
    if not data:
        print("❌ Could not find 'game_data' in Redis.")
        return None

    game_data = json.loads(data)
    tickets = game_data.get("trouble_tickets", [])

    if not tickets:
        print("❌ No trouble tickets found.")
        return None

    return random.choice(tickets)

def display_ticket(ticket):
    print("\n🎫 Trouble Ticket")
    print(f"ID:             {ticket['id']}")
    print(f"Description:    {ticket['description']}")
    print(f"Root Cause:     {ticket['root_cause']}")
    print(f"Minimal Credit: {ticket['minimal_credit']}")
    print(f"Partial Credit: {ticket['partial_credit']}")
    print(f"Full Credit:    {ticket['full_credit']}")

def compare_with_credits(normalized_input, ticket):
    print("\n📊 Cosine Similarity Scores:")
    credit_fields = {
        "Minimal Credit": ticket.get("minimal_credit", ""),
        "Partial Credit": ticket.get("partial_credit", ""),
        "Full Credit": ticket.get("full_credit", "")
    }

    winner = False
    for label, reference in credit_fields.items():
        if reference.strip():
            similarity = calculate_cosine_similarity(normalized_input, reference)
            print(f"{label}: {similarity:.4f}")
            if similarity > 0.5:
                winner = True

    if not winner:
        print("\n❌ Not close enough. Try again next time!")
        return False

    print("\n🎉 Winner Winner Chicken Dinner!")
    return True

def main():
    ticket = get_random_ticket()
    if not ticket:
        return

    display_ticket(ticket)

    user_input = input("\n🧠 Enter your diagnostic response: ").strip()
    if not user_input:
        print("⚠️ No response entered.")
        return

    normalized = normalize_sentence(user_input)

    print("\n✅ Normalized Response:")
    print(normalized)

    passed_similarity = compare_with_credits(normalized, ticket)

    if not passed_similarity:
        return  # Exit early if similarity check fails

    print("\n🧠 Submitting to LLM for final grading...")
    grade, feedback = llm_grade(user_input, ticket)

    print(f"\n🏁 Final Grade: {grade}")
    print(f"📝 Feedback: {feedback}")

if __name__ == "__main__":
    main()

