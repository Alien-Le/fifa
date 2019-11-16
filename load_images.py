import csv
import logging
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from PIL import Image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

req = Request('https://cdn.sofifa.org/players/4/notfound_0.png', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req)
img = Image.open(webpage)
img.save("player_photos/notfound.png")

'''
with open('data.csv', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for csv_row in csv_reader:
        req = Request(csv_row['Photo'], headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req)
            img = Image.open(webpage)
            img.save("player_photos/%s.png" % csv_row['\ufeff'])
            logging.info('save: %s' % csv_row['Photo'])
        except HTTPError:
            logging.info('skip: %s (404)' % csv_row['Photo'])
'''