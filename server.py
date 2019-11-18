# uwsgi --socket :9000 --wsgi-file server.py
import pandas as pd
from urllib import parse

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    query = dict(parse.parse_qsl(env['QUERY_STRING']))
    players = pd.read_csv('data.csv')
    players.rename(columns={'Unnamed: 0':''}, inplace=True)
    if 'age' in query:
        players_filtered = players[players.Age.isin(query['age'].split(','))]
        return [players_filtered.to_json(orient='records').encode()]
    else:
        return []