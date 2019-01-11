from PIL import Image,ImageDraw,ImageFont
import PIL

FONT_PATH = "/Users/shinmitsuno/Desktop/Gohantimes.com_Image_Processing/Pacifico.ttf"
PIC_WIDTH = 1450;

#Takes the image object passed in an argument and add a grey watermark
#on the bottom right corner (Website URL)
def addWatermark(curr_img):
    # add watermark
    draw = ImageDraw.Draw(curr_img)
    font = ImageFont.truetype(
        FONT_PATH, 43)
    width, height = curr_img.size
    xx, yy = (width - 300, height - 78)

    text = "Gohantimes.com"
    #w, h = font.getsize(text)

    draw.text((xx, yy), text, fill=(130, 130, 130, 100), font=font)  # draw transparant text


def resizeImageTest(curr_img):

    width, height = curr_img.size
    #print((int)(width), (int)(height), end=" Is the width and height\n")

    curr_img = curr_img.resize(((int)(width/2.7), (int)(height/2.7)), PIL.Image.ANTIALIAS)
    #print((int)(width/2.7), (int)(height/2.7), end=" Is the new width and height\n")
    return curr_img
