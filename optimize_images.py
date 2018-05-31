import sys
from PIL import Image
import os

def main():
  imgsrc = sys.argv[1]
  path = sys.argv[2]
  # create directory if it doesn't exist
  imgext,imgname = imgsrc[::-1].split(".",1)
  imgname = (imgname.split("/",1)[0])[::-1]
  imgext = imgext[::-1]
  basewidths = [512,192,64,48]
  img = Image.open(imgsrc)
  for x in range(0,len(basewidths)):
    wpercent = (basewidths[x]/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    new_img = img.resize((basewidths[x],hsize), Image.ANTIALIAS)
    new_name = imgname + '_' + str(basewidths[x]) + '.' + imgext
    if imgext == "jpg":
      new_img.save(path + new_name,quality=40)
    else:
      new_img.save(path + new_name)
main()
