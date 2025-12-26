import asyncio

from tools.newsFetcher import fetch_news_urls, fetch_all_news
from tools.ContentSummarizer import ContentSummarizer


def main():
    daily_url = "https://www.info.gov.hk/gia/general/202512/02.htm"
    # pressRelease_url = "https://www.info.gov.hk/gia/general/202512/02/P2025120200791.htm"
    
    # fetch all news per daily page.
    news_urls = fetch_news_urls(url=daily_url)
    results = asyncio.run(fetch_all_news(urls=news_urls))
    
    # summarize each news content.
    summarizer = ContentSummarizer()
    summarized_news = asyncio.run(summarizer.summarize_all_news_content(documents=results))
    
    
    
    
if __name__ == "__main__":
    main()
