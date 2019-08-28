from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
from urllib.request import Request
from urllib.request import urlopen

def get_html(url):
    
    html_content = ''
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #hdr)
        html_page = urlopen(req).read()
        html_content = BeautifulSoup(html_page, "html.parser")
    except: 
        pass
        
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price_temp = html.select('.PriceUser p')[2].get_text().strip()
        price_temp = price_temp.replace('Outside New ZealandNZ$', '').replace(',', '').strip()
        price_parts = price_temp.split('(')
        price = price_parts[0].strip()
        stamp['price'] = price
    except: 
        stamp['price'] = None

    try:
        title = html.select('.DetailTitle')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
        
    try:
        sku = html.select('.invNumberDetail')[0].get_text().strip()
        stamp['sku'] = sku.replace('Item #:', '').strip()
    except:
        stamp['sku'] = None    
        
    try:
        condition = html.select('.LabelText')[0].get_text().strip()
        stamp['condition'] = condition.replace('Condition', '').strip()
    except:
        stamp['condition'] = None 
        
    category = ''   
    try:
        category_items = html.select('.BreadCrumb a')
        for category_item in category_items:
            category_item_text = category_item.get_text().strip()
            if 'Home' not in category_item_text:
                if category:
                    category = category + ' > '
                category = category + category_item_text  
            
        stamp['category'] = category
    except:
        stamp['category'] = None   
        
    stamp['currency'] = "NZD"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('form td td img')
        for image_item in image_items:
            img_src = image_item.get('src')
            img = 'https://www.classicstamps.co.nz/' + img_src
            if img not in images and '.gif' not in img_src:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    try:
        raw_text = html.select('.ProductDetails')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('td a.head2'):
            item_link = 'https://www.classicstamps.co.nz' + item.get('href').replace('&amp;', '&').strip()
            if item_link not in items:
                items.append(item_link)
    except:
        pass

    try:
        next_items = html.select('a.NavBar')
        for next_item in next_items:
            next_item_text = next_item.get_text().strip()
            if 'Next' in next_item_text:
                next_url = 'https://www.classicstamps.co.nz' + next_item.get('href')
                break
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories(category_url):
    
    items = []

    try:
        html = get_html(category_url)
    except:
        return items
 
    try:
        for item in html.select('td a'):
            item_link = 'https://www.classicstamps.co.nz/' + item.get('href')
            if 'redirect1.asp' in item.get('href') and item_link not in items:
                items.append(item_link)
    except: 
        pass

    shuffle(items)
    
    return items

item_dict = {
'New Zealand Definitives':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandDefinitives&x=',
'New Zealand Commemmoratives':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandCommemmoratives&x=',
'New Zealand Health':'https://www.classicstamps.co.nz/rhome1d.asp?Header=Health&x=',
'New Zealand Christmas':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandChristmas&x=',
'New Zealand Booklets':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandBooklets&x=',
'New Zealand Airmail':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandAirmail&x=',
'New Zealand Life Insurance':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandLifeInsurance&x=', 
'New Zealand Postage Dues':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandPostageDues&x=',
'New Zealand Revenues':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandRevenues&x=',
'New Zealand Express':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandExpress&x=',
'Cinderellas':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandCinderellas&x=',
'Miscellaneous':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NZMiscellaneous&x=',
'N.Z. Postcards':'https://www.classicstamps.co.nz/rhome1d.asp?Header=N.Z.Postcards&x=',
'New Zealand Postal History':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandPostalHistory&x=',
'New Zealand Postal Stationery':'https://www.classicstamps.co.nz/rhome1d.asp?Header=NewZealandPostalStationer&x=',
'Antarctic/Arctic':'https://www.classicstamps.co.nz/rhome1d.asp?Header=Antarctic&x=',
'British Commonwealth':'https://www.classicstamps.co.nz/rhome1d.asp?Header=BritishCommonwealth&x=',
'Pacific Islands':'https://www.classicstamps.co.nz/rhome1d.asp?Header=PacificIslands1&x=',
'Foreign':'https://www.classicstamps.co.nz/rhome1d.asp?Header=Foreign&x='
    }
    
for key in item_dict:
    print(key + ': ' + item_dict[key])   

selection = input('Choose country: ')
            
category_url = item_dict[selection]
categories = get_categories(category_url)
for category in categories:
    page_url = category
    while(page_url):
        page_items, page_url = get_page_items(page_url)
        for page_item in page_items:
            stamp = get_details(page_item)