import sys
import requests
from bs4 import BeautifulSoup
import os
from groq import Groq  # Import the Groq library

# Initialize the Groq client
# The API key will be automatically loaded from the GROQ_API_KEY environment variable
client = Groq(api_key='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')


def fetch_article_content(url):
    """
    Fetches and extracts the main text content from a given URL.
    Returns the title and the main text as a single string.
    """
    try:
        # Define a user-agent to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Heuristics to find the main article content.
        article_body = soup.find('body')
        paragraphs = article_body.find_all('p') if article_body else []
        article_text = ' '.join([p.get_text() for p in paragraphs])

        title = soup.find('title').get_text() if soup.find('title') else "Untitled Article"

        return title, article_text

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return "Untitled Article", ""


def get_ai_response(prompt):
    """
    Sends a prompt to the Groq API and returns the response.
    """
    try:
        chat_completion = client.chat.completions.create(
            # Using a fast and capable model from Groq's free tier
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a critical, unbiased news analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error interacting with the AI model: {e}")
        return "Analysis could not be performed."


def get_skeptical_analysis(article_text, article_title):
    """
    Uses Generative AI to perform a skeptical analysis of the article text.
    Returns a dictionary with the analysis results for each section.
    """
    # Prompt for Core Claims
    claims_prompt = f"""
    Based on the following news article, extract 3-5 of the main factual claims. Do not include opinions or commentary, only objective claims. Format the response as a simple bulleted list.

    Article Title: {article_title}
    Article Text:
    ---
    {article_text}
    ---
    """
    core_claims = get_ai_response(claims_prompt)

    # Prompt for Language & Tone
    tone_prompt = f"""
    Analyze the language and tone of the following news article. Classify the language as "neutral and factual," "emotionally charged and persuasive," or "a strong opinion piece." Provide a brief, concise explanation of your classification, citing specific words or phrases as examples if possible.

    Article Text:
    ---
    {article_text}
    ---
    """
    language_analysis = get_ai_response(tone_prompt)

    # Prompt for Potential Red Flags
    red_flags_prompt = f"""
    Read the following news article and identify any potential red flags that may indicate bias or poor reporting. These could include:
    - Over-reliance on anonymous or a single source.
    - Lack of cited data or sources for key claims.
    - Use of loaded or emotionally charged terminology.
    - Dismissing opposing viewpoints without exploration.
    - Use of sensational headlines.

    List your findings as a bulleted list. If no red flags are found, state "No obvious red flags were detected."

    Article Text:
    ---
    {article_text}
    ---
    """
    red_flags = get_ai_response(red_flags_prompt)

    # Prompt for Verification Questions
    questions_prompt = f"""
    Based on the following news article, generate 3-4 specific, insightful questions that a reader should ask to independently verify the content. The questions should challenge the claims and encourage further research.

    Article Text:
    ---
    {article_text}
    ---
    """
    verification_questions = get_ai_response(questions_prompt)

    return {
        "claims": core_claims,
        "language_analysis": language_analysis,
        "red_flags": red_flags,
        "questions": verification_questions
    }


def generate_report(article_title, analysis_data):
    """
    Generates a markdown-formatted report from the analysis data.
    """
    report = f"# Critical Analysis Report for: {article_title}\n\n"

    report += "### Core Claims\n"
    report += analysis_data["claims"] + "\n\n"

    report += "### Language & Tone Analysis\n"
    report += analysis_data["language_analysis"] + "\n\n"

    report += "### Potential Red Flags\n"
    report += analysis_data["red_flags"] + "\n\n"

    report += "### Verification Questions\n"
    report += analysis_data["questions"]

    return report


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python skeptical_analyzer.py <URL_or_file_path>")
        sys.exit(1)

    input_source = sys.argv[1]

    if input_source.startswith("http"):
        print(f"Fetching content from URL: {input_source}...")
        article_title, article_content = fetch_article_content(input_source)
    else:
        print(f"Reading content from local file: {input_source}...")
        try:
            with open(input_source, 'r', encoding='utf-8') as f:
                article_content = f.read()
            article_title = os.path.basename(input_source).replace('.txt', '')
        except FileNotFoundError:
            print(f"Error: The file at {input_source} was not found.")
            sys.exit(1)

    if not article_content:
        print("Could not retrieve article content. Exiting.")
        sys.exit(1)

    print("Performing skeptical analysis...")
    analysis_results = get_skeptical_analysis(article_content, article_title)

    final_report = generate_report(article_title, analysis_results)

    with open("critical_analysis_report.md", "w", encoding='utf-8') as f:
        f.write(final_report)

    print("\nAnalysis complete! Report saved to 'critical_analysis_report.md'")