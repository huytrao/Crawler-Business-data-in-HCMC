# Crawler Business Data in HCMC

## Introduction

This project is designed to crawl and collect business data in Ho Chi Minh City (HCMC). The goal is to gather comprehensive information about various businesses, including their names, addresses, contact details, and other relevant data. This data can be used for market analysis, business development, and other purposes.

## Metrics

## What information I'm collection.

### Data Points Collected

For each business, we collect the following information:

1. **Description**: Full business name and brief description (e.g., "Công Ty TNHH Beauty Salon My Sel, Địa chỉ: 157B Phan Văn Trị, Phường 1...")
2. **Legal Representative**: Name of the person legally representing the business (e.g., "Nguyễn Khuyên Hải Xuyên")
3. **Operating Status**: Current status of the business (e.g., "Đang hoạt động" - Currently operating)
4. **Type of Activity/Business Entity**: Legal form of the business (e.g., "Công ty TNHH Một Thành Viên" - Single Member Limited Company)
5. **Start Date**: Official registration or establishment date (e.g., "07/03/2025")
6. **Address**: Complete business address including street, ward, district, and city (e.g., "157B Phan Văn Trị, Phường 14, Quận Bình Thạnh, Thành phố Hồ Chí Minh")
7. **MST (Tax Identification Number)**: Business tax ID (stored as encoded image data for security and validation purposes)
## Features

- Automated data collection from multiple sources
- Data cleaning and validation
- Storage of collected data in a structured format
- Easy-to-use interface for querying and retrieving data

## Technologies Used

- Python for scripting and automation
- BeautifulSoup and Scrapy for web scraping
- Pandas for data manipulation and cleaning
- SQLite for data storage

## Getting Started
### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/huytrao/hcmc-business-crawler.git
    cd hcmc-business-crawler
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

Create a `config.ini` file with your API keys and settings:
```ini
[api]
key=your_api_key_here

[settings]
delay=2
max_retries=3
```

### Running the Crawler

To start the crawler:
```bash
python src/main.py
```

The collected data will be saved in the `data` directory.
To get started with this project, clone the repository and follow the instructions in the setup guide.

## Contributing

We welcome contributions from the community. Please read our contributing guidelines before submitting a pull request.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact us at [traohuy098@gmail.com](mailto:traohuy098@gmail.com).

