import logging 
from abc import ABC, abstractmethod # implementation in subclasses
from bs4 import BeautifulSoup
from utils import make_request_home
logger = logging.getLogger(__name__) 

# Abstract class for a pipeline
class Pipeline(ABC):
    @abstractmethod
    def process(self, data:str):
        """ Process the input data and return processed result."""
        pass


class HTMLExtractHerf(Pipeline):
    """ Extract href links from HTML data """
    
    def process(self, data: str) -> list:
        """Extract href links from HTML data
        Args:
            data (str): HTML data
            return: list of href links"""
        try:
            temp = make_request_home(data)
            soup = BeautifulSoup(temp, 'html.parser')
            search_results_divs = soup.find_all('div', class_='search-results')
            
            link_list = []
            # Iterate through each div with class 'search-results'
            for div in search_results_divs:
                # Get only the first link in each results div
                link = div.find('a')
                if link and link.get('href'):
                    link_list.append(link.get('href'))
            
            return link_list
        except Exception as e:
            logger.error(f"Error extracting href links: {e}")
            link_list = []
        return link_list

class HTMLCleanerPipeline(Pipeline):
    def process(self, data: str) -> str:
        """ Clean the HTML content and return the text data"""
        try:
            soup = BeautifulSoup(data, 'html.parser')
            # Extract base64 images only from the div with class 'jumbotron'
            base64_images = []

            # Extract the meta description content
            meta_description = soup.find('meta', attrs={'name': 'description'})['content']

            # Save the meta description to a JSON file
            # Extract MST and legal representative
            mst_tag = soup.find('a', href=True, string=lambda t: 'Mã số thuế:' in t)

            # Extract base64 images only from the div with class 'jumbotron'
            base64_images = []
            jumbotron_div = soup.find('div', class_='jumbotron')
            if jumbotron_div:
                for img_tag in jumbotron_div.find_all('img', src=True):
                    if img_tag['src'].startswith('data:image/png;base64,'):
                        base64_images.append(img_tag['src'])



            mst = mst_tag.find_next('a').text if mst_tag else None
            # Extract data only from the div with class 'jumbotron'
            jumbotron_div = soup.find('div', class_='jumbotron')


            # Extract legal representative if available
            legal_representative = None
            if jumbotron_div:
                legal_rep_tag = jumbotron_div.find(string=lambda t: 'Đại diện pháp luật:' in t)
                if legal_rep_tag:
                    legal_representative = legal_rep_tag.split(':')[1].strip()
                else:
                    legal_representative = None
                operating_status = jumbotron_div.find(string=lambda t: 'Trạng thái:' in t)
                if operating_status:
                    operating_status = operating_status.split(':')[1].strip()
                else:
                    operating_status = None
                type_of_activity = jumbotron_div.find(string=lambda t: 'Loại hình hoạt động:' in t)
                if type_of_activity:
                    type_of_activity = type_of_activity.split(':')[1].strip()
                else:
                    type_of_activity = None
                start_date = jumbotron_div.find(string=lambda t: 'Ngày cấp giấy phép:' in t)
                if start_date:
                    start_date = start_date.split(':')[1].strip()
                else:
                    start_date = None    
                address = jumbotron_div.find(string=lambda t: 'Địa chỉ:' in t)
                if address:
                    address = address.split(':')[1].strip()
                else:
                    address = None    
            data_to_save = {
                "description": meta_description,
                "legal_representative": legal_representative,
                "operating_status": operating_status,
                "type_of_activity": type_of_activity,
                'start_date': start_date,
                'address': address,

            }
            # Save the base64 images to data
            data_to_save['MST'] = base64_images[0] if len(base64_images) > 0 else None
            data_to_save['phone_number'] = base64_images[1] if len(base64_images) > 1 else None
            return data_to_save

        except Exception as e:
            logger.error(f"HTML cleaning error : {e}")
            return data


class PipelineManager:
    def __init__(self) -> None:
        self.pipeline = []
    
    def add_pipeline(self,pipeline : Pipeline )-> None:
        """ Add a processing pipeline"""
        # checking is instance of pipeline
        if isinstance(pipeline, Pipeline):
            self.pipeline.append(pipeline)

    # Add multiple pipelines
    def process_data(self, data:str) -> str:
        """ process data through all pipelines"""
        processed_data = data
        for pipeline in self.pipeline:
            try: 
                processed_data = pipeline.process(processed_data)
            except Exception as e:
                logger.error(f"Error processing data through pipeline: {e}")
        return processed_data
    def process_links(self, link_list: list) -> str:
        """Process each link through HTMLCleanerPipleline
        Args:
            link_list (list): List of links
            Return: list of cleaned processed for each links"""
        cleaned_data = []
        for link in link_list:
            logger.info(f"Processing link: {link}")
            temp_data = link
            for pipeline in self.pipeline:
                try:
                    temp_data = pipeline.process(temp_data)
                except Exception as e:
                    logger.error(f"Error processing data through pipeline: {e}")
            cleaned_data.append(temp_data)
        return cleaned_data

    def extract_and_clean(self, url: str) -> list:
        """Extract links and then clean each link
        Args:
            url (str): URL to extract links from
        Returns:
            list: List of cleaned data for each extracted link
        """
        # First pipeline should be HTMLExtractHerf
        extractor = next((p for p in self.pipeline if isinstance(p, HTMLExtractHerf)), None)
        # Second pipeline should be HTMLCleanerPipeline
        cleaner = next((p for p in self.pipeline if isinstance(p, HTMLCleanerPipeline)), None)
        
        if not extractor or not cleaner:
            logger.error("Required pipelines not found")
            return []
        
        try:
            # Extract links
            links = extractor.process(url)
            # save link to 1.txt
            logger.info(f"Extracted {len(links)} links from {url}")
            
            # Process each link through the cleaner
            cleaned_data = []
            for link in links:
                try:

                    html_content = make_request_home(link)
                    if html_content:
                        cleaned = cleaner.process(html_content)
                        cleaned_data.append(cleaned)
                        logger.error(f"Processed link Clean data: {link}")
                    else:
                        logger.error(f"Failed to fetch content for {link}")
                except Exception as e:
                    logger.error(f"Error processing link {link}: {e}")
            
            return cleaned_data
        except Exception as e:
            logger.error(f"Error in extract_and_clean: {e}")
            return []
