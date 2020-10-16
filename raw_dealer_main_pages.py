
import requests
from bs4 import BeautifulSoup

# VARIABLES
categories = ['accents', 'bar', 'bedroom', 'dining', 'entertainment', 'home decor', 'living room', 'office', 'tables', 'youth']

cookies = {
    'ASPSESSIONIDACCASTTA': 'CIAHKGHDLDOEGNBIMMEJFNDP',
    'ASPSESSIONIDACBDQRRD': 'IPMBALHDGCEKDFABFHEEMNDD',
    '_ga': 'GA1.2.1629800997.1602682813',
    '_gid': 'GA1.2.1760408261.1602682813',
    'ASPSESSIONIDACBARRQC': 'NGDDGKMDKBEBHJMFFFGGCLFM',
    'ASPSESSIONIDCCDATTTB': 'BGDLLBNDKBLEHMKLAIGLFOHC',
    'user%5Fid': 'M5143',
    'password': 'audu9855',
    '_gat_gtag_UA_114692620_1': '1',
}

headers = {
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://www.monarchdirect.ca/md_productcategory_inquiry.asp?selwebcategory=BAR',
    'Accept-Language': 'en-US,en;q=0.9',
}


# SCRAPER
with requests.Session() as s:
    for category in categories:
        params = (
            ('selwebcategory', category),
        )
        page = requests.get('http://www.monarchdirect.ca/md_productcategory_inquiry.asp', headers=headers, params=params, cookies=cookies, verify=False)

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            newPage = open('dealer-html/' + category + '.html','w')
            newPage.write(str(soup))
            newPage.close()
            print('finished saving raw html of ' + category + '.')

