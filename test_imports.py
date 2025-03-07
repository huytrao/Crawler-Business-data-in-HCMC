import logging
from fake_useragent import UserAgent
import schedule
# trafilature is a library for extracting content from web pages
import trafilatura
from bs4 import BeautifulSoup
from pymongo import MongoClient

# cinfigure logging
logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

def test_imports( ):
    """ Verify that all required packages are properly imported and functional."""
    try: 
        # Test MongoDB connection
        client = MongoClient('mongodb://localhost:27017/')
        db = client.test_db
        logger.info("MongoDB connection successful")

        # Test UserAgent
        ua = UserAgent(browsers = ['chrome', 'firefox']) 
        logger.info(f"UserAgent generated: {ua.random}")

        # Test BeautifulSoup 
        soup = BeautifulSoup("<html><p>Test</p></html>", "html.parser")
        logger.info(f"BeautifulSoup generated: {soup.get_text()}")

        # Test trafilature 
        test_html = "<html><body><article> Main content </article></body></html>"
        extracted = trafilatura.extract(test_html)
        logger.info(f"Tra filaturea working: {extracted}")

        # Test schedule 
        schedule.every(10).seconds.do(lambda: logger.info("Schedule working"))
        logger.info("Schedule working")

        logger.info("All imports vertified working successfully!")
        return True
    except Exception as e:
        logger.error(f"Import test failed: {e}")
        return False
    
if __name__ == '__main__':
    test_imports()
