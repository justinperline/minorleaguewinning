import pandas, numpy, csv
import lxml.html as LH
import requests, bs4
import re, os

url = "https://www.baseball-reference.com/register/team.cgi?id=8ffc2f78"
tableID = "standard_roster"

res = requests.get(url)
comm = re.compile("<!--|-->")
soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
tables = soup.findAll('table', id = tableID)
tables = str(tables)
linklist = []
playerdatalist = re.split('<tr>', tables)
for i in playerdatalist[2:]:
    link = i[i.find("data-append-csv=")+28:i.find("data-stat")]
    linklist.append(link)
print(linklist)