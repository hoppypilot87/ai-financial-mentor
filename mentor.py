# -----------------------------------------------------------------------------------
# AI Mentor Service with Free/Pro Limits + Brief/Detailed Toggle
# -----------------------------------------------------------------------------------
import os
import datetime
import json
from dotenv import load_dotenv
from openai import OpenAI

# ✅ Load .env for local dev
load_dotenv()

# ✅ API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ No OPENAI_API_KEY found. Set it in .env or as an environment variable.")

# ✅ Initialize OpenAI
client = OpenAI(api_key=api_key)

# ✅ Paths for usage tracking
USAGE_FILE = "usage_tracker.json"

# ✅ Plan limits
LIMITS = {
    "free": {"daily": 1, "monthly": 30},
    "pro": {"daily": 10, "monthly": 250}  # hidden cap prevents abuse
}

# ✅ Load or create usage tracker
def load_usage():
    if not os.path.exists(USAGE_FILE):
        return {"date": str(datetime.date.today()), "daily_count": 0, "monthly_count": 0}
    with open(USAGE_FILE, "r") as f:
        return json.load(f)

def save_usage(data):
    with open(USAGE_FILE, "w") as f:
        json.dump(data, f)

# ✅ Reset counters if day/month changed
def reset_usage_if_needed(usage):
    today = datetime.date.today()
    last_date = datetime.datetime.strptime(usage["date"], "%Y-%m-%d").date()

    # Reset daily count if a new day
    if today > last_date:
        usage["daily_count"] = 0
        # Reset monthly if we’re in a new month
        if today.month != last_date.month:
            usage["monthly_count"] = 0
        usage["date"] = str(today)
    return usage

# ✅ Check usage limit
def check_usage(plan="free"):
    usage = load_usage()
    usage = reset_usage_if_needed(usage)
    save_usage(usage)

    daily_limit = LIMITS[plan]["daily"]
    monthly_limit = LIMITS[plan]["monthly"]

    # ✅ Allow the call if still below the limit
    if usage["daily_count"] < daily_limit and usage["monthly_count"] < monthly_limit:
        return True, usage

    # ✅ Block only when already AT or OVER limit
    if usage["daily_count"] >= daily_limit:
        return False, f"🚫 Daily limit reached for **{plan.upper()}** plan ({daily_limit}/day). Try again tomorrow or upgrade!"
    if usage["monthly_count"] >= monthly_limit:
        return False, f"🚫 Monthly limit reached for **{plan.upper()}** plan ({monthly_limit}/month). Upgrade for more access!"

    return True, usage

# ✅ Increment usage after valid query
def increment_usage(usage):
    usage["daily_count"] += 1
    usage["monthly_count"] += 1
    save_usage(usage)

# ✅ Disclaimer
DISCLAIMER = (
    "⚠️ *Disclaimer: This is AI-generated financial information for educational purposes only.*\n"
    "*It is NOT personalized financial advice. Always consult a certified financial professional before making investment decisions.*\n\n"
)

# ✅ Persona prompts
PERSONA_PROMPTS = {
    "warren_buffett": "You are Warren Buffett, the legendary value investor. Give calm, long-term, rational advice.",
    "financial_coach": "You are a friendly financial coach focused on budgeting, saving, and debt reduction.",
    "budgeting_expert": "You are a budgeting guru who provides step-by-step guidance.",
    "generic": "You are a helpful financial assistant who explains things clearly and simply."
}

def ask_ai_mentor(persona: str, question: str, plan: str = "free", mode: str = "brief") -> str:
    """
    Ask the AI Mentor a financial question with usage tracking.
    
    ✅ Fix: Always allow the first question,
       increment AFTER success, THEN block future calls if over limit.
    """

    # ✅ Load and reset usage
    usage = load_usage()
    usage = reset_usage_if_needed(usage)
    save_usage(usage)

    daily_limit = LIMITS[plan]["daily"]
    monthly_limit = LIMITS[plan]["monthly"]

    # ✅ If ALREADY exceeded limit → block immediately
    if usage["daily_count"] >= daily_limit or usage["monthly_count"] >= monthly_limit:
        return f"🚫 You've reached your **{plan.upper()}** plan limit ({daily_limit}/day). Try again tomorrow or upgrade!"

    # ✅ Persona style
    style_prompt = PERSONA_PROMPTS.get(persona.lower(), PERSONA_PROMPTS["generic"])

    # ✅ Adjust question for mode
    if mode == "brief":
        question = f"Answer very briefly in 3-4 sentences max. {question}"
    else:
        question = f"Provide a concise but more detailed explanation. {question}"

    # ✅ Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": style_prompt},
            {"role": "user", "content": question}
        ]
    )

    ai_reply = response.choices[0].message.content.strip()

    # ✅ Increment usage ONLY AFTER SUCCESSFUL RESPONSE
    usage["daily_count"] += 1
    usage["monthly_count"] += 1
    save_usage(usage)

    return DISCLAIMER + ai_reply

# ✅ Demo usage
if __name__ == "__main__":
    print("🤖 AI Mentor Demo\n")

    # Simulate a FREE user asking a brief question
    user_plan = "free"  # change to "pro" to test Pro plan
    sample_question = "Should I pay off debt before investing?"

    reply = ask_ai_mentor(
        persona="financial_coach",
        question=sample_question,
        plan=user_plan,
        mode="brief"  # or "detailed"
    )
    print(reply)

    print("\n=== Simulating Free Plan Usage ===")
    for attempt in range(3):
        print(f"\nAttempt #{attempt + 1}")
        reply = ask_ai_mentor(
            persona="financial_coach",
            question="Should I invest in index funds?",
            plan="free",
            mode="brief"
        )
        print(reply)
