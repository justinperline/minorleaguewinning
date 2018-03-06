import pandas, numpy, csv
import lxml.html as LH
import requests, bs4
import re, os

## This function simply takes a url and provides the ids
## from the html tables that the code provided here can access.
## Using findTables is great for determining options for the
## pullTable function for the tableID argument.
def findTables(url):
    res = requests.get(url)
    ## The next two lines get around the issue with comments breaking the parsing.
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    divs = soup.findAll('div', id = "content")
    divs = divs[0].findAll("div", id=re.compile("^all"))
    ids = []
    for div in divs:
        searchme = str(div.findAll("table"))
        x = searchme[searchme.find("id=") + 3: searchme.find(">")]
        x = x.replace("\"", "")
        if len(x) > 0:
            ids.append(x)
    return(ids)

## Pulls a single table from a url provided by the user.
## The desired table should be specified by tableID.
## This function is used in all functions that do more complicated pulls.
def pullTable(url, tableID):
    try:
        res = requests.get(url)
        ## Work around comments
        comm = re.compile("<!--|-->")
        soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
        tables = soup.findAll('table', id = tableID)
        data_rows = tables[0].findAll('tr')
        data_header = tables[0].findAll('thead')
        data_header = data_header[0].findAll("tr")
        data_header = data_header[0].findAll("th")
        game_data = [[td.getText() for td in data_rows[i].findAll(['th','td'])]
            for i in range(len(data_rows))
            ]
        data = pandas.DataFrame(game_data)
        header = []
        for i in range(len(data.columns)):
            header.append(data_header[i].getText())
        data.columns = header
        url_stringified = url[56:]
        data.insert(loc=0, column='Team ID', value=url_stringified) #Inserts column with shortened URL value
        data["Link"] = ""
        linklist = get_links(url, tableID)
        for i in range(0,len(linklist)):
            data.at[i, "Link"] = linklist[i]
        data = data.loc[data[header[0]] != header[0]]
        data = data.reset_index(drop = True)
        return(data)
    except:
        print("No Standard Roster Found")

#Importing a list of URLs from a CSV and putting it into a list
def import_urls():
    team_season_urls = []
    with open("affiliate_ids_2017.csv", 'r') as f:
        json_str = f.readlines()
        for line in json_str:
            team_season_urls.append(line.strip())
    return team_season_urls

#Exports the data to a csv
def export_data(data_to_export):
    data_to_export.to_csv('2017_minors.csv')

#Returns list of links from roster table
def get_links(url, tableID):
    res = requests.get(url)
    comm = re.compile("<!--|-->")
    soup = bs4.BeautifulSoup(comm.sub("", res.text), 'lxml')
    tables = soup.findAll('table', id = tableID)
    tables = str(tables)
    linklist = []
    playerdatalist = re.split('<tr>', tables)
    for i in playerdatalist[1:]:
        link = i[i.find("data-append-csv=")+28:i.find("data-stat")]
        linklist.append(link)
    return linklist

################################################
# Main Program
################################################
team_counter = 0
all_data = pandas.DataFrame() #Creates empty dataframe to append the pulled tables to
team_season_urls = import_urls()

for item in team_season_urls:
    print(item)
    data = pullTable(item, "standard_roster")
    all_data = all_data.append(data)
    team_counter += 1
    print("{} Team Seasons Remaining" .format(len(team_season_urls)-team_counter))

print("\nRows = {} \nColumns = {}\n" .format(all_data.shape[0], all_data.shape[1]))
try:
    print(all_data.sample(5))
    export_data(all_data)
except:
    print("\nNo Data Found")