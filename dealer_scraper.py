import requests
from bs4 import BeautifulSoup
# import asyncio
# from contextlib import closing
# import grequests
# from gevent import monkey as curious_george

# curious_george.patch_all(thread=False, select=False)


# VARIABLES
categories = ['accents', 'bar', 'bedroom', 'dining', 'entertainment', 'home decor', 'living room', 'office', 'tables', 'youth']
# categories = ['bar']
cookies = {
    'ASPSESSIONIDACCASTTA': 'CIAHKGHDLDOEGNBIMMEJFNDP',
    'ASPSESSIONIDACBDQRRD': 'IPMBALHDGCEKDFABFHEEMNDD',
    '_ga': 'GA1.2.1629800997.1602682813',
    '_gid': 'GA1.2.1760408261.1602682813',
    'ASPSESSIONIDACBARRQC': 'NGDDGKMDKBEBHJMFFFGGCLFM',
    'ASPSESSIONIDCCDATTTB': 'BGDLLBNDKBLEHMKLAIGLFOHC',
    'user%5Fid': 'M5143',
    'password': 'audu9855',
    'ASPSESSIONIDACCARQRD': 'JPHJMJNDNNHHOFONKOKLOMLD',
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.monarchdirect.ca/md_productcategory_inquiry.asp?selwebcategory=YOUTH',
    'Accept-Language': 'en-US,en;q=0.9',
}

def make_soup(response, *args, **kwargs):
    soup1 = BeautifulSoup(response.content, 'html.parser')
    sku = soup1.find('p', class_='fs20').get_text()[5:]
    newPage = open('dealer-html/products/' + sku[2:] + '.html', 'w')
    newPage.write(str(soup1))
    newPage.close()
    print('finished saving raw html of ' + sku + '.')


urls = {}
for category in categories:
    with open('dealer-html/' + category + '.html', 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        arr = list(soup.find_all('div', class_='row no-space text-style'))
        for x in arr: 
            sku = x.find('div', class_='fs20').get_text()[5:]
            params = (
                ('do_filter', '1'),
                ('filter_itemno', sku),
            )
            if sku not in urls:
                urls[sku] = params

print('number of products: ' + str(len(urls)))
errors = {}
for key in urls:
    res = requests.get('http://www.monarchdirect.ca/md_product_inquiry.asp', headers=headers, params=urls[key], cookies=cookies, verify=False)
    if res.status_code == 200:
        soup1 = BeautifulSoup(res.content, 'html.parser')
        sku = soup1.find('p', class_='fs20').get_text()[5:]
        newPage = open('dealer-html/products/' + sku[2:] + '.html', 'w')
        newPage.write(str(soup1))
        newPage.close()
        print('finished saving raw html of ' + sku + '.')
    else:
        errors.add(key)

if(len(errors) > 0):
    print('your connection timed out. scrape these skus again: ' + str(list(errors)))
# res = (grequests.get('http://www.monarchdirect.ca/md_product_inquiry.asp', headers=headers, params=urls[key], cookies=cookies, verify=False, hooks={'response' : make_soup}) for key in urls)
# grequests.map(res)

# asyncio.run(main())




