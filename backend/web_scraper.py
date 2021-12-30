from bs4 import BeautifulSoup
import requests
import urllib.request
import pymongo
from PIL import Image
from collections import Counter
import json

url_base = "http://orta.io/vscode-themes/"

#mongodb info
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["vsc-theme-finder"]
mycol = mydb["themes"]

page = requests.get(url_base)
print(page.status_code)

doc = BeautifulSoup(page.content, "html.parser")

links = []
names = []
images = []

count = 1

for img in doc.find_all('img'):
    #if( count > 3 ): break
    img_src_clean = img['src'].replace(" ", "%20")
    #problems with unicode char u+ff0d
    if '－' in img_src_clean: continue
    r = requests.get(url_base + img_src_clean, stream=True)
    if r.status_code == 200:
        a = img.find_previous_sibling('a')
        link = a.get('href')
        name = a.find('h3').string
        names.append(name)
        links.append(link)
        images.append(url_base + img_src_clean)
        #print(img_src_clean)
        urllib.request.urlretrieve(url_base + img_src_clean, "image" + str(count))
        print("downloading: ", count)
        count += 1

img_info = []

for i in range(1, count):
    img = Image.open("image" + str(i))
    img = img.convert("RGB")
    width, height = img.size
    all_pixels = []
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x, y))
            all_pixels.append([r, g, b])
    converted_pixels = map(str, all_pixels)
    rgb_num = dict(Counter(converted_pixels))
    img_info.append(rgb_num)
    print("calculating: ", i)

result = zip(names, links, images, img_info)

for item in result:
    mydict = {
        "name": str(item[0]),
        "link": str(item[1]),
        "img_url": str(item[2]),
        "img_info": json.dumps(item[3])
    }
    x = mycol.insert_one(mydict)





#print(result.string)

