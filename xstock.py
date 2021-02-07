import requests
import json

seasons = {
    'ss14', 'fw14',
    'ss15', 'fw15',
    'ss16', 'fw16',
    'ss17', 'fw17',
    'ss18', 'fw18',
    'ss19'
}

tags = {
    'accessories',
    'bottoms',
    'headwear',
    'jackets',
    'shirts',
    't-shirts',
    'tops/sweatshirts',
    'bags',
    'skate'
}

brand = 'supreme'

def __url_add_tags(season, tag):
    return 'https://stockx.com/api/browse?_tags=supreme,season|'+season+','+tag

def __url_add_page_number(url, page_num):
    return url+'&page='+str(page_num)

def __get_products(url):
    r = requests.get(url)
    page_products = json.loads(r.content)['Products']
    return page_products

def get_supreme_hits():
    print('Getting all Supreme products...')
    products = []
    for season in seasons:
        for tag in tags:
            page_number = 1
            url_w_tags = __url_add_tags(season, tag)
            page_url = __url_add_page_number(url_w_tags, page_number)
            page_products = __get_products(page_url)
            while page_products:
                print ('Got Products for: ', season, tag, page_number)
                #print (page_products)
                page_number += 1
                products += page_products
                page_url = __url_add_page_number(url_w_tags, page_number)
                page_products = __get_products(page_url)
    print('Done. Got %i products.' % len(products))
    return products

def update_xstock_json():
    products = get_supreme_hits()
    with open('./xstock.json', 'w') as f:
        json.dump(products, f, indent = True)





def __get_product_activity(product_id):
    print('Getting activity for id %s.' % product_id)
    url = 'https://stockx.com'
    product_search = '/api/products/%s/activity?state=480&currency=USD&limit=10&page=%s&sort=createdAt&order=DESC'
    page_number = 1
    r = requests.get(url + product_search % (product_id, str(page_number)))
    page  = json.loads(r.content)
    try:
        if page['Pagination']['total'] is 0:
            return
    except:
        return
    product_activity = page['ProductActivity']
    while page['Pagination']['nextPage']:
        page_number += 1
        r = requests.get(url + product_search % (product_id, str(page_number)))
        page  = json.loads(r.content)
        product_activity += (page['ProductActivity'])
    return product_activity


def get_all_products_activity():
    with open('./xstock.json', 'r') as f:
        products = json.load(f)
    activity = []
    for p in products:
        activity.append({
            'id': p['id'],
            'activity': __get_product_activity(p['id'])
        })
    return activity


def update_activity_json():
    activity = get_all_products_activity()
    with open('./activity.json', 'w') as f:
        json.dump(activity, f, indent = True)
