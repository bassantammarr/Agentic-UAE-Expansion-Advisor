## Project Overview

This project implements an agentic AI advisor that helps a Jordanian restaurant plan expansion into the UAE market.

The system focuses on strategic recommendations for opening branches in Dubai and Abu Dhabi. It provides guidance on locations, competitors, menu adaptation, pricing strategy, and marketing.

The advisor is implemented using the Agno framework and is accessible through a command-line chatbot interface.


## Architecture Overview

The system follows an Agent + Tools architecture using the Agno framework.

### Components:
1. Agent
   - The core agent interprets user questions and generates strategic recommendations using an OpenAI language model.

2. Tools
   - The agent can call external tools when additional information is required.

### Tools included in the system:
1. Competitor Finder  
    - Uses Exa search to identify restaurant competitors in Dubai and Abu Dhabi.

2. Competitor Menu Analyzer  
    - Scrapes restaurant websites using Playwright and BeautifulSoup to extract menu text.

3. Flow
   
    User Question  
        ↓  
    Agent reasoning  
        ↓  
    Optional tool usage  
        ↓  
    Structured recommendation

## Technologies Used

- Python
- Agno framework
- OpenAI API
- Exa Search API
- Playwright (web scraping)
- BeautifulSoup (HTML parsing)


## Setup Instructions

1. Clone the repository

   - git clone https://github.com/bassantammarr/uae-market-expansion-advisor.git

2. Navigate to the project

   - cd uae-market-expansion-advisor

3. Create virtual environment

   - python -m venv venv

4. Activate environment

   - Windows:venv\Scripts\activate


   - Mac/Linux:source venv/bin/activate

5. Install dependencies

   - pip install -r requirements.txt

6. Add API keys

   - Create a `.env` file:

   - OPENAI_API_KEY=your_key_here  
   - EXA_API_KEY=your_key_here  

7. Run the project

   - python agent.py


## How the System Works

The system runs as a command-line chatbot.

Users can ask strategic questions about expanding a Jordanian restaurant into Dubai or Abu Dhabi.

The agent processes the question and generates a structured response. When necessary, it may call external tools to retrieve competitor or menu information.

Responses are formatted using clear headings and bullet points to make them useful for business decision-making.

## Key Design Decisions

### CLI Interface
A command-line interface was chosen because it allows rapid prototyping and testing without requiring additional frontend development. This makes it easier to demonstrate the advisor’s capabilities during evaluation.

Agno Framework
Agno was selected because it simplifies building agentic systems with tool integration.

Structured Prompt Design
The system prompt was carefully designed to guide the agent to produce executive-style responses with actionable recommendations.

Tool Integration
Search and scraping tools were added to allow the agent to access real-world competitor information when necessary.

## API Cost Control

Several strategies were used to reduce API usage:

- Used the `gpt-4.1-mini` model for lower cost.
- Limited responses to under 500 words.
- Set `max_tokens` to 800.
- Restricted search results to a small number.
- Tools are only used when additional information is required.

## Evaluation / Testing

Example Questions Tested

1. What are the best locations to open our first branch in Dubai?
2. Who are the main competitors for kebab restaurants in Dubai?
3. What customer segments should we target?
4. How should we adapt our menu for UAE customers?
5. What price range should our meals target?
6. What marketing strategy should we use for launch?
7. What delivery platforms should we prioritize?
8. What are the risks of expanding into the UAE market?
9. Should we focus on dine-in or delivery first?
10. How should we expand after the first branch?

What Worked Well
- Clear structured recommendations
- Good strategic insights
- Tool usage for competitor discovery

Limitations Observed
- Competitor results depend on search availability
- Some websites cannot be scraped

## Limitations

- The system relies on general market knowledge rather than real financial datasets.
- Competitor information depends on search results.
- Menu scraping may fail for certain websites.

Future Improvements

- Add structured restaurant datasets
- Add location scoring models
- Improve competitor analysis
- Add user friendly UI "working on it right now"

## AI Tool Usage Disclosure

AI tools were used during development for guidance and code review.

Tools Used:
- ChatGPT

How AI was used: 
- refining system prompts to improve cost efficiency while maintaining response quality
- assisting with documentation writing  

Although AI tools were used for assistance during development, the main system components were implemented by the developer, including the agent architecture, tool integrations, scraping pipeline, prompt design, and API cost control.

## Conclusion

This project demonstrates how an agentic AI system can assist with strategic business decisions such as international market expansion. By combining a language model with external tools for search and scraping, the advisor can provide structured, actionable insights for restaurant executives considering expansion into the UAE market.
