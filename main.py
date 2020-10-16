import glob
from bs4 import BeautifulSoup
import pandas as pd

# - Title
# - Description
# - Price
# - SKU
# - Product Type
# - Tags
# - Weight
# - All pictures
# - Inventory Status
# - All Pictures
# - Picture's name
# - All additional information (material, collection, weight, carton dimension etc)

# VARIABLES
max_image_count = 31

# SCRAPER
sku = []
title = []
description = []
bullet_points = []
price = []
product_type = []
tags = []
images = []
inventory_status = []
data = {}
for filename in glob.glob('dealer-html/products/*'):
    # print(filename[16:20])
    imgs = []
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        sku.append('I '+ filename[21:].split('.html')[0])
        # print(filename[21:].split('.html')[0])
        title.append(soup.find('h4', class_='media-heading').get_text())
        description.append(soup.find('body').find_all('p')[3].get_text())
        bullet_points.append(', '.join([x.get_text() for x in soup.find('div', class_='col-lg-9').find('ul').find_all('li')]))
        price.append(soup.find('span', class_='primary-600 fw600').get_text())
        product_type.append(soup.find_all('p')[1].get_text().split('DEPARTMENT: ')[1])
        inventory_status.append(soup.find_all('span', class_='fw600')[1].get_text())
        imgs = [x['src'].split()[0] for x in soup.find('div', id='ProductImgAutoPlay').find_all('img')]
        imgs.append(soup.find_all('img')[3]['src'].split()[0]) 
        if len(imgs) < max_image_count:
            [imgs.append(None) for i in range(0,max_image_count-len(imgs))]

        images.append(imgs)
        raw_data = soup.find_all('td', class_='width-200')
        for x in raw_data:
            k = x.find('span', class_='fw600').get_text()[:-1]
            if k not in data:
                data[k] = []


mx = 0
for filename in glob.glob('dealer-html/products/*'):
    # print(filename[16:20])
    with open(filename, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'html.parser')
        raw_data = soup.find_all('td', class_='width-200')
        mx += 1
        for x in raw_data:
            k = x.find('span', class_='fw600').get_text()[:-1]
            data[k].append(x.get_text().split(': ')[1] if ': ' in x.get_text() else None)
            
        for key in data.keys():
            if len(data[key]) < mx:
                data[key].append(None)


data['sku'] = sku
data['title'] = title
data['description'] = description
data['bullet_points'] = bullet_points
data['price'] = price
data['product_type'] = product_type
data['inventory_status'] = inventory_status

imgss = {}

for img in images:
    for i in range(0,len(img)):
        if 'image' + str(i+1) not in imgss:
            imgss['image' + str(i+1)] = []
        imgss['image' + str(i+1)].append(img[i])
for key in imgss.keys():
    data[key] = imgss[key]


# print(imgss)
data.pop('')
df = pd.DataFrame.from_dict(data)
df.set_index('sku')
cols = df.columns.tolist()
cols.remove('sku')
cols = ['sku'] + cols
df = df[cols]
# df = df[['sku', 'BOX (SHIPPING CARTONS QTY)', 'BOX 1 - CUBE', 'BOX 1 - DEPTH / WIDTH', 'BOX 1 - HEIGHT', 'BOX 1 - LENGTH', 'BOX 1 - WEIGHT / LBS', 'BOX 1 HS NUMBER', 'BOX 1 UPC CODE', 'COUNTRY OF PRIMARY WOOD MILL', 'DEPARTMENT - 1', 'FINISH - PRIMARY', 'FINISH ATTRIBUTES', 'FINISHED ON ALL SIDES', 'FOAM DENSITY', 'KEYWORD COLOR', 'KEYWORD FEATURE', 'KEYWORD FEATURE 3', 'KEYWORD FEATURE 4', 'KEYWORD FEATURE 5', 'KEYWORD MATERIAL - FINISH', 'KEYWORD USAGE', 'KEYWORD USAGE 2', 'KEYWORD USAGE 3', 'KEYWORD USAGE 4', 'LEG - DEPTH / WIDTH', 'LEG - HEIGHT', 'LEG - LENGTH', 'LEGS - FINISH', 'LEGS - INCLUDED (QTY)', 'MATERIAL - 1', 'MATERIAL - 2', 'MATERIAL COLOR', 'MATERIAL CONTENT (%) POLYESTER', 'PACKAGING MATERIAL WEIGHT', 'PRODUCT - DEPTH / WIDTH', 'PRODUCT - HEIGHT', 'PRODUCT - LENGTH', 'PRODUCT - WEIGHT / LBS', 'PRODUCT TYPE', 'SEAT - DEPTH', 'SEAT - WIDTH', 'SEAT CUSHION THICKNESS', 'SEAT HEIGHT FROM FLOOR', 'SHAPE', 'STYLE', 'UPHOLSTERY', 'WEIGHT CAPACITY', 'WOOD PERCENTAGE (%)', 'WOOD SPECIES PRIMARY', 'ASSEMBLY REQUIRED', 'ASSEMBLY TIME', 'BED SPECS', 'DEPARTMENT - 2', 'FINISH - SECONDARY', 'KEYWORD FEATURE 2', 'KEYWORD USAGE 5', 'CARB COMPLIANT', 'KEYWORD COLOR 2', 'WINE BOTTLE QTY', 'WINE BOTTLE STORAGE', 'WINE GLASS QTY', 'WINE GLASS STORAGE', 'BOX 1 HS DESCRIPTION', 'FEATURE', 'KEYWORD MATERIAL 2 - FINISH', 'MATERIAL CONTENT (%) COTTON', 'MATERIAL CONTENT (%) POLYURETHANE', 'PIECES IN SET', 'PRODUCT 2 - DEPTH / WIDTH', 'PRODUCT 2 - HEIGHT', 'PRODUCT 2 - LENGTH', 'PRODUCT 2 - WEIGHT / LBS', 'SEAT BACK - DEPTH / WIDTH', 'SEAT BACK - HEIGHT', 'SEAT BACK - WIDTH', 'SEAT SWIVEL', 'SEAT SWIVEL RANGE', 'SET TYPE', 'WEIGHT CAPACITY 2', 'BED TYPE', 'LEG 2 - DEPTH / WIDTH', 'LEG 2 - HEIGHT', 'LEG 2 - LENGTH', 'LEG 3 - DEPTH / WIDTH', 'LEG 3 - HEIGHT', 'LEG 3 - LENGTH', 'LEGS 2 - INCLUDED (QTY)', 'LEGS 3 - INCLUDED (QTY)', 'GLASS THICKNESS', 'KEYWORD BACK END SET 1', 'KEYWORD BACK END SET 1 2', 'KEYWORD BACK END SET 1 3', 'SHELF - DEPTH / WIDTH', 'SHELF - HEIGHT', 'SHELF - LENGTH', 'SHELF 2 - DEPTH / WIDTH', 'SHELF 2 - HEIGHT', 'SHELF 2 - LENGTH', 'SHELF 3 - DEPTH / WIDTH', 'SHELF 3 - HEIGHT', 'SHELF 3 - LENGTH', 'SHELF MAXIMUM WEIGHT CAPACITY', 'SHELF MAXIMUM WEIGHT CAPACITY 2', 'SHELF MAXIMUM WEIGHT CAPACITY 3', 'SHELVES QTY', 'SHELVES QTY 2', 'SHELVES QTY 3', 'TIPPING PREVENTION', 'CASTORS LOCKING QTY', 'CASTORS QTY', 'DRAWER GLIDES', 'DRAWER INCLUDED QTY', 'DRAWER INTERIOR - DEPTH / WIDTH', 'DRAWER INTERIOR - HEIGHT', 'DRAWER INTERIOR - LENGTH', 'HARDWARE COLOR (HANDLES / KNOBS)', 'HARDWARE MATERIAL ( HANDLES / KNOBS)', 'BOX TOTAL CUBE', 'CONTAINER QTY', 'HOOKS ON COAT RACK QTY', 'KEYWORD BACK END SET 1 4', 'CARE', 'FILL MATERIALS', 'HOME DECOR CATEGORIES', 'KEYWORD BACK END SET 1 5', 'KEYWORD BACK END SET 1 6', 'KEYWORD BACK END SET 1 7', 'KEYWORD BACK END SET 1 8', 'KEYWORD BACK END SET 2', 'KEYWORD BACK END SET 2 2', 'KEYWORD BACK END SET 2 3', 'KEYWORD BACK END SET 2 4', 'KEYWORD BACK END SET 2 5', 'KEYWORD BACK END SET 2 6', 'LOCATION', 'PATTERN', 'BIFMA CERTIFIED', 'SEAT ADJUSTIBLE', 'SEAT ADJUSTIBLE RANGE', 'SEAT ARM - DEPTH / WIDTH', 'SEAT ARM - HEIGHT', 'SEAT ARM - LENGTH', 'SEAT HEIGHT FROM FLOOR 2', 'TILT MECHANISM', 'KEYWORD COLOR 3', 'KEYWORD MATERIAL 3 - FINISH', 'DRAWER LETTER SIZE', 'PRODUCT - DEPTH / WIDTH (MAX)', 'SHELF THICKNESS', 'CORNER', 'DRAWER LEGAL SIZE', 'SHELF ADJUSTABLE 2', 'SHELF HEIGHT ADJUSTABLE RANGE 2', 'SHELF THICKNESS 2', 'COUNTER HEIGHT', 'CABINET INTERIOR - DEPTH / WIDTH', 'CABINET INTERIOR - HEIGHT', 'CABINET INTERIOR - LENGTH', 'CABINETS INCLUDED QTY', 'SHELF 4 - DEPTH / WIDTH', 'SHELF 4 - HEIGHT', 'SHELF 4 - LENGTH', 'SHELF ADJUSTABLE', 'SHELF ADJUSTABLE 3', 'SHELF HEIGHT ADJUSTABLE RANGE', 'SHELF HEIGHT ADJUSTABLE RANGE 3', 'SHELF MAXIMUM WEIGHT CAPACITY 4', 'SHELF THICKNESS 3', 'SHELF THICKNESS 4', 'SHELVES QTY 4', 'PRODUCT 3 - DEPTH / WIDTH', 'PRODUCT 3 - HEIGHT', 'PRODUCT 3 - LENGTH', 'PRODUCT 3 - WEIGHT / LBS', 'WEIGHT CAPACITY 3', 'KEYWORD BACK END SET 1 10', 'KEYWORD BACK END SET 1 9', 'KEYWORD BACK END SET 2 7', 'KEYWORD BACK END SET 2 8', 'KEYWORD BACK END SET 2 9', 'SEAT FILL MATERIAL', 'LEGS - FINISH - SECONDARY', 'ACCOMMODATES ALL TV SIZES', 'STYLE NAME', 'EXTENSION LEAF QTY', 'STANDARD HEIGHT', 'TABLE LEAF - DEPTH / WIDTH', 'TABLE LEAF - LENGTH', 'TABLE SEATING CAPACITY', 'KEYWORD COLOR 4', 'ADJUSTABLE HEIGHT', 'MATERIAL CONTENT (%) LINEN', 'MATERIAL CONTENT (%) ACRYLIC', 'BOX 2 - CUBE', 'BOX 2 - DEPTH / WIDTH', 'BOX 2 - HEIGHT', 'BOX 2 - LENGTH', 'BOX 2 - WEIGHT / LBS', 'BOX 2 UPC CODE', 'DRAWER GLIDES 3', 'DRAWER GLIDES 4', 'DRAWER GLIDES 5', 'DRAWER INCLUDED QTY 2', 'DRAWER INCLUDED QTY 3', 'DRAWER INCLUDED QTY 4', 'DRAWER INCLUDED QTY 5', 'DRAWER INTERIOR 2 - DEPTH / WIDTH', 'DRAWER INTERIOR 2 - HEIGHT', 'DRAWER INTERIOR 2 - LENGTH', 'DRAWER INTERIOR 3 - DEPTH / WIDTH', 'DRAWER INTERIOR 3 - HEIGHT', 'DRAWER INTERIOR 3 - LENGTH', 'DRAWER INTERIOR 4 - DEPTH / WIDTH', 'DRAWER INTERIOR 4 - HEIGHT', 'DRAWER INTERIOR 4 - LENGTH', 'DRAWER INTERIOR 5 - DEPTH / WIDTH', 'DRAWER INTERIOR 5 - HEIGHT', 'DRAWER INTERIOR 5 - LENGTH', 'DRAWER LEGAL SIZE 4', 'DRAWER LEGAL SIZE 5', 'DRAWER LETTER SIZE 3', 'DRAWER LETTER SIZE 4', 'DRAWER LETTER SIZE 5', 'DRAWER GLIDES 2', 'DRAWER LEGAL SIZE 2', 'DRAWER LETTER SIZE 2', 'SHELF 5 - DEPTH / WIDTH', 'SHELF 5 - HEIGHT', 'SHELF 5 - LENGTH', 'SHELF ADJUSTABLE 4', 'SHELF HEIGHT ADJUSTABLE RANGE 4', 'SHELF MAXIMUM WEIGHT CAPACITY 5', 'SHELF THICKNESS 5', 'SHELVES QTY 5', 'PRODUCT - HEIGHT (MAX)', 'PRODUCT 2 - HEIGHT (MAX)', 'DRAWER LEGAL SIZE  2', 'DRAWER LETTER SIZE  2', 'FABRIC PATTERN', 'FABRIC USAGE (METERS)', 'COUNTRY OF SECONDARY WOOD MILL', 'LEG 4 - DEPTH / WIDTH', 'LEG 4 - HEIGHT', 'LEG 4 - LENGTH', 'LEGS 4 - INCLUDED (QTY)', 'BOTTOM HEM HEIGHT', 'CURTAIN HEADER TYPE', 'CURTAIN LIGHT FILTRATION', 'GROMMET DIAMETER', 'HEADER HEIGHT', 'SIDE HEM WIDTH', 'GLASS THICKNESS 2', 'LEG 5 - DEPTH / WIDTH', 'LEG 5 - HEIGHT', 'LEG 5 - LENGTH', 'LEGS 5 - INCLUDED (QTY)', 'PRODUCT 4 - DEPTH / WIDTH', 'PRODUCT 4 - HEIGHT', 'PRODUCT 4 - LENGTH', 'PRODUCT 4 - WEIGHT / LBS', 'PRODUCT 5 - DEPTH / WIDTH', 'PRODUCT 5 - HEIGHT', 'PRODUCT 5 - LENGTH', 'PRODUCT 5 - WEIGHT / LBS', 'WEIGHT CAPACITY 4', 'WEIGHT CAPACITY 5', 'WIRE MANAGEMENT', 'WIRE MANAGEMENT QTY', 'ISTA PKG', 'CA FR FOAM', 'SEAT BACK 2 - HEIGHT', 'SEAT RECLINE', 'SEAT RECLINE ANGLE', 'SEAT RECLINE ANGLE MAXIMUM', 'PILLOW TYPE', 'DOVE TAIL', 'OPTIONS', 'MATERIAL CONTENT (%) NYLON', 'SEAT 2 - DEPTH', 'SEAT 2 - WIDTH', 'SEAT CUSHION THICKNESS 2', 'WOOD SPECIES SECONDARY', 'MATERIAL CONTENT (%) OLEFIN', 'ERGONOMIC', 'SEAT BACK 2 - DEPTH / WIDTH', 'SEAT BACK 2 - WIDTH', 'SHAPE 2', 'SHAPE 3', 'SHELF 10 - DEPTH / WIDTH', 'SHELF 10 - HEIGHT', 'SHELF 10 - LENGTH', 'SHELF 6 - DEPTH / WIDTH', 'SHELF 6 - HEIGHT', 'SHELF 6 - LENGTH', 'SHELF 7 - DEPTH / WIDTH', 'SHELF 7 - HEIGHT', 'SHELF 7 - LENGTH', 'SHELF 8 - DEPTH / WIDTH', 'SHELF 8 - HEIGHT', 'SHELF 8 - LENGTH', 'SHELF 9 - DEPTH / WIDTH', 'SHELF 9 - HEIGHT', 'SHELF 9 - LENGTH', 'SHELF MAXIMUM WEIGHT CAPACITY 10', 'SHELF MAXIMUM WEIGHT CAPACITY 6', 'SHELF MAXIMUM WEIGHT CAPACITY 7', 'SHELF MAXIMUM WEIGHT CAPACITY 8', 'SHELF MAXIMUM WEIGHT CAPACITY 9', 'SHELVES QTY 10', 'SHELVES QTY 6', 'SHELVES QTY 7', 'SHELVES QTY 8', 'SHELVES QTY 9', 'DROP LEAF QTY', 'SHELF HEIGHT ADJUSTABLE RANGE 5', 'BAR HEIGHT', 'KEYBOARD TRAY', 'KEYBOARD TRAY - DEPTH / WIDTH', 'KEYBOARD TRAY - HEIGHT', 'KEYBOARD TRAY - LENGTH', 'FOAM DENSITY 2', 'SEAT CONSTRUCTION - SINUOUS SPRING', 'CABINET INTERIOR 2 - DEPTH / WIDTH', 'CABINET INTERIOR 2 - HEIGHT', 'CABINET INTERIOR 2 - LENGTH', 'CABINETS INCLUDED QTY 2', 'SEAT BACK CLEARANCE TO RECLINE', 'MATERIAL CONTENT (%) RAYON', 'title', 'description', 'bullet_points', 'price', 'product_type', 'inventory_status', 'image1', 'image2', 'image3', 'image4', 'image5', 'image6', 'image7', 'image8', 'image9', 'image10', 'image11', 'image12', 'image13', 'image14', 'image15', 'image16', 'image17', 'image18', 'image19', 'image20', 'image21', 'image22', 'image23', 'image24', 'image25', 'image26', 'image27', 'image28', 'image29', 'image30', 'image31']]
# print(df.columns.tolist())
csv = df.to_csv('products.csv', index=True)
print(df)
print('exported to csv')



