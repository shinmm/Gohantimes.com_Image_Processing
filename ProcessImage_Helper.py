from PIL import Image,ImageDraw,ImageFont
import PIL

FONT_PATH = "/Users/shinmitsuno/Desktop/Gohantimes_Image_Processing/Pacifico.ttf"
PIC_WIDTH = 1450;

#Takes the image object passed in an argument and add a grey watermark
#on the bottom right corner (Website URL)
def addWatermark(curr_img):
    # add watermark
    draw = ImageDraw.Draw(curr_img)
    font = ImageFont.truetype(
        FONT_PATH, 43)
    width, height = curr_img.size
    #x, y = (width - 200, height - 100)
    xx, yy = (width - 315, height - 78)

    text = "Gohantimes.com"
    #w, h = font.getsize(text)

    draw.text((xx, yy), text, fill=(211, 211, 211, 100), font=font)  # draw transparant text

def resizeImage(curr_img):
    width, height = curr_img.size
    wpercent = (PIC_WIDTH / float(width))
    hsize = int((float(height) * float(wpercent)))
    curr_img = curr_img.resize((PIC_WIDTH, hsize), PIL.Image.ANTIALIAS)
    return curr_img


def resizeImageTest(curr_img):

    width, height = curr_img.size
    #print((int)(width), (int)(height), end=" Is the width and height\n")

    curr_img = curr_img.resize(((int)(width/2.7), (int)(height/2.7)), PIL.Image.ANTIALIAS)
    #print((int)(width/2.7), (int)(height/2.7), end=" Is the new width and height\n")
    return curr_img
