# import serpapi

# params = {
#   "q": "who won the latest india vs pakistan match",
#   "api_key": "04fa6857fcb4b81450d7ae9ae86ff2d0d4dd50594e80304a11bee56174a42ef2"
# }

# search = serpapi.GoogleSearch(params)
# results = search.get_dict()
# ai_overview = results["ai_overview"]
# print(ai_overview)

from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field

# Initialize the FirecrawlApp with your API key
app = FirecrawlApp(api_key='fc-cffd0abdf63f46c0b029afd6d25c92bc')

class ExtractSchema(BaseModel):
    company_mission: str
    supports_sso: bool
    is_open_source: bool
    is_in_yc: bool

data = app.extract([
  'https://google.com/*'
  
], {
    'prompt': 'list the cricket matches of championship trophy 2025',
    'enableWebSearch': True
})
print(data)