import requests
from typing import List
from api import Players, Teams

def url(route: str):
    return f"http://127.0.0.1:8000{route}"

print("Joakim Nilsson Final task in python 2023")

def print_menu():
    print (
        """
        _____________________
        1: Add a team        |
        2: Get teams         |
        3: Delete a team     |
        4: Update a team     |
        _____________________|
        5: Add a player      |
        6: Get players       |
        7: Delete a player   |
        8: Update a player   |
        _____________________|
        9: Give player a team|
        _____________________|
        10: Exit program     |
        _____________________|
        """
    )

def add_teams():
    print("Adds a team")
    teams = input("Team name: ")
    location = input("Team location: ")
    short = input("Team short: ")
    new_teams = Teams(teams=teams, location=location, short=short)
    res = requests.post(url("/add_teams"), json=new_teams.dict())
    print(res)

def add_players():
    print("Adds a player")
    first_name = input("Player first name: ")
    last_name = input("Player last name: ")
    age = input("Player age: ")
    new_player = Players(first_name=first_name, last_name=last_name, age=int(age))
    print(new_player)
    res = requests.post(url("/add_players"), json=new_player.dict())
    print(res)

def get_teams():
    teams = []
    print("Get teams")
    res = requests.get(url("/teams"))
    if not res.status_code == 200:
        return
    data = res.json()
    for team in data:
        team = Teams(**team)
        print(f"ID: {team.id}")
        print(f"Name: {team.teams}")
        print(f"Location: {team.location}")
        print(f"Short: {team.short}")
        teams.append(team)
    return teams

def get_players():
    players = []
    print("Get players")
    res = requests.get(url("/players"))
    if not res.status_code == 200:
        return
    data = res.json()
    for player in data:
        player = Players(**player)
        print(f"ID: {player.id}")
        print(f"First name: {player.first_name}")
        print(f"Last name: {player.last_name}")
        print(f"Age: {player.age}")
        players.append(player)
    return players

def delete_teams():
    teams = get_teams()
    for team in teams:
        print(f"{team.teams}, (ID: {team.id})")
    print("Delete a team")
    team_to_delete = input("Enter the team ID that you want to delete: ")
    if not str.isdigit(team_to_delete):
        print("Please do only enter digits!")
        return
    res = requests.delete(url(f"/delete_teams/{team_to_delete}"))
    print(res.json())

def delete_players():
    players = get_players()
    for player in players:
        print(f"{player.first_name} {player.last_name} (ID: {player.id})")
    print("Delete a player")
    player_to_delete = input("Enter the player ID that you want to delete: ")
    if not str.isdigit(player_to_delete):
        print("Please do only enter digits!")
        return
    res = requests.delete(url(f"/delete_players/{player_to_delete}"))
    print(res.json())

def update_teams(teams: List[Teams]):
    team_to_update = input("Enter the team ID that you want to update: ")
    if not str.isdigit(team_to_update):
        print("Please do only enter digits!")
        return

    index = None
    for i, team in enumerate(teams):
        if team.id == int(team_to_update):
            index = i
            break

    if index == None:
        print("No team with that ID")
        return
    teams = teams[index]

    teams = input("Team name (Leave blank if same): ")
    location = input("Team location (Leave blank if same): ")
    short = input("Team short (Leave blank if same): ")

    if not teams:
        teams = teams.name
    if not location:
        location = teams.location
    if not short:
        short = teams.short
    
    new_teams = Teams(teams=teams, location=location, short=short)
    res = requests.put(url(f"/update_teams/{team_to_update}"), json=new_teams.dict())
    
    if res.ok:
        try:
            print(res.json())
        except ValueError:
            print("Not a working JSON")
    else:
        print(f"Request failed {res.status_code}")


def update_players(players: List[Players]):
    player_to_update = input("Enter the player ID that you want to update: ")
    if not str.isdigit(player_to_update):
        print("Please do only enter digits!")
        return

    index = None
    for i, player in enumerate(players):
        if player.id == int(player_to_update):
            index = i
            break

    if index == None:
        print("No player with that ID")
        return
    players = players[index]

    first_name = input("Player first name (Leave blank if same): ")
    last_name = input("Player last name (Leave blank if same): ")
    age = input("Player age (Leave blank if same): ")

    if not first_name:
        first_name = players.frist_name
    if not last_name:
        last_name = players.last_name
    if not age:
        age = players.age
    
    new_players = Players(first_name=first_name, last_name=last_name, age=age)
    res = requests.put(url(f"/update_players/{player_to_update}"), json=new_players.dict())
    
    if res.ok:
        try:
            print(res.json())
        except ValueError:
            print("Not a working JSON")
    else:
        print(f"Request failed {res.status_code}")

def assign_teams():
    res = requests.post(url("/assign_teams"))
    if res.ok:
        try:
            print(res.json())
        except ValueError:
            print("Invalid JSON")
    else:
        print(f"Request failed {res.status_code}")

def main():
    print_menu()
    choice = input("What do you want to do: ")
    choice.strip()
    if not str.isdigit(choice):
        print("Please enter one digit")
        return


    
    match int(choice):
        case 1:
            add_teams()
        case 2:
            get_teams()
        case 3:
            delete_teams()
        case 4:
            teams = get_teams()
            update_teams(teams)
        case 5:
            add_players()
        case 6:
            get_players()
        case 7:
            delete_players()
        case 8:
            players = get_players()
            update_players(players)
        case 9:
            assign_teams()
        case 10:
            exit()
        case _:
            print("Enter a valid choice")


while __name__ == "__main__":
    main()
