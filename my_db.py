import sqlite3
import os
import json


class FootballDatabase:
    db_url: str

    def __init__(self, db_url: str):
        self.db_url = db_url

        if not os.path.exists(self.db_url):
            self.init_db()

    def call_database(self, query, *args):
        conn = sqlite3.connect(self.db_url)
        cur = conn.cursor()
        cur.execute(query, args)
        data = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return data

    def init_db(self):
        init_db_query = """
        CREATE TABLE IF NOT EXISTS Teams (
            id INTEGER PRIMARY KEY NOT NULL,
            teams TEXT NOT NULL,
            location TEXT NOT NULL,
            short TEXT NOT NULL
        ); """
        init_db_query2 = """
        CREATE TABLE IF NOT EXISTS Players (
            id INTEGER PRIMARY KEY NOT NULL,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            age INTEGER,
            team_id INTEGER
        );
        """
        insert_query = """
        INSERT INTO Teams (teams, location, short)
        VALUES ('teams', 'location', 'short');
        """
        insert_query2 = """
        INSERT INTO Players (first_name, last_name, age)
        VALUES ('first_name', 'last_name', '1');
        """
        

        self.call_database(init_db_query)
        self.call_database(init_db_query2)
        self.call_database(insert_query)
        self.call_database(insert_query2)