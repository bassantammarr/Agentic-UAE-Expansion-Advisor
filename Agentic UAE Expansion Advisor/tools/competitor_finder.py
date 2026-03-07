import os

from agno.tools import tool
from agno.tools.exa import ExaTools
from dotenv import load_dotenv
load_dotenv()

exa = ExaTools(num_results=3, api_key=os.getenv("EXA_API_KEY"))


@tool
def find_competitors(query: str) -> str:
   

    results = exa.search(query)

    return str(results)


