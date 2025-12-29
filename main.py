import asyncio

from tools.logger import Logger
from tools.newsFetcher import fetch_news_urls, fetch_all_news
from tools.ContentSummarizer import ContentSummarizer
# from tools.ReportGenerator import ReportGenerator
from tools.writeReport import write_report
from tools.SummaryConsolidator import SummaryConsolidator

from pprint import pformat

def main():
    
    # inititate classes.
    logger = Logger(__name__).get_logger()
    summarizer = ContentSummarizer(logger=logger)
    consolidator = SummaryConsolidator(logger=logger)
    
    # url for daily gov press release webpage.
    while True:
        date = input("Enter the date in YYYYMMDD format (or type 'q' for quit):")
        if date.lower() == 'q':
            break
        
        daily_url = f"https://www.info.gov.hk/gia/general/{date[:6]}/{date[6:]}.htm"
        logger.info(f"Daily url: {daily_url}")
        
        # fetch all news per daily page.
        news_urls = fetch_news_urls(url=daily_url, logger=logger)
        results = asyncio.run(fetch_all_news(urls=news_urls))
        
        logger.info(f"Total news page scraped: {len(results)}")
        # record the results in logger.
        for result in results:
            logger.info(f"Metadata: \n%s", pformat(result[0].metadata))
            logger.info(f"Page content: \n%s", result[0].page_content)
            logger.info("-"*100)
        
        # summarize each news content.
        summarized_news = asyncio.run(summarizer.summarize_all_news_content(documents=results))
        logger.info(f"Total news page summarized: {len(summarized_news)}")
        
        # consolidate summaries into daily report.
        report_text = consolidator.consolidate_summary(summaries=summarized_news)
        logger.info(f"Consolidated Daily Press Release Report: \n%s", report_text)
        
        # write a report in text file.
        filename = write_report(
            url=daily_url,
            text=report_text
            )
        logger.info(f"FileName: {filename} - Daily Press Release Report generated.")
    
if __name__ == "__main__":
    main()
