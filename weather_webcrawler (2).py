from bs4 import BeautifulSoup 
import requests
import time
from RequestGuard import RequestGuard , get_domain
def insert_High_low_dwpoint(spans_list):
    insert_list= ['Dew_point','Low','High','Feelslike']

    for item in insert_list:
        spans_list.insert(7,item)

    return spans_list
def title_genorator(html):
    all_spans = html.find_all('span', class_="Ellipsis--ellipsis--zynqj",style="-webkit-line-clamp:2" )
    additional_list = ['Night','Day','Current']

    for item in additional_list:
        all_spans.insert(0,item)

    for i in range(2):
        dunmb_ette = html.find_all('span', class_="Ellipsis--ellipsis--zynqj",style="-webkit-line-clamp:2" )
        
        for span in dunmb_ette:
            all_spans.append(span)

    all_spans=insert_High_low_dwpoint(all_spans)

    for span in all_spans:

        if hasattr(span,".text")==True:
            yield span.text

        else:
            yield span
def get_temperature_and_titles(html):
    all_spans = html.find_all('span',{'data-testid':'TemperatureValue'}, dir='ltr')
    list_of_temp_string = []
    list_of_temp_numb = []
    list_of_titles = []
    gen=title_genorator(html)
    for i in range(16):

        next_title=next(gen)
        list_of_titles.append(next_title)
        print(next_title)
        list_of_temp_string.append(all_spans[i])
        print(all_spans[i].text)

    for temp in list_of_temp_string:
        if (temp.text!= '--'):
            list_of_temp_numb.append(float(str(temp.text)[:-1]))
        else:
            list_of_temp_numb.append("--")

    return list_of_temp_numb,list_of_titles
def Jacket_Decider(temp_list):
    morning_supercold=20
    morning_prettycold=35
    morning_warm=50
    afternoon_supercold=40
    afternoon_prettycold=60
    morning_real = temp_list[3]
    afternoon_real = temp_list[4]
    if morning_real<morning_supercold:
        return "a hoodie and a heavy coat"
    if morning_real<=morning_prettycold and afternoon_real<afternoon_supercold:
        return 'a heavy coat'
    if morning_real<=morning_prettycold and afternoon_real<afternoon_prettycold:
        return 'a hoodie and a jaket'
    if morning_real>morning_prettycold and morning_real<morning_warm:
        return "a hoodie"
    else:
        return "Nothing"
def getlocation(html):
    location = html.find_all('h1', class_="CurrentConditions--location--yub4l")
    return location[0].text
def weather_webcrawler():
    url = 'https://weather.com/weather/today/l/ea835c43eb02f0cf867f2174064b6a7dc60d2358338d270fb0d6134abb8f335e' #this url can be replaced with you home town
    # user_url = input("please enter your url: ")
    # if user_url != "":
    #     url = user_url

    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    location = getlocation(html)
    numbers, titels = get_temperature_and_titles(html)   
    print(f"your current temp in {location} is {numbers[0]}")
    print(f"your high for today is {numbers[1]}")
    print(f"your low for today is {numbers[2]}")
    Jacket = Jacket_Decider(numbers)
    print(f"given your temperatrues its recomended that you wear {Jacket}")
    time.sleep(5)

    return None
"""Current
48°
Day
49°
Night
40°
Morning
41°
Afternoon
47°
Evening
41°
Overnight
43°
Feelslike
47°
High
49°
Low
40°
Dew_point
32°
Now
48°
3 pm
47°
4 pm
47°
5 pm
46°
6 pm
42°"""
weather_webcrawler()
