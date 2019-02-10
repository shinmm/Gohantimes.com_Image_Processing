from PIL import Image,ImageDraw,ImageFont
import PIL

PIC_WIDTH = 1450;

#Takes the image object passed in an argument and add a grey watermark
#on the bottom right corner (Website URL)
#Caters to various fonts
def addWatermark(curr_img, font_name):
    # add watermark
    draw = ImageDraw.Draw(curr_img)
    text = "Gohantimes.com"

    fontsize = 1  # starting font size
    # portion of image width you want text width to be
    img_fraction = 0.30

    font = ImageFont.truetype(
        font_name, fontsize)
    while font.getsize(text)[0] < img_fraction * curr_img.size[0]:
        # iterate until the text size is just larger than the criteria
        fontsize += 1
        font = ImageFont.truetype(font_name, fontsize)

    width, height = curr_img.size
    text_w, text_h = draw.textsize(text, font)
    xx, yy = (width - text_w, height - text_h) #dynamic placement of text

    #w, h = font.getsize(text)

    draw.text((xx, yy), text, fill=(130, 130, 130, 100), font=font)  # draw transparant text


#Resize image to about 1/3 of the size to about 1500 px width
def resizeImage(curr_img):

    width, height = curr_img.size
    #print((int)(width), (int)(height), end=" Is the width and height\n")

    curr_img = curr_img.resize(((int)(width/2.7), (int)(height/2.7)), PIL.Image.ANTIALIAS)
    #print((int)(width/2.7), (int)(height/2.7), end=" Is the new width and height\n")
    return curr_img

