# uwsgi --socket :9000 --wsgi-file server.py
import sys
import pymysql
import json
import argparse
from urllib import parse
from pymysql.cursors import DictCursor
from contextlib import closing

parser = argparse.ArgumentParser(description='Short sample app')
parser.add_argument('--config_path', action="store", dest="config_path", default='/srv/alien')
args = parser.parse_args()

sys.path.append(args.config_path)

import config  # NOQA


def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    res = []
    query = dict(parse.parse_qsl(env['QUERY_STRING']))
    if 'age' in query:
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
