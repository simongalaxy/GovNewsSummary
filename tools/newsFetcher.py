from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import asyncio

def fetch_news_urls(url: str) -> list[str]:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")
    pattern = re.compile(r"^P.*\.htm$")
    
    # filter the urls for news page.
    links = []
    for a in soup.find_all("a"):
        href = a.get("href")
        postFix = href.split("/")[-1]
        if pattern.match(postFix):
            url = f"https://www.info.gov.hk{href}"
            print(url)
            links.append(url)
    
    return links


async def fetch_news_content(url: str):
    bst_strainer = SoupStrainer("span", {"id": "pressrelease"})
    loader = WebBaseLoader(
        web_path=(url),
        bs_kwargs={"parse_only": bst_strainer},
    )
    
    return loader.load()


async def fetch_all_news(urls: list[str]):
    tasks = [fetch_news_content(url=url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    print(f"Total news page scraped: {len(results)}")
    # for result in results:
    #     print(result)
       
    return results