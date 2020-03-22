def date_to_num(s):
    d = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04"}
    s = s[4:]+"."+d[s[:3]]
    return s


from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import re
import matplotlib.pylab as plt

urls = ["https://www.worldometers.info/coronavirus/coronavirus-cases/#total-cases",
        "https://www.worldometers.info/coronavirus/coronavirus-death-toll/"
        ]

for i in range(3):

    page_url = urls[i%2]

    uClient = uReq(page_url)


    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
     
    script = str(page_soup.find("script",text = re.compile(r"data: ."))) if i!=2 else str(page_soup.find("script",text = re.compile(r"Total Cured")))


    #Extract Data from this mess

    start = script.find("data: ") + 5
    script1 = script[start:]
    end = script1.find("]")+1
    data_cases = eval(script1[:end]) if i == 0 else data_cases
    data_cases_death = eval(script1[:end]) if i==1 else [] if i == 0 else data_cases_death
    data_cases_recovered =  eval(script1[:end]) if i == 2 else []
    if i==0:
    # x_value
        start = script.find("categories: ") + 11
        script1 = script[start:]
        end = script1.find("]")+1
        
        x_val = list(map(date_to_num,eval(script1[:end])))
        for i in range(len(x_val)):
            if i%4!=0:
                x_val[i] = i*" "
    if i==2:
        data_cases_recovered = [0] * (len(data_cases)-len(data_cases_recovered))+data_cases_recovered


print(len(data_cases_death))

plt.plot(x_val,data_cases,"b-o")
plt.plot(x_val,data_cases_death,"r-o")
plt.plot(x_val,data_cases_recovered,"g-o")
plt.show()
