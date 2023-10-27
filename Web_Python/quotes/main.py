from pprint import pprint
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://quotes.toscrape.com"


def get_urls(base_url: str):
    urls1 = ["/"]
    urls2 = ["/"]
    data_authors = []
    data_quotes = []
    
    while urls1:
        url = urls1.pop(0)
        response = requests.get(base_url + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data_authors.extend(get_authors(base_url, soup))
        
        tags = soup.select_one('nav ul.pager li.next a')
        
        if tags:
            link = tags['href']
            urls1.append(link)

            
    while urls2:
        url = urls2.pop(0)
        response = requests.get(base_url + url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.select_one('nav ul[class=pager] li[class=next] a')
        #link = tags['href']
        
        data_quotes.extend(get_quotes(base_url, soup))
    
        if tags:
            link = tags['href']
            urls2.append(link)
        else:
            print("You have reached the bottom.")
        
        
    return data_authors, data_quotes


def get_authors(base_url: str, soup):
    authors = []
    quote_elements = soup.select('div.quote')
    
    for element in quote_elements:
        author_element = element.select_one('span small.author')
        author_link = author_element.find_next('a')['href']
        
        author_data = get_author_data(base_url + author_link)
        if author_data:
            authors.append(author_data)

    return authors


def get_author_data(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    fullname = url.split('/')[-1].replace('-', ' ').strip()
    born_date_element = soup.select_one('div.author-details span.author-born-date')
    born_location_element = soup.select_one('div.author-details span.author-born-location')
    description_element = soup.select_one('div.author-details div')
    
    if fullname and born_date_element and born_location_element and description_element:
        born_date = born_date_element.text.strip()
        born_location = born_location_element.text.strip()[3:]
        description = description_element.text.strip()
        
        author_data = {
            'fullname': fullname,
            'born_date': born_date,
            'born_location': born_location,
            'description': description
        }
        
        return author_data
    
    return None


def get_quotes(base_url: str, soup):
    quotes = []
    quote_elements = soup.select('div.quote')
    
    for element in quote_elements:
        quote_text = element.select_one('span.text').text.strip()
        quote_author = element.select_one('small.author').text.strip()
        quote_tags = [el.text.strip() for el in element.select('div.tags a')]

        quotes_data = {
            'tags': quote_tags,
            'author': quote_author,
            'quote': quote_text
        }
        
        quotes.append(quotes_data)
        
    return quotes
    

if __name__ == '__main__':
    try:
        data_authors, data_quotes = get_urls(BASE_URL)
        
        with open('data_authors.json', 'w', encoding='utf-8') as file:
            json.dump(data_authors, file, indent=4, ensure_ascii=False)
        
        with open('data_quotes.json', 'w', encoding='utf-8') as file:
            json.dump(data_quotes, file, indent=4, ensure_ascii=False)
    
    except Exception as e:
        print(f"Error: {e}")
        
