from PIL import Image
import os

new_height = 100
d = os.path.dirname(__file__)
content_path = d + '\\shop_cite\\static\\shop_cite\\assets\\img\\content\\category'
dir_list = os.listdir(content_path)
for file_name in dir_list:
    print(file_name)
    image = Image.open(content_path + '\\' + file_name)
    width, height = image.size
    new_width = int(width/(height/new_height))
    new_image = image.resize((new_width, new_height))
    try:
        new_image.save(content_path + '\\' + file_name)
    except OSError:
        new_image.save(content_path + '\\' + file_name, format='PNG')
