from fastapi import FastAPI, UploadFile, File
from PIL import Image
from collections import Counter
import pymongo
import json
import shutil
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins2 = [
    "localhost:3000"
    "http://localhost:3000",
    "https://localhost:3000",
    "http://192.168.0.26:3000",
]

#for testing
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    
    #copy image to local to analize it
    with open(f'{file.filename}', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    input_img = Image.open(file.filename)
    input_img = input_img.convert("RGB")
    width, height = input_img.size

    all_input_pixels = []
    for x in range(0, width):
        for y in range(0, height):
            r1, g1, b1 = input_img.getpixel((x, y))
            all_input_pixels.append([r1, g1, b1])
    converted_pixels1 = map(str, all_input_pixels)
    input_count = dict(Counter(converted_pixels1))

    #mongodb info
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["vsc-theme-finder"]
    mycol = mydb["themes"]

    winners = []
    for i in mycol.find():
        end_value = 0
        match_num = 0
        clr_info = json.loads(i["img_info"])

        for key in input_count.keys():
            if key in clr_info.keys():
                end_value += (input_count[key] - clr_info[key])
                match_num += 1

        winners.append((i["name"], i["link"], i["img_url"], match_num, end_value))

    new_list = sorted(winners, reverse=True, key=lambda d: d[3])
    new_list_cut = new_list[0:5]
    #print(*new_list1, sep = "\n")

    #delete image after we´ve gathered all the info
    os.remove(file.filename)

    return new_list_cut