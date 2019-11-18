# uwsgi --socket :9000 --wsgi-file server.py
import sys
import pandas as pd
import pymysql
import json
from urllib import parse
from pymysql.cursors import DictCursor
from contextlib import closing


sys.path.append('/srv/alien')

import config

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    res = []
    query = dict(parse.parse_qsl(env['QUERY_STRING']))
    if 'age' in query:
        # players = pd.read_csv('data.csv')
        # players.rename(columns={'Unnamed: 0':''}, inplace=True)
        # players_filtered = players[players.Age.isin(query['age'].split(','))]
        # return [players_filtered.to_json(orient='records').encode()]

        ages = query['age'].split(',')
        with closing(pymysql.connect(**config.MYSQL)) as connection:
            with connection.cursor(DictCursor) as cursor:
                cursor.execute('''
                SELECT
                    wage AS Wage,
                    position_in_sprite AS Pos,
                    age as Age,
                    overall_rate as Overall,
                    external_id as ID
                FROM player
                LEFT JOIN nationality USING(nationality_id)
                LEFT JOIN club USING (club_id)
                WHERE age IN(''' + ', '.join(['%s'] * len(ages)) + ''')
                ORDER BY Wage ASC''', ages)
                res = cursor.fetchall()
                ''',
                    name as Name,
                    club as Club,
                    nationality as Nationality'''

        res.append(json.dumps(res).encode())

    return res
