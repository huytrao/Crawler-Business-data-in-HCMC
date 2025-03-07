import requests
import logging
from time import sleep
from utils import get_random_user_agent, random_delay, validate_url
from pipeline import PipelineManager, HTMLCleanerPipeline, HTMLExtractHerf
from database import Database

logger = logging.getLogger(__name__)

class Crawler:
    """
    Web crawler class.
    Attributes:
        base_url (str): Base URL to start crawling
        db_instance (Database): Database instance
        force_refresh (bool): Force refresh of data
        max_retries (int): Maximum number of retries for HTTP requests
        """
    def __init__(self, base_url, db_instance=None, force_refresh=False, max_retries=3):
        self.base_url = base_url
        self.db = db_instance or Database()
        self.pipeline_manager = PipelineManager()
        self.force_refresh = force_refresh
        self.max_retries = max_retries
        self.setup_pipeline()

    def setup_pipeline(self) -> None:
        """Setup default processing pipeline."""
        self.pipeline_manager.add_pipeline(HTMLExtractHerf())
        self.pipeline_manager.add_pipeline(HTMLCleanerPipeline())


    def make_request(self, url, retry_count=0)-> str:
        """Make HTTP request with retry mechanism.
        args: url (str): URL to fetch
        retry_count (int): Current retry count
        return: str: Response content"""
        if not validate_url(url):
            raise ValueError(f"Invalid URL: {url}")

        headers = {'User-Agent': get_random_user_agent()}
        try:
            delay = random_delay()
            logger.info(f"Waiting {delay:.2f} seconds before requesting {url}")

            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            logger.info(f"Successfully fetched {url} (status: {response.status_code})")
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            if retry_count < self.max_retries:
                wait_time = (retry_count + 1) * 5  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds (attempt {retry_count + 1}/{self.max_retries})")
                sleep(wait_time)
                return self.make_request(url, retry_count + 1)
            return None

    def process_page(self, url) -> None:
        """Process a single page.
        args: url (str): URL to process
        return: None"""
        try:
            logger.info(f"Processing URL: {url} (force_refresh: {self.force_refresh})")

            if not self.force_refresh:
                needs_update = self.db.needs_update(url)
                logger.info(f"URL {url} needs update: {needs_update}")
                if not needs_update:
                    logger.info(f"Skip URL {url} - recent data exists")
                    return

            content = self.make_request(url)
            if content:
                processed_data = self.pipeline_manager.extract_and_clean(url)

                if processed_data:
                    print(processed_data)
                    self.db.save_data(url, processed_data)
                
                logger.info(f"Content fetched successfully for {url} , length: {len(content)}")
            else:
                logger.error(f"Failed to fetch content for {url} after all retries")
        except Exception as e:
            logger.error(f"Error processing {url}: {e}")

    def run(self, target_urls=None) -> None:
        """Main crawler execution.
        args: target_urls (list): List of URLs to crawl
        return: None
        """
        try:
            urls_to_crawl = target_urls if target_urls else [self.base_url]
            logger.info(f"Starting crawler with {len(urls_to_crawl)} URLs")
            for url in urls_to_crawl:
                self.process_page(url)
                logger.info(f"Completed processing {url}")
        except Exception as e:
            logger.error(f"Crawler execution error: {e}")