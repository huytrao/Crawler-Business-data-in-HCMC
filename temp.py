# import requests
# from utils import make_request_home
# from bs4 import BeautifulSoup
# import json

# """
# Extract href link from HTML data
# Args:
#     data (str): HTML data
#     return: list of href links
# """

# temp = make_request_home("https://www.tratencongty.com/company/74d19e3b-cong-an-xa-hong-tien/")

# soup = BeautifulSoup(temp, 'html.parser')
# # find all links inside <ul class = "list-link"
# search_results_div = soup.find('div', class_='search-results')
# # Extract base64 images only from the div with class 'jumbotron'
# base64_images = []

# # Extract the meta description content
# meta_description = soup.find('meta', attrs={'name': 'description'})['content']

# # Extract the canonical link
# canonical_link = soup.find('link', rel='canonical')['href']

# # Save the meta description to a JSON file
# # Extract MST and legal representative
# mst_tag = soup.find('a', href=True, string=lambda t: 'Mã số thuế:' in t)

# # Extract base64 images only from the div with class 'jumbotron'
# base64_images = []
# jumbotron_div = soup.find('div', class_='jumbotron')
# if jumbotron_div:
#     for img_tag in jumbotron_div.find_all('img', src=True):
#         if img_tag['src'].startswith('data:image/png;base64,'):
#             base64_images.append(img_tag['src'])



# mst = mst_tag.find_next('a').text if mst_tag else None
# # Extract data only from the div with class 'jumbotron'
# jumbotron_div = soup.find('div', class_='jumbotron')


# # Extract legal representative if available
# legal_representative = None
# if jumbotron_div:
#     legal_rep_tag = jumbotron_div.find(string=lambda t: 'Đại diện pháp luật:' in t)
#     if legal_rep_tag:
#         legal_representative = legal_rep_tag.split(':')[1].strip()
#     else:
#         legal_representative = None
#     operating_status = jumbotron_div.find(string=lambda t: 'Trạng thái:' in t)
#     if operating_status:
#         operating_status = operating_status.split(':')[1].strip()
#     else:
#         operating_status = None
#     type_of_activity = jumbotron_div.find(string=lambda t: 'Loại hình hoạt động:' in t)
#     if type_of_activity:
#         type_of_activity = type_of_activity.split(':')[1].strip()
#     else:
#         type_of_activity = None
#     start_date = jumbotron_div.find(string=lambda t: 'Ngày cấp giấy phép:' in t)
#     if start_date:
#         start_date = start_date.split(':')[1].strip()
#     else:
#         start_date = None    
#     address = jumbotron_div.find(string=lambda t: 'Địa chỉ:' in t)
#     if address:
#         address = address.split(':')[1].strip()
#     else:
#         address = None    
# data_to_save = {
#     "description": meta_description,
#     "legal_representative": legal_representative,
#     "operating_status": operating_status,
#     "type_of_activity": type_of_activity,
#     'start_date': start_date,
#     'address': address,

# }
# # Save the base64 images to data
# data_to_save['MST'] = base64_images[0] if len(base64_images) > 0 else None
# data_to_save['phone_number'] = base64_images[1] if len(base64_images) > 1 else None



# print(data_to_save)
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.crawler_db
collection = db.crawler_collection

for document in collection.find():
    print(document)