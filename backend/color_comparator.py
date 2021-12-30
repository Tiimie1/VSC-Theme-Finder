from PIL import Image
from collections import Counter
import pymongo
import json

input_img = Image.open("ss3.png")
input_img = input_img.convert("RGB")
width, height = input_img.size

all_input_pixels = []

for x in range(0, width):
    for y in range(0, height):
        r1, g1, b1 = input_img.getpixel((x, y))
        all_input_pixels.append([r1, g1, b1])
converted_pixels1 = map(str, all_input_pixels)
input_count = dict(Counter(converted_pixels1))

img_info = []
highest_num = 0
highest_name = ""

#mongodb info
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["vsc-theme-finder"]
mycol = mydb["themes"]

winners = []

print(json.loads(mycol.find_one()["img_info"]).keys())

for i in mycol.find():
    end_value = 0
    match_num = 0
    clr_info = json.loads(i["img_info"])

    for key in input_count.keys():
        if key in clr_info.keys():
            end_value += (input_count[key] - clr_info[key])
            match_num += 1

    winners.append((i["link"], i["img_url"] ,match_num, end_value))

    if(match_num > highest_num):
        highest_num = match_num
        highest_name = i["name"]
    # print("image" + str(i))
    # print("value: ", end_value)
    # print("num of matches: ", match_num)
    # print("------------------------------------")

new_list = sorted(winners, key=lambda d: d[2])
print(*new_list, sep = "\n")