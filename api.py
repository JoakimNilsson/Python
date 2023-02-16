from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from my_db import FootballDatabase
import random

class Teams(BaseModel):
    id: int = None
    teams: str
    location: str
    short: str

class Players(BaseModel):
    id: int = None
    first_name: str
    last_name: str
    age: int = None
    team_id: int = None

app = FastAPI()
db = FootballDatabase("FootballDatabase.db")

app.curr_id = 1
app.teams: List[Teams] = []
app.players: List[Players] = []

@app.get("/")
def root():
    return "Joakim Nilsson final task in python programming 2023!"

@app.get("/teams")
def get_teams():
    get_teams_query = """
    SELECT * FROM Teams
    """
    data = db.call_database(get_teams_query)
    team = []
    for element in data:
        id, teams, location, short = element
        team.append(Teams(id=id, teams=teams, location=location, short=short))
    print(data)
    return team

@app.get("/teams/{id}")
def get_teams(id: int):
    return "Returns only the id " + str(id)

@app.post("/add_teams")
def add_teams(teams: Teams):
    insert_query = """
    INSERT INTO Teams (teams, location, short)
    VALUES ( ?, ?, ? )
    """
    db.call_database(insert_query, teams.teams, teams.location, teams.short)
    return "Adds a team"

@app.delete("/delete_teams/{id}")
def delete_teams(id: int):
    delete_query = """
    DELETE FROM Teams WHERE id = ?
    """
    db.call_database(delete_query, id)
    return True

@app.put("/update_teams/{id}")
def update_teams(id: int, new_teams: Teams):
    update_teams_query = """
    UPDATE Teams SET teams = ?, location = ?, short = ?
    WHERE id = ?
    """
    db.call_database(update_teams_query, new_teams.teams, new_teams.location, new_teams.short, id)
    return True


@app.get("/players")
def get_players():
    get_players_query = """
    SELECT * FROM Players
    """
    data = db.call_database(get_players_query)
    players = []
    for element in data:
        id, first_name, last_name, age, team_id = element
        players.append(Players(id=id, first_name=first_name, last_name=last_name, age=age))
    print(data)
    return players

@app.get("/players/{id}")
def get_players(id: int):
    return "Returns only the id " + str(id)

@app.post("/add_players")
def add_players(players: Players):
    print(players)
    insert_query2 = """
    INSERT INTO Players (first_name, last_name, age)
    VALUES ( ?, ?, ? )
    """
    db.call_database(insert_query2, players.first_name, players.last_name, players.age)
    return "Adds a player"

@app.delete("/delete_players/{id}")
def delete_players(id: int):
    delete_query = """
    DELETE FROM Players WHERE id = ?
    """
    db.call_database(delete_query, id)
    return True

@app.put("/update_players/{id}")
def update_players(id: int, new_players: Players):
    update_players_query = """
    UPDATE Players SET first_name = ?, last_name = ?, age = ?
    WHERE id = ?
    """
    db.call_database(update_players_query, new_players.first_name, new_players.last_name, new_players.age, id)
    return True

@app.post("/assign_teams")
def assign_teams():
    teams = db.call_database("SELECT * FROM Teams")
    if not teams:
        raise HTTPException(status_code=404, detail="No teams found in the database.")
    
    players = db.call_database("SELECT * FROM Players")
    if not players:
        raise HTTPException(status_code=404, detail="No players found in the database.")
    
    random.shuffle(teams)
    team_index = 0

    for player in players:
        assigned_team = teams[team_index]
        db.call_database("UPDATE Players SET team_id = ? WHERE id = ?", assigned_team[0], player[0])
        
        team_index += 1
        if team_index >= len(teams):
            team_index = 0
    
    return {"The players got a team!"}