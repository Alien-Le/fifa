import sys
import pandas as pd
import pymysql
import argparse
from pymysql.cursors import DictCursor
from contextlib import closing

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('--config_path', action="store", dest="config_path", default='/srv/alien')
args = parser.parse_args()

sys.path.append(args.config_path)

import config


dbname = config.MYSQL['db']
config.MYSQL['db']  = ''
with closing(pymysql.connect(**config.MYSQL)) as connection:
    with connection.cursor(DictCursor) as cursor:
        cursor.execute('CREATE DATABASE IF NOT EXISTS ' + dbname)
config.MYSQL['db']  = dbname


players = pd.read_csv('data.csv')
nationalities = list(players['Nationality'].unique())
clubs = [club for club in list(players['Club'].unique()) if str(club) != 'nan']

group = players.sort_values(['Age', 'Unnamed: 0'], ascending=[True, True]).groupby('Age')
players['position_in_sprite'] = group.cumcount()

with closing(pymysql.connect(**config.MYSQL)) as connection:
    with connection.cursor(DictCursor) as cursor:
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS nationality (
            nationality_id INT(11) NOT NULL AUTO_INCREMENT,
            nationality VARCHAR(255) NOT NULL,
            PRIMARY KEY (nationality_id),
            UNIQUE KEY (nationality)
        )  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci''')
        cursor.execute('INSERT IGNORE INTO nationality (nationality) VALUES ' + ', '.join(['(%s)'] * len(nationalities)), nationalities)
        cursor.execute('SELECT * FROM nationality')
        db_nationalities = {}
        for db_nationality in cursor.fetchall():
            db_nationalities[db_nationality['nationality']] = db_nationality['nationality_id']
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS club (
            club_id INT(11) NOT NULL AUTO_INCREMENT,
            club VARCHAR(255) NOT NULL,
            PRIMARY KEY (club_id),
            UNIQUE KEY (club)
        )  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci''')
        cursor.execute('INSERT IGNORE INTO club (club) VALUES ' + ', '.join(['(%s)'] * len(clubs)), clubs)
        cursor.execute('SELECT * FROM club')
        db_clubs = {}
        for db_club in cursor.fetchall():
            db_clubs[db_club['club']] = db_club['club_id']
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            player_id INT(11) NOT NULL AUTO_INCREMENT,
            name VARCHAR(255) NOT NULL,
            age TINYINT(4) NOT NULL,
            external_id INT(11) NOT NULL,
            wage INT(11) NOT NULL,
            overall_rate TINYINT(4) NOT NULL,
            club_id INT(11) DEFAULT NULL,
            nationality_id INT(11) NOT NULL,
            position_in_sprite INT(11) NOT NULL,
            PRIMARY KEY (player_id),
            UNIQUE KEY (external_id),
            KEY age (age),
            CONSTRAINT fk__player_nationality FOREIGN KEY (nationality_id) REFERENCES nationality (nationality_id) ON DELETE CASCADE ON UPDATE CASCADE,
            CONSTRAINT fk__player_club FOREIGN KEY (club_id) REFERENCES club (club_id) ON DELETE CASCADE ON UPDATE CASCADE
        )  ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci''')
        players_data = []
        for idx, player in players.iterrows():
            players_data.append(player['Name'])
            players_data.append(player['Age'])
            players_data.append(player['ID'])
            players_data.append(player['Wage'].replace('€', '').replace('K', ''))
            players_data.append(player['Overall'])
            if str(player['Club']) != 'nan':
                players_data.append(db_clubs[player['Club']])
            else:
                players_data.append(None)
            players_data.append(db_nationalities[player['Nationality']])
            players_data.append(player['position_in_sprite'])
        cursor.execute('''
        INSERT IGNORE INTO player (name, age, external_id, wage, overall_rate, club_id, nationality_id, position_in_sprite)
        VALUES ''' + ', '.join(['(%s, %s, %s, %s, %s, %s, %s, %s)'] * len(players)), players_data)
