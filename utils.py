# utils.py provide utily functions random user agents, introducing random delays, and validating URLS.
import random
import time
from fake_useragent import UserAgent
import logging
import requests
from time import sleep
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_random_user_agent():
    """Generate a random user agent string."""
    try:
        ua = UserAgent(browsers=['chrome', 'firefox', 'safari'])
        return ua.random
    except Exception as e:
        logger.error(f"Error generating user agent: {e}")
        # Fallback user agent
        fallback_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
        ]
        return random.choice(fallback_agents)

def random_delay(min_delay=0.1, max_delay=3):
    """Implement random delay between requests."""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
    return delay

def validate_url(url):
    """Basic URL validation."""
    return url.startswith(('http://', 'https://'))

def make_request_home(url, retry_count=0, max_retries=20) -> str:
    """
    Make request to get home page HTML.
    Args:
        url (str): URL to fetch
        retry_count (int): Current retry count
        max_retries (int): Maximum number of retries
    Returns:
        str: Response content
    """
    if retry_count >= max_retries:
        return None

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
        wait_time = (retry_count + 1) * 5  # Exponential backoff
        logger.info(f"Retrying in {wait_time} seconds (attempt {retry_count + 1}/{max_retries})")
        sleep(wait_time)
        return make_request_home(url, retry_count + 1, max_retries)