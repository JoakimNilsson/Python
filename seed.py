import json
from my_db import FootballDatabase

db = FootballDatabase("FootballDatabase.db")

create_teams = """
INSERT INTO Teams (
    teams,
    location,
    short
) VALUES (
    ?,?,?
)
"""
create_players = """
INSERT INTO Players (
    first_name,
    last_name,
    age
) VALUES (
    ?,?,?
)
"""

with open("seed.json", "r") as seed:
            data = json.load(seed)

            for Teams in data["Teams"]:
                db.call_database(create_teams, Teams["teams"], Teams["location"], Teams["short"])

            for Players in data["Players"]:
                db.call_database(create_players, Players["first_name"], Players["last_name"], Players["age"])