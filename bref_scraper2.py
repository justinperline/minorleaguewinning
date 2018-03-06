import pandas, numpy, csv
from lxml import html
import requests, bs4
import re, os

#Importing a list of URLs from a CSV and putting it into a list
def import_urls():
    team_season_urls = []
    with open("bref_affiliate_links.csv", 'r') as f:
        json_str = f.readlines()
        for line in json_str:
            team_season_urls.append(line.strip())
    return team_season_urls

def get_id(url):
    res = requests.get(url)
    content = html.fromstring(res.content)
    team_season_year_id = content.xpath("//*[@id='footer_header']/div/span[4]/strong/span/text()")
    return team_season_year_id

#Exports the data to a csv
def export_data(data_to_export):
    data_to_export.to_csv('bref_teams.csv')

################################################
# Main Program
################################################
team_counter = 0
all_data = pandas.DataFrame() #Creates empty dataframe to append the pulled tables to
team_season_urls = import_urls()

for item in team_season_urls:
    print(item)
    team_syid = get_id(item)
    all_data = all_data.append(team_syid)
    team_counter += 1
    print("{} Team Seasons Remaining" .format(len(team_season_urls)-team_counter))

print("\nRows = {} \nColumns = {}\n" .format(all_data.shape[0], all_data.shape[1]))

try:
    print(all_data.sample(5))
    export_data(all_data)
except:
    print("No Data Found")
