import requests, json, csv, time

#Gets data from webpage and transforms it into a list of dictionaries for each game
def get_data(url):
    try:
        game_log = []
        response = requests.get(url)
        schedule = response.json()
        num_games = int(schedule['schedule_team_complete']['queryResults']['totalSize'])
        row_num = 0
        while num_games > 0:
            opponent_score = schedule['schedule_team_complete']['queryResults']['row'][row_num]['opponent_score']
            team_score = schedule['schedule_team_complete']['queryResults']['row'][row_num]['team_score']
            game_time_et = schedule['schedule_team_complete']['queryResults']['row'][row_num]['game_date']
            result = schedule['schedule_team_complete']['queryResults']['row'][row_num]['result']
            game_status = schedule['schedule_team_complete']['queryResults']['row'][row_num]['game_status']
            season_id = schedule['schedule_team_complete']['queryResults']['row'][row_num]['editorial_stats_season']
            team_id = schedule['schedule_team_complete']['queryResults']['row'][row_num]['team_id']
            data_list = {
            'game_time_et' : game_time_et, 
            'game_status' : game_status, 
            'result' : result, 
            'team_score': team_score, 
            'opponent_score' : opponent_score,
            'season_id' : season_id,
            'team_id' : team_id}
            game_log.append(data_list)
            num_games -= 1
            row_num += 1
        return game_log
    except:
        print("No Team-Season ID")

#Exporting the list of dictionaries to a CSV file
def export(data_to_export):
    try:
        with open("milb_game_logs2.csv", 'a', newline='') as csvfile:
            fieldnames = ['game_time_et', 'game_status', 'result', 'team_score', 'opponent_score', 'season_id', 'team_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for item in data_to_export:
                #for jitem in item:
                    #writer.writerow(jitem)
                writer.writerow(item)
    except:
        print("No data found")

#Importing a list of URLs from a CSV and putting it into a list
def import_urls():
    team_urls = []
    with open("milb_affiliation_links2.csv", 'r') as f:
        json_str = f.readlines()
        for line in json_str:
            team_urls.append(line.strip())
    return team_urls

###################################################################
# Main Program
###################################################################

final_data = []
team_urls = import_urls()
team_counter = 0
e_c = 0
e_t = 0
e_a = 0
e_r = 0
for item in team_urls:
    start = time.time()
    data = get_data(item)
    print("Game Log {} Recorded" .format(item[-24:]))
    #final_data.append(data)
    #print("Game Log {} Added" .format(item[-24:]))
    team_counter += 1
    export(data)
    print("Team-Seasons Remaining: {}" .format(len(team_urls)-team_counter))
    end = time.time()
    elapsed = end - start
    e_t += elapsed
    e_c += 1
    e_a = e_t/e_c
    e_r = (e_a*len(team_urls)) - (e_a*(len(team_urls)-team_counter))
    print("Estimated Time: {:.0f}m {:.0f}s" .format(e_r//60, e_r%60))

#export(final_data)
#print("Data Exported")