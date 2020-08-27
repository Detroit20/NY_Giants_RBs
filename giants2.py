# import the required modules

import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import re
import sqlite3





only_tr_tags = SoupStrainer('tr')




#url = 'https://www.pro-football-reference.com/teams/nyg/career-rushing.htm'
url2 = 'https://www.pro-football-reference.com/teams/nyg/career-rushing.htm#rushing::none'

# the code below creates two files
# one comprising all the data on the web page,
# the other only the data between two specific hmtl tags: tr and \tr

html = urllib.request.urlopen(url2).read()
soup = BeautifulSoup(html, 'html.parser')

souptable = BeautifulSoup(html, 'html.parser',parse_only=only_tr_tags)




# Create a list of 400 player records, but with HTML tags still in



#print(souptable)

# the code below iterates through the BS4 object, souptable,
# converts all the BS4 objects in to strings
# and then creates a list of stats for each player ' player'
#and an overall list of players, each with their own stats 'allplayers'

allplayers = []



for record in souptable:
    player = []
    allplayers.append(player)
    for stat in record:
        newstat = str(stat)
        cleanr = re.compile('<.*?>')
        clean_stat = re.sub(cleanr, '', newstat)
        player.append(clean_stat)





#print(len(player))
#print(len(allplayers))

#print(allplayers)
#print(player)

#the code below creates a function to turn strings of numbers into integers or floating point values
#while leaving strings of letters alone

def validate(num):
    try:
        return int(num)
    except (ValueError, TypeError):
        try:
            return float(num)
        except (ValueError, TypeError):
            return num

# the code below uses the function above to creates a new list of list,
#where all the elements of each player's records are strings, integer or floats

allplayers2 = []
for player in allplayers:
    player2 = []
    allplayers2.append(player2)
    for stat in player:
        newstat = validate(stat)
        player2.append(newstat)

print(len(allplayers2))

# the code below deletes from allplayers2, all the sub-lists that
#are not real player records (e.g. list of table headings)


for player in allplayers2:
    unwanted = ("From")
    unwanted2 = ("Rushing")
    if unwanted in player:
        allplayers2.remove(player)
    elif unwanted2 in player:
        allplayers2.remove(player)


print(len(allplayers2))





print(len(allplayers2))
#print(allplayers2)

# the code below create sql database

conn = sqlite3.connect('giantsoffensedb.sqlite')
cur = conn.cursor()

# the code below creates a table in the database, called Rushing
# and poputlates it with the data stored in allplayers2

cur.executescript('''DROP TABLE IF EXISTS rushing;

CREATE TABLE rushing (pfr_rating INTEGER, player_name TEXT, first_year INTEGER, last_year INTEGER, games_played INTEGER, position INTEGER, approx_value INTEGER, attempts INTEGER, total_yards INTEGER, touchdowns INTEGER, longest_run INTEGER, yards_per_carry INTEGER, yards_per_game INTEGER, fumbles INTEGER)''')

for record in allplayers2:
    cur.execute('''INSERT INTO rushing(pfr_rating, player_name, first_year, last_year, games_played, position, approx_value, attempts, total_yards, touchdowns, longest_run, yards_per_carry, yards_per_game, fumbles) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (record))
    conn.commit()
