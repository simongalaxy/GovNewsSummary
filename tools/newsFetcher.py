from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup, SoupStrainer
import requests
import re
import asyncio


def fetch_news_urls(url: str, logger) -> list[str]:
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
            logger.info(url)
            links.append(url)
    
    return links


async def fetch_news_content(url: str):
    bst_strainer = SoupStrainer("span", id=re.compile(r"^(PRHeadlineSpan|pressrelease)"))
    bst_loader = WebBaseLoader(
        web_path=(url),
        bs_kwargs={"parse_only": bst_strainer},
    )
    doc = bst_loader.load()
    splitted_content = doc[0].page_content.split("\n\t\t\t\t")
    doc[0].metadata["id"] = url.split("/")[-1].replace(".htm", "")
    doc[0].metadata["title"] = splitted_content[0].strip()
    doc[0].metadata["published_date"] = splitted_content[2].strip().split(", ")[1:]
    doc[0].metadata["published_time"] = splitted_content[4].strip().split(" ")[-1]
    
    return doc


async def fetch_all_news(urls: list[str]):
    tasks = [fetch_news_content(url=url) for url in urls]
    results = await asyncio.gather(*tasks)
 
    return results