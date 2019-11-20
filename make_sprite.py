import csv
import logging
import os
import math
from PIL import Image

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

max_frames_row = 100

size = 36, 36

files = os.listdir("player_photos/")
files.sort()

files.remove('notfound.png')

logging.info('use %s files' % len(files))

images_by_age = {}

with open('data.csv', newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for csv_row in csv_reader:
        if csv_row['Age'] not in images_by_age:
            images_by_age[csv_row['Age']] = []
        images_by_age[csv_row['Age']].append(csv_row['\ufeff'])

for age, images in images_by_age.items():
    print(age)

    frames = []
    tile_width = 0
    tile_height = 0
    spritesheet_width = 0
    spritesheet_height = 0

    for image in images:
        try:
            with Image.open("player_photos/%s.png" % image) as im:
                if size is not None:
                    im.thumbnail(size, Image.ANTIALIAS)
                frames.append(im.getdata())
        except Exception:
            with Image.open("player_photos/notfound.png") as im:
                if size is not None:
                    im.thumbnail(size, Image.ANTIALIAS)
                frames.append(im.getdata())
            # logging.warning("%s.png is not a valid image" % image)

    tile_width = frames[0].size[0]
    tile_height = frames[0].size[1]

    if len(frames) > max_frames_row:
        spritesheet_width = tile_width * max_frames_row
        required_rows = math.ceil(len(frames) / max_frames_row)
        spritesheet_height = tile_height * required_rows
    else:
        spritesheet_width = tile_width * len(frames)
        spritesheet_height = tile_height

    print(spritesheet_height)
    print(spritesheet_width)

    spritesheet = Image.new("RGBA", (int(spritesheet_width), int(spritesheet_height)))

    for current_frame in frames:
        top = tile_height * math.floor((frames.index(current_frame)) / max_frames_row)
        left = tile_width * (frames.index(current_frame) % max_frames_row)
        bottom = top + tile_height
        right = left + tile_width

        box = (left, top, right, bottom)
        box = [int(i) for i in box]
        cut_frame = current_frame.crop((0, 0, tile_width, tile_height))

        spritesheet.paste(cut_frame, box)

    spritesheet.save("sprites/sprite-%s.png" % age, "PNG")
