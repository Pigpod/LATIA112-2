import requests
from bs4 import BeautifulSoup
import pandas as pd

#設定目標網頁
url = "https://www.db.yugioh-card.com/yugiohdb/card_search.action?ope=1&sess=1&pid=1000009200000&rp=99999&request_locale=ja"

#儲存網頁回傳，並以utf-8編碼
response = requests.get(url)
response.encoding = 'utf-8'

#將網頁源碼存進soup
soup = BeautifulSoup(response.text,'html.parser')

#從soup中找到所要的資料的所在位址
items = soup.find_all('div' , class_='t_row c_normal')

#解析網頁並抓取資料
data = []
index = 1

for item in items:
    try:
        #解析卡片資訊
        card_tag = item.find('dl').find('dd',class_= 'box_card_name flex_1 top_set').find('span', class_ = 'card_name')
        card = card_tag.get_text(strip=True)
        attribute_tag = item.find('dl').find('dd',class_= 'box_card_spec flex_1').find('span').find('span')
        attribute = attribute_tag.get_text(strip=True)
        effect_tag = item.find('dl').find('dd',class_= 'box_card_text c_text flex_1')
        effect = effect_tag.get_text(strip=True)

        #將解析出的資料存入字典，並添加到列表中
        temp_data = {
            "卡名": card,
            "屬性": attribute,
            "效果": effect
        }
        data.append(temp_data)

        print(f"------卡片{index}------")
        print(f"卡名:{card}")
        print(f"屬性:{attribute}")
        print(f"效果:{effect}")
        index+=1
    except:
        continue

#將抓取的資料轉成DataFrame，並存成csv檔
df = pd.DataFrame(data)
filename = 'requests_cards.csv'
df.to_csv(filename, index=False, encoding='utf_8_sig')
