# Skeptical News Article Analyzer

This program provides a critical, skeptical analysis of an online news article. It fetches the article's content and uses a Generative AI model to produce a structured report highlighting core claims, analyzing language, identifying potential red flags, and providing questions for further verification.

## How to Use

1.  **Clone this repository.**
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Get a Groq API Key:**
    * Sign up for a free account on the [Groq Console](https://console.groq.com/).
    * Navigate to the "API Keys" section and generate a new secret key.
4.  **Set the API Key as an Environment Variable:**
    This is the most secure way to use your key. Your script is configured to automatically read the key from the environment variable named `GROQ_API_KEY`.
    * **Windows:** Open Command Prompt and run:
        ```bash
        setx GROQ_API_KEY "YOUR_SECRET_KEY"
        ```
    * **macOS / Linux:** Open your terminal and run:
        ```bash
        export GROQ_API_KEY="YOUR_SECRET_KEY"
        ```
5.  **Run the script:**
    ```bash
    python skeptical_analyzer.py "[https://example-news-article.com/article-url](https://example-news-article.com/article-url)"
    ```
    Replace the URL with the link to the news article you want to analyze.

## Output

The program will generate a file named `critical_analysis_report.md` in the same directory. This file contains the complete report in Markdown format.

## Implementation Notes

**Web Content Handling:**
The program uses the `requests` and `BeautifulSoup4` libraries to fetch and parse the HTML content from the given URL. This approach is generally effective for a wide range of websites. However, if a website employs anti-scraping measures (e.g., Cloudflare protection, dynamic content loaded via JavaScript), the direct fetching method may fail.

**Generative AI Integration:**
The core of the analysis relies on a Generative AI model from Groq's API. The script uses the `groq` Python library to interact with their API.