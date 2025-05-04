import json
import os
from typing import List, Set, Tuple

from crawl4ai import (
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMExtractionStrategy,
)

from models.job import Job
from utils.data_utils import is_complete_job, is_duplicate_job


def get_browser_config() -> BrowserConfig:
    return BrowserConfig(
        browser_type="chromium",
        headless=False,
        verbose=True,
    )


def get_llm_strategy() -> LLMExtractionStrategy:
    return LLMExtractionStrategy(
        provider="groq/deepseek-r1-distill-llama-70b",
        api_token=os.getenv("GROQ_API_KEY"),
        schema=Job.model_json_schema(),
        extraction_type="schema",
        instruction=(
            "Extract all job objects with 'title', 'company', 'location', 'salary', "
            "'job_type', 'description', and 'posted_date' from the following content."
        ),
        input_format="markdown",
        verbose=True,
    )


async def check_no_results(
    crawler: AsyncWebCrawler,
    url: str,
    session_id: str,
) -> bool:
    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            session_id=session_id,
        ),
    )

    if result.success:
        return "No Results Found" in result.cleaned_html
    else:
        print(f"Error fetching page for 'No Results Found' check: {result.error_message}")
        return False


async def fetch_and_process_page(
    crawler: AsyncWebCrawler,
    page_number: int,
    base_url: str,
    css_selector: str,
    llm_strategy: LLMExtractionStrategy,
    session_id: str,
    required_keys: List[str],
    seen_titles: Set[str],
) -> Tuple[List[dict], bool]:
    url = f"{base_url}?page={page_number}"
    print(f"Loading page {page_number}...")

    if await check_no_results(crawler, url, session_id):
        return [], True

    result = await crawler.arun(
        url=url,
        config=CrawlerRunConfig(
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=llm_strategy,
            css_selector=css_selector,
            session_id=session_id,
        ),
    )

    if not (result.success and result.extracted_content):
        print(f"Error fetching page {page_number}: {result.error_message}")
        return [], False

    extracted_data = json.loads(result.extracted_content or "[]")
    if not extracted_data:
        print(f"No jobs found on page {page_number}.")
        return [], False

    print("Extracted data:", extracted_data)

    complete_jobs = []
    for job in extracted_data:
        print("Processing job:", job)

        if job.get("error") is False:
            job.pop("error", None)

        if not is_complete_job(job, required_keys):
            continue

        if is_duplicate_job(job["title"], seen_titles):
            print(f"Duplicate job '{job['title']}' found. Skipping.")
            continue

        seen_titles.add(job["title"])
        complete_jobs.append(job)

    if not complete_jobs:
        print(f"No complete jobs found on page {page_number}.")
        return [], False

    print(f"Extracted {len(complete_jobs)} jobs from page {page_number}.")
    return complete_jobs, False
