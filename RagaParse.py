import requests
from bs4 import BeautifulSoup
import json

def cleanse_data(instr):
    outstr = instr
    outstr = outstr.replace('\xa0',' ').replace('\n','')
    outstr = outstr.replace(u"\u2081",'1')
    outstr = outstr.replace(u"\u2082",'2')
    outstr = outstr.replace(u"\u2083",'3')

    return outstr

page = requests.get("https://en.wikipedia.org/wiki/List_of_Janya_ragas")

soup = BeautifulSoup(page.content,"html.parser")

html = list(soup.children)[2]
body = list(html.children) [3]
raga_table = body.find("table", class_="wikitable")

raga_table_tds = raga_table.find_all("td")

raga_details={}
raga_list=[]
raga_tds = raga_table_tds

# Use later for Raga wise processing
# raga_scale_thumbnail = body.find("div",class="thumbinner")


idx = 0

for elem in range(0,len(raga_tds)):

    data_val = raga_tds[elem].get_text()

    if idx == 0:
    
        mela_num = data_val.split()[0]

        if mela_num.isdigit():
            mela_raga = ' '.join(data_val.split()[1:])
            raga_details["name"] = ' '.join(data_val.split()[1:])
            is_mela = True
        else:
            is_mela = False
            raga_details["name"] = data_val

        if is_mela == False:
            raga_details["mela_raga"] = mela_raga
            raga_details["mela_num"] = ""
        else:
            raga_details["mela_raga"] = ""
            raga_details["mela_num"] = mela_num

        # Find link if available

        raga_link = raga_tds[elem].find("a",href=True)
        if raga_link != None:  
            raga_details["link"] = "https://en.wikipedia.org" + raga_link["href"]
        else:
            raga_details["link"] = ""


    elif idx == 1:
        raga_details["arohana"] = cleanse_data(data_val)
    else:
        raga_details["avarohana"] = cleanse_data(data_val)
    
    idx = idx + 1

    # Reset index to 0
    if idx > 2:
        idx = 0
        raga_list.append(raga_details)
        raga_details={}
   
# print(len(raga_list))
# print(raga_list[0])
# print(raga_list[948])

with open("raga_json.json","w", encoding="utf8") as fout:
    json.dump(raga_list, fout, ensure_ascii=False)

