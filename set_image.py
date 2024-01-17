import time

import PIL.Image
from PIL import Image
import os

def create_image_set(img_dir,img_name):
    start = time.time()
    thumb = 30,30
    small = 540,540
    medium = 768, 768
    large = 1080, 1080
    xl = 1200, 1200

    image = Image.open(os.path.join(img_dir,img_name))
    image_name = img_name.split('.')[0]
    image_extension = img_name.split('.')[-1]
    # for webp
    webp_img = image.copy()
    fixed_height = 1000
    height_percent = (fixed_height/float(webp_img.size[1]))
    # ensure all images are same size
    width_size = int(float(webp_img.size[0])*float(height_percent))
    webp_img = webp_img.resize((width_size,fixed_height), PIL.Image.NEAREST)
    webp_img.save(f"{os.path.join(img_dir, image_name)}.webp",'webp', optimize=True, quality=99)

    end = time.time()
    time_elapsed = end - start
    print(f"Task complete in {time_elapsed}")
