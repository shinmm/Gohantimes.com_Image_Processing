import os
import shutil
import glob
import sys
import timeit
import multiprocessing

from multiprocessing import Pool
from PIL import Image
from ProcessImage_Helper import resizeImageTest, addWatermark

START_TIME = timeit.default_timer()
print(START_TIME)
def proccess_image(filename):
    try:

        image_curr = Image.open(filename)
        # Check image rotation and correct it if necessary
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

        print("File Being Edited : {}\n".format(filename))
        print("Original Photo Size : {} pixels(width) and {} pixels(height)\n"
                          .format(image_curr.size[0], image_curr.size[1]))
        # resize image
        image_curr = resizeImageTest(image_curr)

        print("Resized Photo Size : {} pixels(width) and {} pixels(height)\n"
                          .format(image_curr.size[0], image_curr.size[1]))

        # add watermark
        addWatermark(image_curr)

        filename = filename[:-4]
        resize_filename = filename + '-resized.jpg'

        print("File renamed to : {}\n".format(resize_filename))

        image_curr.save(resize_food_dir + '/' + resize_filename, optimize=True, quality=80)
        return image_curr

    except FileNotFoundError:
        print("File Was not found!\n")


#edited for testing conc
print("Running...")
#.txt file to log processing information



# create new directory to store resized food photos
try:
    root_dir = os.getcwd()  # Path to main root folder
    food_dir = os.getcwd() + "/test_food_images"  # Path to food directory
    resize_food_dir = root_dir + "/food_img_PROCESSED"
    if (not os.path.isdir(resize_food_dir)):
        print("Creating new directory {}\n".format(resize_food_dir))
        os.mkdir(resize_food_dir)
    else:
        print("Resize folder Already exists!\n")
        print("Creating and deleting new directory\n")
        shutil.rmtree(resize_food_dir)
        os.mkdir(resize_food_dir)
    # change current working directory to food folder
    os.chdir(food_dir)

except FileNotFoundError:
    print("Directory was not found\n")
    sys.exit()

# loop through images in food folder to process
try:
    # save list of filenames
    #processes = []
    food_image_files = glob.glob("*.jpg")
    pool = multiprocessing.Pool()
    pool.map(proccess_image, food_image_files)
    pool.close()
    # for file in food_image_files:
    #     p = multiprocessing.Process(target=proccess_image, args=(file,))
    #     processes.append(p)
    #     p.start()
    #
    # for process in processes:
    #     process.join()
#
except KeyboardInterrupt:
    print("Program was stopped prematurely\n")

# Total runtime of the program
print("The program took {} seconds!\n".format(timeit.default_timer() - START_TIME))

print("Program executed")
