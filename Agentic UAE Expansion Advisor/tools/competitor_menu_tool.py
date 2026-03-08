from agno.tools import tool
from menu_scraper import scrape_page, extract_menu_text
from text_cleaner import clean_text


@tool
def analyze_competitor_menu(url: str) -> str:
    
    html = scrape_page(url)

    raw_text = extract_menu_text(html)

    cleaned = clean_text(raw_text)

    return cleaned