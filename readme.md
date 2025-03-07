# Crawler Business Data in HCMC

## Introduction

This project is designed to crawl and collect business data in Ho Chi Minh City (HCMC). The crawler extracts detailed business information from web sources like tratencongty.com, processes the data through a pipeline system, and stores it in MongoDB for further analysis.

## Data Points Collected
![Untitled Diagram drawio](https://github.com/user-attachments/assets/652408e0-1265-433d-b323-4a0202aa6d5f)

For each business, we collect the following information:

1. **Description**: Full business name and brief description
2. **Legal Representative**: Name of the person legally representing the business
3. **Operating Status**: Current status of the business (e.g., "Đang hoạt động")
4. **Type of Activity/Business Entity**: Legal form of the business (e.g., "Công ty TNHH")
5. **Start Date**: Official registration or establishment date
6. **Address**: Complete business address including street, ward, district, and city
7. **MST (Tax Identification Number)**: Business tax ID (stored as base64 encoded image)
8. **Phone Number**: Business contact number (stored as base64 encoded image)

## Features

- Automated data collection from business registry websites
- Data cleaning and extraction via customizable pipeline system
- MongoDB storage with automatic update management
- Configurable crawling with random delays and rotating user-agents
- Robust error handling and retry mechanism

## Architecture

The project consists of several components:

- **Crawler**: Manages HTTP requests and coordinates the crawling process
- **Pipeline**: Processes HTML data through extraction and cleaning stages
- **Database**: Handles MongoDB operations and data persistence
- **Utils**: Provides utility functions for HTTP requests, user agents, etc.

## Technologies Used

- Python 3.11+
- BeautifulSoup4 for HTML parsing
- MongoDB for data storage
- Requests library for HTTP requests
- Fake-UserAgent for rotating browser identification

## Getting Started

### Prerequisites
- Python 3.11 or higher
- MongoDB server running locally or remotely
- pip package manager
- Git

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/huytrao/Crawler-Business-data-in-HCMC.git
    cd Crawler-Business-data-in-HCMC
    ```

2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The crawler can be configured through parameters in the Crawler class:

```python
crawler = Crawler(
    force_refresh=False,  # Set to True to ignore cached data
    max_retries=3         # Maximum retry attempts for failed requests
)
```

### Running the Crawler

To test the crawler:
```bash
git clone https://github.com/huytrao/Crawler-Business-data-in-HCMC.git
cd Crawler-Business-data-in-HCMC
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
 install package
```bash
pip install poetry
poetry install
```

```bash
python test_imports.py  
python test_crawler.py
```


## Contributing

We welcome contributions from the community. Please feel free to submit pull requests or open issues.

## Contact

For any questions or inquiries, please contact us at [traohuy098@gmail.com](mailto:traohuy098@gmail.com).
