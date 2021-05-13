import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json


reviewlist = []

def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.replace('Amazon.co.uk:Customer reviews:', '').strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        print("Unsucessfully get reviews")
        pass

urlList = []
with open('ProductList.txt') as my_file:
    for line in my_file:
        urlList.append(line)

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

for url in urlList:
    r = requests.get(url, headers=HEADERS)
    print(r.status_code)
    print(r)
    print(r.text)
    soup = BeautifulSoup(r.text, "lxml")
    get_reviews(soup)
    time.sleep(10)

df = pd.DataFrame(reviewlist)
df.to_excel('ReviewInExcel.xlsx', index=False)
df.to_csv (r'ReviewC.csv', index = False, header=True)
with open('ReviewsJ.json', 'w') as outfile:
    json.dump(reviewlist, outfile)
print('Finished')









