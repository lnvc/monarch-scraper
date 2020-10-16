import requests
from bs4 import BeautifulSoup

# VARIABLES
categories = ['new', 'accents', 'bar', 'bedroom', 'dining', 'entertainment', 'home-decor', 'living-room', 'office', 'tables', 'youth']

# SCRAPER
for category in categories:
    page = requests.get("http://www.monarchspec.com/en/" + category + ".html?p=1&product_list_limit=24")

    if page.status_code == 200:
        soup = BeautifulSoup(page.content, 'html.parser')
        newPage = open('html/' + category + '/' + category + '_page1.html','w')
        newPage.write(str(soup))
        newPage.close()
        print('finished saving raw html of ' + category + ' page 1.')

        try: 
            pages = soup.find_all('ul', class_='items pages-items')[0]
            nextPage = pages.find('li', class_='item pages-item-next')
        except:
            nextPage = None

        i = 2
        while(nextPage):
            address = requests.get(nextPage.a['href'])
            addressSoup = BeautifulSoup(address.content, 'html.parser')
            pages = addressSoup.find_all('ul', class_='items pages-items')[0]
            nextPage = pages.find('li', class_='item pages-item-next')
            temp = open('html/' + category + '/' + category + '_page' + str(i) + '.html','w')
            temp.write(str(addressSoup))
            temp.close()
            print('finished saving raw html of ' + category + ' page ' + str(i) + '.')
            i+=1
            if(not nextPage):
                break



