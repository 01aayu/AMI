import asyncio

from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv

from config import BASE_URL, CSS_SELECTOR, REQUIRED_KEYS
from utils.data_utils import (
    save_venues_to_csv,
)
from utils.scraper_utils import (
    fetch_and_process_page,
    get_browser_config,
    get_llm_strategy,
)

load_dotenv()


async def crawl_venues(job_keyword: str):
    """
    Crawl job listings based on a user-specified keyword.
    """
    from urllib.parse import quote_plus

    # Encode keyword for URL
    encoded_keyword = quote_plus(job_keyword.strip())

    # Construct the base search URL for Quikr Jobs
    search_url = f"https://www.quikr.com/jobs/{encoded_keyword}+zwqxj1466534506"

    print(f"Searching jobs for: {job_keyword}")
    print(f"Search URL: {search_url}")

    # Initialize configurations
    browser_config = get_browser_config()
    llm_strategy = get_llm_strategy()
    session_id = "job_crawl_session"

    # Initialize state
    page_number = 1
    all_jobs = []
    seen_names = set()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        while True:
            jobs, no_results_found = await fetch_and_process_page(
                crawler,
                page_number,
                search_url,
                CSS_SELECTOR,
                llm_strategy,
                session_id,
                REQUIRED_KEYS,
                seen_names,
            )

            if no_results_found:
                print("No more jobs found. Ending crawl.")
                break

            if not jobs:
                print(f"No jobs extracted from page {page_number}.")
                break

            all_jobs.extend(jobs)
            page_number += 1
            await asyncio.sleep(2)

    if all_jobs:
        save_venues_to_csv(all_jobs, f"{job_keyword.replace(' ', '_')}_jobs.csv")
        print(f"Saved {len(all_jobs)} jobs to '{job_keyword}_jobs.csv'.")
    else:
        print("No jobs were found during the crawl.")

    llm_strategy.show_usage()


async def main():
    job_keyword = input("Enter job keyword (e.g., data entry, security guard): ")
    await crawl_venues(job_keyword)


if __name__ == "__main__":
    asyncio.run(main())
