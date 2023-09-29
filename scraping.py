import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import htmltabletomd
import time

def scrape(url,old_content):
    try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            titles=soup('h2')
            if titles[0]==old_content:
                print('no new content')
                return 'no new content'
            contents = soup('p')
            paged_content={}
            for i in range(0, len(contents)-1):
                paged_content[titles[i].text]=contents[i].text
            return paged_content
    except:
        return 'url failed'
        
#for different page

def page_runner(o_data):
    
    url = 'https://www.legalraasta.com/blog/'
    data=[]
    pages = 5
    if len(o_data) ==0:
        for i in range(1,pages):
            url_pg = url+'page/'+str(i)+'/'
            content = scrape(url_pg,o_data)
            if content == 'url failed':
                print('url failed')
                break
            if content == 'no new content':
                print('no new content')
                break
            data.append(content)
        return data
    else:
        url_pg = url+'page/'+str(1)+'/'
        content = scrape(url_pg,o_data[0])
        if content == 'no new content':
            print('no new content')
            return o_data
        o_data.append(content)
        return o_data
data=[]
while True:
    print('Started Checking for new page')
    data = page_runner(data)
    print(data)
    time.sleep(10)
    
output_file = 'scraped_data.json'
with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)
