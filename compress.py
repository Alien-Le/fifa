from PIL import Image

sprite = Image.open('sprite.png')
sprite.save('sprite-compressed.png', "PNG", optimize = True)