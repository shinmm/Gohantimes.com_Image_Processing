import os
import shutil
import sys
import time,datetime
from PIL import Image

from ProcessImage_Helper import resizeImageTest, addWatermark

START_TIME = time.clock()
#edited for testing conc
print("Running...")
#.txt file to log processing information
process_log = open("PROCESS_LOG",'w')
process_log.write("Program start time {}\n\n".format(datetime.datetime.now()))

# create new directory to store resized food photos
try:
    root_dir = os.getcwd()  # Path to main root folder
    food_dir = os.getcwd() + "/test_food_images"  # Path to food directory
    resize_food_dir = root_dir + "/food_img_PROCESSED"
    if (not os.path.isdir(resize_food_dir)):
        process_log.write("Creating new directory {}\n".format(resize_food_dir))
        os.mkdir(resize_food_dir)
    else:
        process_log.write("Resize folder Already exists!\n")
        process_log.write("Creating and deleting new directory\n")
        shutil.rmtree(resize_food_dir)
        os.mkdir(resize_food_dir)
    # change current working directory to food folder
    os.chdir(food_dir)
except FileNotFoundError:
    process_log.write("Directory was not found\n")
    sys.exit()


food_count = 0  # number of items in directory

# loop through images in food folder to process
try:
    for filename in os.listdir(os.getcwd()):
        try:

            image_curr = Image.open(filename)
            #Check image rotation and correct it if necessary
            if hasattr(image_curr, '_getexif'):
                orientation = 0x0112
                exif = image_curr._getexif()
                if exif is not None:
                    orientation = exif[orientation]
                    rotations = {
                        3: Image.ROTATE_180,
                        6: Image.ROTATE_270,
                        8: Image.ROTATE_90
                    }
                    if orientation in rotations:
                        image_curr = image_curr.transpose(rotations[orientation])

            process_log.write("\nFile Being Edited : {}\n".format(filename))
            process_log.write("Original Photo Size : {} pixels(width) and {} pixels(height)\n"
                              .format(image_curr.size[0],image_curr.size[1]))
            # resize image
            image_curr = resizeImageTest(image_curr)

            process_log.write("Resized Photo Size : {} pixels(width) and {} pixels(height)\n"
                              .format(image_curr.size[0], image_curr.size[1]))


            # add watermark
            addWatermark(image_curr)

            filename = filename[:-4]
            resize_filename = filename + '-resized.jpg'

            process_log.write("File renamed to : {}\n".format(resize_filename))

            image_curr.save(resize_food_dir + '/' + resize_filename, optimize=True, quality=80)

            del image_curr  # reset image_curr object
        except FileNotFoundError:
            process_log.write("File Was not found!\n")
        food_count += 1
    print("Total number of images processed" + food_count)
except KeyboardInterrupt:
    process_log.write("Program was stopped prematurely\n")
    print("Program was stopped prematurely\n")

# Total runtime of the program
process_log.write("The program took {} seconds!\n".format(time.clock() - START_TIME))

print("Program executed")