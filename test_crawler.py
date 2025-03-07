import logging
from crawler import Crawler
from database import Database
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def verify_mongodb_data(db, urls):
    """Verify that data was properly saved to MongoDB."""
    try:
        # Check recent records (last hour)
        one_hour_ago = datetime.now() - timedelta(hours=1)
        for url in urls:
            result = db.collection.find_one({
                'url': url,
                'timestamp': {'$gt': one_hour_ago}
            })
            if result:
                logger.info(f"Found data for {url}:")
                logger.info(f"Content length: {len(result['content'])}")
                logger.info(f"Timestamp: {result['timestamp']}")
            else:
                logger.error(f"No recent data found for {url}")
    except Exception as e:
        logger.error(f"Error verifying MongoDB data: {e}")
def create_url_list():
    """Create a list of URLs to test."""
    urls = []
    for i in range (1, 2):
        urls.append(f"https://www.tratencongty.com/thanh-pho-ho-chi-minh/?page={i}")
    return urls

def test_multiple_urls():
    """Test crawler with multiple URLs.
    crawl the URLs and verify the data in MongoDB.
    for each URL, the crawler will fetch the content, process it, and save it to MongoDB.
    """
    urls = []
    urls = create_url_list()
    db = Database()
    crawler = Crawler(urls[0], db_instance=db, force_refresh=True)

    logger.info(f"Starting crawler test with {len(urls)} URLs")
    crawler.run(target_urls=urls)

    # Verify data in MongoDB
    logger.info("Verifying saved data in MongoDB")
    verify_mongodb_data(db, urls)

if __name__ == "__main__":
    test_multiple_urls()