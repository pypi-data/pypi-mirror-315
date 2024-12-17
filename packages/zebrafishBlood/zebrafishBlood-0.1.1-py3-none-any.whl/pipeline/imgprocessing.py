import openslide
import cv2
from PIL import Image
import numpy as np

# dimensions() returns width and height of image in integer
# cutimg() cuts one single tile at a specified location of ndpi image; return PIL image
# saveimg() saves image in png format; returns path of image

def dimensions(PATH):
    slide = openslide.OpenSlide(PATH)

    width = slide.dimensions[0]
    height = slide.dimensions[1]

    slide.close()
    return width, height

def cutimg(PATH, x, y, IMGSZ):
    slide = openslide.OpenSlide(PATH)
    tile = slide.read_region((x, y), 0, (IMGSZ, IMGSZ))
    slide.close()
    return tile

def saveimg(PATH, image, x, y):
    path = PATH + f'/tile_{x}_{y}.png'
    image = image.convert("RGB")
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, image)
    return path