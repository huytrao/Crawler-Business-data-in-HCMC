import logging
from datetime import datetime, timedelta
from pymongo import MongoClient 
from pymongo.errors import PyMongoError

# Configure logging
logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name = "crawler_db") -> None:
        """ Initialize the database
        Args:
            db_name (str): Database name
        """
        self.db_name = db_name
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[self.db_name]
        self.collection = self.db['crawler_collection']
        self.init_db()

    def init_db(self):
        """ Initialize the database with requirement indexes"""
        try: 
            # create index on url field
            self.collection.create_index("url", unique = True)
            # create index on last_updated field for faster querying
            self.collection.create_index("timestamp")
            logger.info("Database initialized successfully")
            
        except PyMongoError as e:
            logger.error(f"Database initialization error: {e}")

    def save_data(self, url, content):
        """Save the data to the database
        Args:
            url (str): URL
            content (str): Content
        """
        try :
            document = {
                "url" : url,
                "content": content,
                "timestamp": datetime.now()
            }
            result = self.collection.update_one(
                {'url': url},
                {'$set': document},
                upsert = True
            )
            logger.info(f"Data saved successfully for URL: {url}, content length: {len(content)}")
        except PyMongoError as e:
            logger.error(f"Error saving data for URL:: {e}")

    def needs_update(self, url:str):
        """Check if the url needs to be updated older than 10 days
        Args:
            url (str): URL"""
        try:
            ten_days_ago = datetime.now() - timedelta(days= 10)
            result = self.collection.find_one({
                'url': url,
                'timestamp': {'$lt': ten_days_ago}
            })

            needs_update = result is None
            if result:
                logger.info(f"URL: {url}, Found recent record, {result['timestamp']}")
            else: 
                logger.info(f"URL: {url}, No recent record found")
                return needs_update
        # Handle the exception
        except PyMongoError as e:
            logger.error(f"Error checking update: {e}")
            return True

    
