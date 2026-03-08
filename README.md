# UAE Market Expansion Advisor (Agentic AI)

An Agentic AI system that helps a Jordanian restaurant specializing in meaty pizza and kebab sandwiches expand into the UAE market (Dubai & Abu Dhabi).
The system uses LLM reasoning + web tools to analyze competitors, menus, pricing, and market opportunities.

## Features
- Competitor discovery using Exa search

- Restaurant menu scraping and analysis

- Strategic recommendations for:

    - Locations

     - Pricing

     - Marketing

     - Delivery strategy

     - Operations

## Technologies Used
- Python

- Agno Agent Framework

- OpenAI API

- Exa Search API

- Playwright

- BeautifulSoup
  
- Regex text processing

## Project Structure

```
project/
│
├── main.py
├── agent.py
├── tools/
│   ├── competitor_finder.py
│   └── competitor_menu_tool.py
│
├── menu_scraper.py
├── text_cleaner.py
├── .env
└──requirements.txt
```

## Features

- AI-powered market entry strategy

- Competitor menu analysis

- Web scraping with Playwright

- HTML parsing with BeautifulSoup

- Token optimization before sending data to the AI model

- Market insights for Dubai and Abu Dhabi


## Setup Instructions

1. Clone the repository

   - git clone https://github.com/yourusername/uae-market-expansion-advisor.git

2. Navigate to the project

   - cd uae-market-expansion-advisor

3. Create virtual environment

   - python -m venv venv

4. Activate environment

   - Windows: venv\Scripts\activate
  
   - Mac/Linux: source venv/bin/activate
  

5. Install dependencies

   - pip install -r requirements.txt

6. Add API keys

   - Create a .env file:

   - OPENAI_API_KEY=your_key_here
   - EXA_API_KEY=your_key_here

7. Run the project

   - python agent.py


Watch the demo: https://drive.google.com/drive/u/0/folders/1QJUy7uv3h5Bf5VJwuriO1esIN_yMICQ2?sort=13&direction=a
