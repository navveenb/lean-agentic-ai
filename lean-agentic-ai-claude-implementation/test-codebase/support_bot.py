"""
Sample App: Customer Support Bot
This is a DELIBERATELY wasteful codebase for testing the /cost-analyzer workflow.
Every LLM call uses claude-opus (frontier model) — most of them shouldn't.
"""

import anthropic

client = anthropic.Anthropic()


# ============================================================
# CALL 1: Spam Classification
# Task: Yes/No classification — should be Tier 1 (Haiku)
# Currently: Using Opus ($15/1M input) for a yes/no answer
# ============================================================
def classify_spam(email_text: str) -> bool:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=10,
        messages=[
            {"role": "user", "content": f"Is this email spam? Reply only YES or NO.\n\n{email_text}"}
        ]
    )
    return "YES" in response.content[0].text.upper()


# ============================================================
# CALL 2: Entity Extraction
# Task: Extract name + email from text — should be Tier 1 (Haiku)
# Currently: Using Opus for simple extraction
# ============================================================
def extract_contact_info(text: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=200,
        system="Extract the person's name and email address from the text. Return JSON: {\"name\": \"...\", \"email\": \"...\"}",
        messages=[
            {"role": "user", "content": text}
        ]
    )
    return response.content[0].text


# ============================================================
# CALL 3: Sentiment Analysis
# Task: Classify sentiment — should be Tier 1 (Haiku)
# Currently: Using Opus for 3-way classification
# ============================================================
def analyze_sentiment(message: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=20,
        messages=[
            {"role": "user", "content": f"What is the sentiment of this message? Reply POSITIVE, NEGATIVE, or NEUTRAL only.\n\n{message}"}
        ]
    )
    return response.content[0].text.strip()


# ============================================================
# CALL 4: Ticket Routing
# Task: Route to department — should be Tier 1 (Haiku)
# Currently: Using Opus for simple routing
# ============================================================
def route_ticket(ticket_text: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=30,
        messages=[
            {"role": "user", "content": f"Which department should handle this ticket? Reply with one of: BILLING, TECHNICAL, SALES, GENERAL.\n\n{ticket_text}"}
        ]
    )
    return response.content[0].text.strip()


# ============================================================
# CALL 5: Summarize Customer Conversation
# Task: Summarize a single conversation — should be Tier 2 (Sonnet)
# Currently: Using Opus for single-doc summarization
# ============================================================
def summarize_conversation(conversation: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=500,
        system="Summarize this customer support conversation in 2-3 sentences.",
        messages=[
            {"role": "user", "content": conversation}
        ]
    )
    return response.content[0].text


# ============================================================
# CALL 6: Draft Reply Email
# Task: Draft a reply — should be Tier 2 (Sonnet)
# Currently: Using Opus for template-based drafting
# ============================================================
def draft_reply(customer_message: str, resolution: str) -> str:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=800,
        system="You are a friendly customer support agent. Draft a reply email.",
        messages=[
            {"role": "user", "content": f"Customer said: {customer_message}\n\nResolution: {resolution}\n\nDraft a professional reply."}
        ]
    )
    return response.content[0].text


# ============================================================
# CALL 7: Complex Escalation Analysis
# Task: Multi-step reasoning about whether to escalate — Tier 3 is justified
# Currently: Using Opus — THIS ONE IS CORRECT
# ============================================================
def analyze_escalation(ticket_history: str, customer_tier: str, sla_data: str) -> dict:
    response = client.messages.create(
        model="claude-opus-4-20250514",
        max_tokens=1000,
        system="""Analyze this escalation case. Consider:
1. Customer history and tier
2. SLA compliance status
3. Business impact
4. Whether previous resolutions were attempted
Provide a detailed recommendation with reasoning.""",
        messages=[
            {"role": "user", "content": f"Ticket History:\n{ticket_history}\n\nCustomer Tier: {customer_tier}\n\nSLA Data:\n{sla_data}"}
        ]
    )
    return response.content[0].text


# ============================================================
# MAIN — Process a sample ticket
# ============================================================
if __name__ == "__main__":
    email = "Dear customer, you have won a prize! Click here to claim your $1,000,000."

    # Wasteful pipeline: every call uses Opus
    is_spam = classify_spam(email)
    print(f"Spam: {is_spam}")

    if not is_spam:
        contact = extract_contact_info(email)
        sentiment = analyze_sentiment(email)
        department = route_ticket(email)
        summary = summarize_conversation(email)
        reply = draft_reply(email, "Marked as resolved")
        print(f"Contact: {contact}")
        print(f"Sentiment: {sentiment}")
        print(f"Routed to: {department}")
