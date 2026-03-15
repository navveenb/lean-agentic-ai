"""
Sample App: Content Pipeline
Another deliberately wasteful file — uses GPT-4 for everything.
"""

from openai import OpenAI

client = OpenAI()


# ============================================================
# CALL 1: Categorize article
# Task: Classification — should be Tier 1 (GPT-4o-mini)
# Currently: Using GPT-4 for simple category assignment
# ============================================================
def categorize_article(title: str, body: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=20,
        messages=[
            {"role": "system", "content": "Categorize this article. Reply with one of: TECH, BUSINESS, SPORTS, ENTERTAINMENT, SCIENCE."},
            {"role": "user", "content": f"Title: {title}\n\nBody: {body[:500]}"}
        ]
    )
    return response.choices[0].message.content.strip()


# ============================================================
# CALL 2: Generate SEO tags
# Task: Extraction — should be Tier 1 (GPT-4o-mini)
# Currently: Using GPT-4 for tag extraction
# ============================================================
def generate_seo_tags(article_text: str) -> list:
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=100,
        messages=[
            {"role": "system", "content": "Generate 5 SEO tags for this article. Return as comma-separated list."},
            {"role": "user", "content": article_text[:1000]}
        ]
    )
    return response.choices[0].message.content.strip().split(",")


# ============================================================
# CALL 3: Translate headline
# Task: Translation — should be Tier 2 (GPT-4o)
# Currently: Using GPT-4 for simple translation
# ============================================================
def translate_headline(headline: str, target_lang: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=100,
        messages=[
            {"role": "user", "content": f"Translate this headline to {target_lang}: {headline}"}
        ]
    )
    return response.choices[0].message.content.strip()


# ============================================================
# CALL 4: Format JSON output
# Task: Formatting — should be Tier 1 or even NO LLM (use code)
# Currently: Using GPT-4 to format data that could be done with Python
# ============================================================
def format_article_json(title, category, tags, summary):
    response = client.chat.completions.create(
        model="gpt-4",
        max_tokens=300,
        messages=[
            {"role": "user", "content": f"""Format this as JSON:
Title: {title}
Category: {category}
Tags: {tags}
Summary: {summary}

Return valid JSON only."""}
        ]
    )
    return response.choices[0].message.content
