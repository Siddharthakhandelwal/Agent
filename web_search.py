import re
import requests

# Fire Crawl API configuration (replace with your actual API key)
FIRE_CRAWL_API_KEY = "fc-cffd0abdf63f46c0b029afd6d25c92bc"
FIRE_CRAWL_ENDPOINT = "https://api.firecrawl.dev/v1/search"

def needs_web_search(query):
    """Determine if a query requires web search
    
    This function detects if a query likely needs current information from the internet
    by looking for specific keywords or patterns.
    """
    search_indicators = [
        "search", "find", "lookup", "recent", "latest", "current", "news",
        "today", "yesterday", "this week", "this month", "this year",
        "update", "information about", "data on", "research", "download",
        "what is", "who is", "where is", "when did", "how to"
    ]
    
    query_lower = query.lower()
    
    # Check for time-sensitive words
    time_indicators = ["current", "latest", "recent", "today", "now", "update"]
    has_time_indicator = any(indicator in query_lower for indicator in time_indicators)
    
    # Check for question words
    question_indicators = ["what", "who", "where", "when", "why", "how"]
    has_question = any(indicator in query_lower for indicator in question_indicators)
    
    # Check for search-related words
    has_search_word = any(indicator in query_lower for indicator in search_indicators)
    
    # Check for specific terms that suggest factual information is needed
    fact_seeking = re.search(r"(^|\s)(find|get|download|search for)(\s|$)", query_lower) is not None
    
    return has_time_indicator or (has_question and has_search_word) or fact_seeking

def search_web(query, num_results=5):
    """Search the web using Fire Crawl API"""
    headers = {
        "Authorization": f"Bearer {FIRE_CRAWL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": query,
        "num_results": num_results,
        "include_domains": [],  # Optional: specific domains to include
        "exclude_domains": [],  # Optional: specific domains to exclude
        "time_period": "month"  # Options: day, week, month, year, all
    }
    
    try:
        response = requests.post(FIRE_CRAWL_ENDPOINT, headers=headers, json=data)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def extract_file_links(search_results):
    """Extract links to downloadable files from search results"""
    file_extensions = [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", 
        ".txt", ".csv", ".zip", ".rar", ".7z", ".tar", ".gz"
    ]
    
    file_links = []
    
    # Check each search result for links
    for result in search_results.get("results", []):
        # Check main URL
        url = result.get("url", "")
        if any(url.lower().endswith(ext) for ext in file_extensions):
            file_links.append({
                "url": url,
                "title": result.get("title", "Unknown"),
                "type": url.split(".")[-1].upper()
            })
        
        # Check content for links
        content = result.get("content", "")
        link_matches = re.finditer(r'href=[\'"]?([^\'" >]+)', content)
        for match in link_matches:
            link_url = match.group(1)
            if any(link_url.lower().endswith(ext) for ext in file_extensions):
                file_links.append({
                    "url": link_url if link_url.startswith(("http://", "https://")) else f"{result.get('domain', '')}{link_url}",
                    "title": f"File from {result.get('title', 'Unknown')}",
                    "type": link_url.split(".")[-1].upper()
                })
    
    return file_links

def extract_answer_from_search(search_results, query):
    """Extract and compile a comprehensive answer from search results"""
    if "error" in search_results:
        return f"Error while searching: {search_results['error']}"
    
    if not search_results.get("results"):
        return "No relevant information found online for your query."
    
    # Compile relevant snippets and information
    compiled_info = "Here's what I found online about your query:\n\n"
    
    for i, result in enumerate(search_results.get("results", [])[:5]):
        title = result.get("title", "Untitled")
        url = result.get("url", "")
        snippet = result.get("snippet", result.get("content", ""))[:300] + "..."
        
        compiled_info += f"{i+1}. **{title}**\n"
        compiled_info += f"   {snippet}\n"
        compiled_info += f"   Source: {url}\n\n"
    
    # Extract file links if any
    file_links = extract_file_links(search_results)
    if file_links:
        compiled_info += "I also found these relevant files:\n\n"
        for i, file in enumerate(file_links[:3]):  # Limit to 3 files
            compiled_info += f"- [{file['title']} ({file['type']})]({file['url']})\n"
    
    return compiled_info