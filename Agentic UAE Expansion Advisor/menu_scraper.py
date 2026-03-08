from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def scrape_page(url: str) -> str:

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page()

        page.goto(url, timeout=60000)

        page.wait_for_timeout(4000)

        html = page.content()

        browser.close()

    return html


def extract_menu_text(html: str) -> str:

    soup = BeautifulSoup(html, "lxml")

    for tag in soup(["script", "style", "noscript"]):
        tag.extract()

    text = soup.get_text(separator="\n")

    return text




