import json
import sqlite3
import requests

response = requests.get('https://www.balldontlie.io/api/v1/teams')
if(response.status_code != requests.codes.ok):
    print("Something went wrong!")
else:
    teams = response.json()

teams_important_information = []
dictionary_list=[]

for team in teams["data"]:
    name=team["full_name"]
    city=team["city"]
    conference=team["conference"]
    division=team["division"]

    information=name,city,conference,division

    teams_dictionary={
        "name":name,
        "city":city,
        "conference":conference,
        "division":division
    }

    teams_important_information.append(information)
    dictionary_list.append(teams_dictionary)

db=sqlite3.connect("NBA_teams.db")
cursor=db.cursor()

cursor.execute('''
        CREATE TABLE NBA_TEAMS_INFORMATION (name string, city string, conference string, division string)
''')

cursor.executemany('''INSERT INTO NBA_TEAMS_INFORMATION VALUES (?,?,?,?)''',teams_important_information)

db.commit()
db.close()

#creating new json file
with open("NBA_teams_info.json","w") as file:
    json.dump(dictionary_list,file,indent=4)
