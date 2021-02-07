import requests
import json
from lxml import html


url = 'https://www.supremecommunity.com'

def __get_dropweek_hrefs():
    print('Getting dropweek hrefs...')
    seasons = [
        'spring-summer2017',
        'fall-winter2017',
        'spring-summer2018',
        'fall-winter2018',
        'spring-summer2019'
        ]
    season_hrefs = ['/season/'+season+'/droplists/' for season in seasons]

    week_hrefs = []
    for href in season_hrefs:
        r = requests.get(url+href)
        text = r.text
        hxt = html.fromstring(text)
        week_hrefs += hxt.xpath('/html/body/div[2]/section[3]/div/div/div[1]/div/a/@href')
    print('Done.')
    return week_hrefs

def __get_pages_itemids(href):
    print('Getting ids from : ', href)
    r = requests.get(url+href)
    text = r.text
    hxt = html.fromstring(text)
    itemids = hxt.xpath('/html/body/div[2]/section[2]/div[1]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/div[1]/@data-itemid')
    print('Done.')
    return itemids

def __get_all_itemids():
    hrefs = __get_dropweek_hrefs()
    ids = []
    for href in hrefs:
        ids += __get_pages_itemids(href)
    return ids

def __get_item_info(itemid):
    print('Getting info for item# : ', itemid)
    link = url+'/season/itemdetails/'+itemid
    r = requests.get(link)
    text = r.text
    hxt = html.fromstring(text)
    details = hxt.xpath('//div[@class="row detail-row"]')[0]
    print('Done.')

    description = details.xpath('./h2[@class="detail-desc"]/text()')
    if len(description) > 0:
        description = description[0]
    else:
        description = None
    return {
        'title': details.xpath('./h1[@class="detail-title"]/text()')[0],
        'description': description,
        'release_date': details.xpath('./h2[@class="details-release-small"]/span/text()')[0],
        'upvotes': int(details.xpath('.//p[@class="upvotes hidden"]/text()')[0]),
        'downvotes': int(details.xpath('.//p[@class="downvotes hidden"]/text()')[0]),
        #'price_usd': int((details.xpath('.//span[@class="label label--inline price-label"]/text()')[0]).split(' ')[-1]),
        'colors': details.xpath('./div[1]/div/ul/li[3]/div[2]/div/span/text()') or None,
        'scraped_link': link,
        'itemid': itemid
    }

def get_all_items():
    itemids = __get_all_itemids()
    items = []
    for itemid in itemids:
        items.append(__get_item_info(itemid))
    print('Found %s items.' % len(items))
    return items

def update_supremecommunity_json():
    items = get_all_items()
    with open('./supremecommunity.json', 'w') as f:
        json.dump(items, f, indent = True)
