import os
import requests
from dotenv import load_dotenv
load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")

def google_linkedin_search(name):
    query = f"{name} site:linkedin.com/in"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.post(
        "https://google.serper.dev/search",
        headers=headers,
        json={"q": query}
    )
    if response.status_code == 200:
        results = response.json().get("organic", [])
        if results:
            snippet = results[0].get("snippet", "No useful info found.")
            link = results[0].get("link", "")
            return snippet, link
        else:
            return "No results found.", ""
    else:
        return f"Error: {response.status_code}", ""

def research_person(name):
    snippet, link = google_linkedin_search(name)
    return f"{name} appears to be associated with:\n{snippet}\nLinkedIn: {link}"
