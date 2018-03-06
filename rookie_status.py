import requests, csv
from lxml import html

def import_urls():
    player_urls = []
    with open("rookie_limits.csv", 'r') as f:
        json_str = f.readlines()
        for line in json_str:
            player_urls.append(line.strip())
    return player_urls

def export_data(data_to_export):
    with open('rookie_limits_output.csv', 'w') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(data_to_export)

###############
# Main Program
###############
exceeding_limits_data = []
player_urls = import_urls()
counter = 0
for i in player_urls:
    print(i)
    try:
        response = requests.get(i)
        response = str(response.content)
        exceeding_limits_num = response.find("Exceeded rookie limits during")
        try:
            exceeding_limits = int(response[exceeding_limits_num+30:exceeding_limits_num+34])
        except:
            exceeding_limits = 0
        exceeding_limits_data.append(exceeding_limits)
        counter = counter + 1
        print("#{} of {}: {}" .format(counter, len(player_urls), exceeding_limits))
    except:
        print("Broken Link")

export_data(exceeding_limits_data)

