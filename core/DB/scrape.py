import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

class SearchTool:
    def extract_url(self, full_link):
        # Use regex to extract the part between 'url=' and '&ved'
        match = re.search(r'url=(https?://[^&]+)&ved=', full_link)
        if match:
            return match.group(1)  # Return the URL part
        return None

    def google_search(self, query, num_results=2):
        query = urllib.parse.quote_plus(query)  # Converts the query to a URL-encoded format
        url = f"https://www.google.com/search?q={query}&num={num_results}"
        self.url=url
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        # Send request to Google search
        response = requests.get(url, headers=headers)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all the link elements in the search results
        links = []
        for item in soup.find_all("a", href=True):
            href = item['href']
            link=self.extract_url(href)
            if link:
                links.append(link)
        # Return only the top 'num_results' links
        return links[:num_results]

    def get_page_content(self, links):
        pages_content = []
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        for link in links:
            try:
                response = requests.get(link, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # paragraphs=''
                    for p in soup.find_all('p'):
                        pages_content.append(p.get_text())

                    # pages_content.append(paragraphs)

            except requests.exceptions.RequestException as e:
                # print(f"Failed to retrieve {link}: {e}")
                pass
        return pages_content
    
    def search(self, query, num_results=3):
        responses=[]

        for el in query:
            top_links = self.google_search(el, num_results)
            # print(top_links)
            top_links+=self.url
            page_contents = self.get_page_content(top_links)
            # print(page_contents)
            responses+=page_contents
        
        return responses

# Example usage

# qs=['1. "Google stock price today"', '2. "Current Google stock price"', '3. "Google stock market watch"', '4. "Alphabet Inc. stock price"', '5. "Google investor relations"']
search_query = "us elections presidential candidat3es"
searchtool=SearchTool()
# temp=searchtool.search(qs)
# print(temp)
# print(len(temp), len(temp[0]))