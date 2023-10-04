import datetime
from selenium import webdriver # You can also use requests, just change functions all_players_list and top_players_teams.
from bs4 import BeautifulSoup
import pandas as pd 
import sys

help_message = """
Welcome to the CSGO Stats Scraper - Help Documentation.
This Program allows its users to scrape the latest CSGO Stats for Top Players and teams,
without being limited by the website's Time Filter, hence cs.py will allow the user to surf the whole database.

-- Below are the methods on how to run this program -- 

The Faster Usage Ability (From the CMD/TERMINAL directly) can be performed in 3 methods:
Method 1 (Specifying Start Date & End Date) Example:
	py cs.py 2022-07-03 2022-10-23
Method 2 (Specifying Start Date only, End Date will be considered as of today) Example:
	py cs.py 2022-07-03
Method 3 (Searching for a specific player's stats!) Example searching for player name 's1mple':
	py cs.py search for s1mple

The Regular Usage, is by running the program normally from the CMD/TERMINAL,
the flow of execution will be explained in run-time.

The Program allows its users to:
1- TPT: Search for the Top Players and Teams, for a specific time range upon user's request or ALL Time Stats.
2- SP: Search for a specific player in the top leaderboards and retrieve this player's stats.

Thanks for using our CSGO Stats Scraper.
github: gavinx17
"""
# Global Variables
average_rating = 0
average_maps = 0
average_k_d = 0
average_rounds = 0
target_player_bool = bool


# This Block is intended for the Faster Usage Ability of cs.py from console
arguments_list = sys.argv
if (len(arguments_list) > 1):
	regular_flow_execution = False
	target_player_bool = False
	if len(arguments_list) == 2:
		year,month,day = arguments_list[1].split("-")
		startDate = datetime.date(int(year),int(month),int(day))
		endDate = datetime.date.today()
	elif len(arguments_list) == 3:
		year,month,day = arguments_list[1].split("-")
		startDate = datetime.date(int(year),int(month),int(day))
		year,month,day = arguments_list[2].split("-")
		endDate = datetime.date(int(year),int(month),int(day))
		if (endDate > datetime.date.today()):
			endDate = datetime.date.today()
	elif len(arguments_list) == 4:
		if ( (arguments_list[1].lower() == "search") and (arguments_list[2].lower() == "for") ):
			quick_search_bool = True
			target_player = arguments_list[3]
			target_player_bool = True
		else:
			quick_search_bool = False
			quit()
else:
	regular_flow_execution = True


# Functions constructing cs.py:
def main_menu():
	global target_player_bool
	if (regular_flow_execution == True):
		active=True 
		while (active==True):
			user_request = input("\nSpecify your request from: TPT (Top Players & Teams), SP (Specific Player), LM (Live Matches), H for Help and X to exit the program: ")
			if user_request.lower() == "tpt":
				startDate, endDate = range_constructor()
				top_players_teams(startDate, endDate)

			elif user_request.lower() == "lm":
				target_player_bool = False
				match_stats()
       
			elif user_request.lower() == "sp":
				target_player_bool = False
				all_players_list()

			elif user_request.lower() == 'h':
				print(help_message + " \n")

			elif user_request.lower() == "x":
				print("\nThanks for using my HLTV Stats Scraper!\n")
				active=False

	#Main Method for the Faster Usage Ability of cs.py
	elif (regular_flow_execution == False):
		if len(arguments_list) == 4:
			all_players_list()
		else:
			top_players_teams(startDate, endDate)
   
def date_logic(start_end):
	"""Logical evaluation of the dates given by the user"""
	date_input = input(start_end)
	if (date_input.lower()=='today'):
		return datetime.date.today()
	else:
		year,month,day = date_input.split("-")
		evaluated_date = datetime.date(int(year),int(month),int(day))
		if (evaluated_date> datetime.date.today()):
			print(f"User specified a future date, results will be fetched up till today's date: {datetime.date.today()}")
			evaluated_date = datetime.date.today()
		return evaluated_date


def range_constructor():
	"""Constructs the date-range upon which to retrieve the stats, uses date_logic() to evaluate given dates"""
	alltime_request = input("[Y] To Retrieve the All Time Top Stats - [N] To specify date range, Choose between Y/N: ")
	if alltime_request.lower() == "y":
		startDate, endDate = None, None
	else:
		message = """	
		[+] Enter the 'From' and 'To' Dates upon which to retrieve the stats.
		[+] Use the following format: YYYY-MM-DD
		[!] Enter 'Today' if you require today's date.\n"""
		print(message)
		startDate = date_logic("From: ")
		endDate = date_logic("To: ")
	return startDate, endDate
	


def top_players_teams(startDate, endDate):
	"""The Function that scrapes statistics of top teams and players from the website and generates the reports"""
	if (startDate==None) and (endDate==None):
		url ="https://www.hltv.org/stats"
	else:
		url =f"https://www.hltv.org/stats?startDate={startDate}&endDate={endDate}"
	dr = webdriver.Chrome()
	dr.get(url)
	soup = BeautifulSoup(dr.page_source, 'html.parser')

	top_players_list = list()
	player_ranking_list = list()
	player_maps_list = list()

	top_teams_list = list()
	team_ranking_list = list()
	team_maps_list = list()

	player_map_average = 0
	player_rating_average = 0
	team_map_average = 0
	team_rating_average = 0
 
	all_top_players_info = soup.find(class_="col")
	all_top_teams_info = all_top_players_info.find_next(class_="col")

	# Top Players Scraper 
	for name in all_top_players_info.find_all('a', class_ = "name"):
		player_name = name.string
		top_players_list.append(player_name)
	for rating in all_top_players_info.find_all('div', class_="rating"):
		player_rating = rating.contents[0].string
		player_ranking_list.append(player_rating)
		player_rating = str(player_rating)
		player_rating_average = player_rating_average + float(player_rating)
	for maps in all_top_players_info.find_all('div', class_="average gtSmartphone-only"):
		player_nb_maps = maps.contents[0].string
		player_maps_list.append(player_nb_maps)
		player_nb_maps = str(player_nb_maps)
		player_map_average = player_map_average + int(player_nb_maps)

	# Top Teams Scraper 
	for name in all_top_teams_info.find_all_next('a', class_="name"):
		team_name = name.string
		top_teams_list.append(team_name)
	for rating in all_top_teams_info.find_all_next('div', class_="rating"):
		team_rating = rating.contents[0].string
		team_ranking_list.append(team_rating)
		team_rating = str(team_rating)
		team_rating_average = team_rating_average + float(team_rating)
	for maps in all_top_teams_info.find_all_next('div', class_="average gtSmartphone-only"):
		team_nb_maps = maps.contents[0].string
		team_maps_list.append(team_nb_maps)
		team_nb_maps = str(team_nb_maps)
		team_map_average = team_map_average + int(team_nb_maps)

	# Table Reports Generator in top_players_teams(startDate, endDate)
	player_table_report = pd.DataFrame(data={'Player   ':top_players_list, 'Rating':player_ranking_list, '  Maps':player_maps_list})
	team_table_report = pd.DataFrame(data={'Team   ':top_teams_list, 'Rating':team_ranking_list, '  Maps':team_maps_list})
 
	player_map_average = float((player_map_average) / len(player_table_report))
	player_rating_average = float((player_rating_average) / len(player_table_report))
	team_map_average = float((team_map_average) / len(player_table_report))
	team_rating_average = float((team_rating_average) / len(player_table_report))
 
	request = input("Retrieve reports for players/teams/both: ")
	if request.lower()=="players":
		print("\nTop Players: ","\n",player_table_report)
		print("\nTop Player Rating Average: ", round(player_rating_average,2))
		print("Top Player Map Average: ", round(player_map_average,2))
	elif request.lower()=="teams":
		print("\n\nTop Teams: ","\n",team_table_report)
		print("\nTop Team Rating Average: ", round(team_rating_average,2))
		print("Top Team Map Average: ", round(team_map_average,2))
	else:
		print("\nTop Players: ","\n",player_table_report)
		print("\nTop Players Rating Average: ", round(player_rating_average,2))
		print("Top Players Map Average: ", player_map_average)
		print("\n\nTop Teams: ","\n",team_table_report)
		print("\nTop Team Rating Average: ", round(team_rating_average,2))
		print("Top Team Map Average: ", round(team_map_average,2))
	
def all_players_list():
    
	url = "https://www.hltv.org/stats/players"
	dr = webdriver.Chrome()
	dr.get(url)
	soup = BeautifulSoup(dr.page_source, "html.parser")
	players_name_list=list()
	maps_list=list()
	rounds_list=list()
	k_d_diff_list=list()
	k_d_list=list()
	rating_list=list()
	rating_floats=list()
	k_d_floats=list()
	k_d_diff_floats=list()
	map_floats=list()
	round_floats=list()
	global average_rating
	global average_maps
	global average_k_d
	global average_rounds
	global target_player_bool
	players_dictionary = {"Player": players_name_list, "Maps": maps_list, "Rounds": rounds_list, "K-D Diff": k_d_diff_list, "K/D": k_d_list, "Rating": rating_list}

	for element_tag in soup.find_all("tbody"):
		for row in element_tag.find_all("tr"):
			count=0
			for col in row.find_all("td"):
				col = str(col)
				player_soup = BeautifulSoup(col, "html.parser")
				if player_soup.find(class_='playerCol'):
					name = player_soup.find("a").string
					players_name_list.append(name)	
				elif player_soup.find(class_='statsDetail') and count % 2 == 0:
					count+=1
					maps_list.append(player_soup.string)
					maps = str(player_soup.string)
					map_floats.append(int(maps))
				elif player_soup.find(class_='statsDetail gtSmartphone-only'):
					rounds_list.append(player_soup.string)
					rounds = str(player_soup.string)
					round_floats.append(int(rounds))
				elif player_soup.find(class_="kdDiffCol won") or player_soup.find(class_="kdDiffCol lost") or player_soup.find(class_="kdDiffCol"):
					k_d_diff_list.append(player_soup.string)
					k_d_diff = str(player_soup.string)
					k_d_diff_floats.append(int(k_d_diff))
				elif player_soup.find(class_="statsDetail") and count % 2 == 1:
					count+=1
					k_d_list.append(player_soup.string)
					k_d = str(player_soup.string)
					k_d_floats.append(float(k_d))
				elif player_soup.find(class_="ratingCol ratingPositive") or player_soup.find(class_="ratingCol ratingNegative") or player_soup.find(class_="ratingCol ratingNeutral"):
					rating_list.append(player_soup.string)
					rating = float(player_soup.string)
					rating_floats.append(rating)
     
	df = pd.DataFrame(data=players_dictionary)

	average_rating = float(sum(rating_floats) / len(df))
	average_k_d = float(sum(k_d_floats)/ len(df))
	average_maps = float(sum(map_floats) / len(df))
	k_d_diff_average = float(sum(k_d_diff_floats) / len(df))
	average_rounds = float(sum(round_floats) / len(df))

	if (target_player_bool == True): #Handling the Fast Usage Ability of cs.py
		find_player_stats(target_player, df)
		
	elif (target_player_bool == False): #Handling the Regular Usage Ability of cs.py
		print(f"\nRetrieved Stats for {len(df)} TOP players in CSGO!")
		request = input(f"Specify player name to retrieve their stats or 'ALL' to show ALL {len(df)} players' stats: ")
		if request.lower() == "all":
			print(df, "\n")
			print("Average Rating: ", round(average_rating,2))
			print("K-D Average: ", round(average_k_d, 2))
			print("K-D Diff Average: ", round(k_d_diff_average, 2))
			print("Round Average: ", round(average_rounds, 2))
			print("Map Average: ", round(average_maps, 2))
			player_lookup(df)
		else:
			find_player_stats(request, df)
   
def player_lookup(df):
	search = input("\nLookup player stats: 'YES' or 'NO': ")
	while search.lower() == "yes":
		player_name = input("\nSpecify Players Name: ")
		find_player_stats(player_name, df)
	else:
		main_menu()

def find_player_stats(target_player, df):
	"""Determines stats of a user specified player, given the dataframe to scrape"""
	target_player_name_count = 0
	for player_number in range(0,len(df)):
		if df.iloc[player_number]['Player'] == target_player:
			print_player_data(player_number, df)
			player_lookup(df)
			target_player_name_count += 1
			if target_player_name_count == 0:
				print(f"[!ERROR!] {target_player} couldn't be found in the top leaderboards.\n[!] Player Names are CASE Sensitive.")
  
def print_player_data(player_number, df):
	print("Player  [" + df.iloc[player_number]['Player'] + "]")
	print("Maps  [" + df.iloc[player_number]['Maps'] + "]" + "	VS Average Maps:  [", round(average_maps,2), "]")
	print("Rating  [" + df.iloc[player_number]['Rating'] + "]" + "  VS   Average Rating:  [", round(average_rating,2), "]")
	print("Rounds  [" + df.iloc[player_number]['Rounds'] + "]" + "  VS Average Rounds:  [", round(average_rounds,2), "]")
	print("K/D  [" + df.iloc[player_number]['K/D'] + "]" + "  VS Average K/D:  [", round(average_k_d,2), "]")
	print("K-D Diff  [" + df.iloc[player_number]['K-D Diff'] + "]")
 
def match_stats():
	url = "https://www.hltv.org/matches"
	dr = webdriver.Chrome()
	dr.get(url)
	soup = BeautifulSoup(dr.page_source, "html.parser")
#	df = get_player_df()
	team_names = list()
	count = 0
	team_one_players = {"Team": team_names}
	print("[+]LIVE MATCHES:\n")
	for element_tag in soup.find_all(class_="widthControl"):
		for row in element_tag.find_all(class_="newMatches"):
			for col in row.find_all(class_="liveMatchesContainer"):
				for matches in col.find_all(class_="matchTeamName"):
					teams = matches.string
					if count % 2 == 1:
						print(teams)
						count = count + 1
					elif count % 2 == 0: 
						print(teams + " vs ", end="")
						count = count + 1
    
def get_player_df():
	url = "https://www.hltv.org/stats/players"
	dr = webdriver.Chrome()
	dr.get(url)
	soup = BeautifulSoup(dr.page_source, "html.parser")
	players_name_list=list()
	maps_list=list()
	rounds_list=list()
	k_d_diff_list=list()
	k_d_list=list()
	rating_list=list()
	players_dictionary = {"Player": players_name_list, "Maps": maps_list, "Rounds": rounds_list, "K-D Diff": k_d_diff_list, "K/D": k_d_list, "Rating": rating_list}

	for element_tag in soup.find_all("tbody"):
		for row in element_tag.find_all("tr"):
			count=0
			for col in row.find_all("td"):
				col = str(col)
				player_soup = BeautifulSoup(col, "html.parser")
				if player_soup.find(class_='playerCol'):
					name = player_soup.find("a").string
					players_name_list.append(name)	
				elif player_soup.find(class_='statsDetail') and count % 2 == 0:
					count+=1
					maps_list.append(player_soup.string)
				elif player_soup.find(class_='statsDetail gtSmartphone-only'):
					rounds_list.append(player_soup.string)
				elif player_soup.find(class_="kdDiffCol won") or player_soup.find(class_="kdDiffCol lost") or player_soup.find(class_="kdDiffCol"):
					k_d_diff_list.append(player_soup.string)
				elif player_soup.find(class_="statsDetail") and count % 2 == 1:
					count+=1
					k_d_list.append(player_soup.string)
				elif player_soup.find(class_="ratingCol ratingPositive") or player_soup.find(class_="ratingCol ratingNegative") or player_soup.find(class_="ratingCol ratingNeutral"):
					rating_list.append(player_soup.string)
		
	df = pd.DataFrame(data=players_dictionary)
	return df
# Find someway to pass rating_average
## Main Method controlling the actual flow of execution

#Main Method for the Regular Usage of cs.py
main_menu()
