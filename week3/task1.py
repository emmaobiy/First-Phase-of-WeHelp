import urllib.request
import json
import re
import csv

# 下載第一個檔案
url1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
response1 = urllib.request.urlopen(url1)
data1 = response1.read().decode('utf-8')

# 下載第二個檔案
url2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
response2 = urllib.request.urlopen(url2)
data2 = response2.read().decode('utf-8')

# 解析 data1 和 data2 中的 JSON 數據
json_data1 = json.loads(data1)
json_data2 = json.loads(data2)

# 取第一個檔案中的景點名稱、SERIAL_NO、經度、緯度和第一張圖片的 URL
def info1(data):
    attractions = {}
    for result in data["data"]["results"]:
        serial_no = result.get("SERIAL_NO", "")
        name = result.get("stitle", "")
        longitude = result.get("longitude", "")
        latitude = result.get("latitude", "")
        filelist = result.get("filelist", "")

        if filelist:
            urls = re.findall(r'https://[^\s]+?\.(?:jpg|jpeg|png|gif)', filelist, re.IGNORECASE)
            first_image_url = urls[0] if urls else ""
        else:
            first_image_url = ""
        attractions[serial_no] = {"name": name, "longitude": longitude, "latitude": latitude, "first_image_url": first_image_url}
    return attractions

# 取第一個檔案中的景點資訊
attractions1 = info1(json_data1)

# 取第二個檔案中的景點地址、捷運站和 SERIAL_NO
def info2(data):
    attractions = {}
    for result in data["data"]:
        serial_no = result.get("SERIAL_NO", "")
        address = result.get("address", "")
        station = result.get("MRT", "")
        attractions[serial_no] = {"address": address, "station": station}
    return attractions

# 取第二個檔案中的景點資訊
attractions2 = info2(json_data2)

# 以捷運站為鍵、景點名為值的字典
mrt_and_spots = {}
for serial_no, info in attractions2.items():
    if serial_no in attractions1:
        station = info.get("station", "")
        address = info.get("address", "")
        if station:
            if station not in mrt_and_spots:
                mrt_and_spots[station] = []
            mrt_and_spots[station].append(attractions1[serial_no]["name"])

# 寫入 mrt.csv
with open('mrt.csv', 'w', newline='', encoding='utf-8') as csvfile:
    for station, spots in mrt_and_spots.items():
        csvfile.write(f"{station},{', '.join(spots)}\n")

# 寫入 spot.csv
with open('spot.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['景點名稱', '行政區', '經度', '緯度', '圖片網址']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    for serial_no, info in attractions1.items():
        name = info.get("name", "")
        address = attractions2.get(serial_no, {}).get("address", "未知")
        # 使用正則表達取行政區
        district_match = re.search(r'([\u4e00-\u9fa5]+區)', address)
        district = district_match.group(1) if district_match else "未知"
        longitude = info.get("longitude", "")
        latitude = info.get("latitude", "")
        first_image_url = info.get("first_image_url", "")
        writer.writerow({'景點名稱': name, '行政區': district, '經度': longitude, '緯度': latitude, '圖片網址': first_image_url})
