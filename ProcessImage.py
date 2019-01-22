import os
import shutil
import glob
import sys
import timeit
import multiprocessing
from multiprocessing import Pool
from PIL import Image
from ProcessImage_Helper import resizeImage, addWatermark

root_dir = ""
resize_food_dir = ""
font_path = ""

START_TIME = timeit.default_timer() #For program run time


#This function is to be run by multiple processors
#It will rotate, resize and water each image in the food directory
def proccess_image(filename):
    global resize_food_dir
    global font_path
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

        # print("File Being Edited : {}\n".format(filename))
        # print("Original Photo Size : {} pixels(width) and {} pixels(height)\n"
        #                   .format(image_curr.size[0], image_curr.size[1]))
        # # resize image
        image_curr = resizeImage(image_curr)

        # print("Resized Photo Size : {} pixels(width) and {} pixels(height)\n"
        #                   .format(image_curr.size[0], image_curr.size[1]))

        # add watermark
        addWatermark(image_curr, font_path)

        filename = filename[:-4]
        resize_filename = filename + '-resized.jpg'

        # print("File renamed to : {}\n".format(resize_filename))
        image_curr.save(resize_food_dir + '/' + resize_filename, optimize=True, quality=80)
        return image_curr

    except FileNotFoundError:
        print("File Was not found!\n")

# This function will create a new directory to store the processed image
#If there is an existing directory, it will first delete is and create a new one
def createNewDirectory():
    # create new directory to store resized food photos
    global resize_food_dir
    try:
        food_dir = root_dir + "/test_food_images"  # Path to food directory
        resize_food_dir = root_dir + "/food_img_PROCESSED"
        if (not os.path.isdir(resize_food_dir)):
            # print("Creating new directory {}\n".format(resize_food_dir))
            os.mkdir(resize_food_dir)
        else:
            # print("Resize folder Already exists!\n")
            # print("Creating and deleting new directory\n")
            shutil.rmtree(resize_food_dir)
            os.mkdir(resize_food_dir)
        # change current working directory to food folder
        os.chdir(food_dir)


    except FileNotFoundError:
        print("Directory was not found\n")
        sys.exit()

# This function will search the current directory for a font file.
# More specifically, it will look for a .ttf file and store its file path
# in the global variable font_path
def searchFont():
    global font_path
    print("Searching for font")
    font_path = os.path.join(root_dir, "Pacifico.ttf")
    return font_path


#main function to run full script
def main():
    global root_dir
    root_dir = os.path.dirname(__file__) #set global variable with root directory path

    #Create new directory to store processed .jpg files
    createNewDirectory()
    #Seach for font file
    searchFont()

    # loop through images in food folder to process
    try:
        # save list of filenames
        #threads = []
        food_image_files = glob.glob("*.jpg")
        pool = multiprocessing.Pool(4)
        pool.map(proccess_image, food_image_files)

        pool.close()

    except KeyboardInterrupt:
        print("Program was stopped prematurely\n")

    # Total runtime of the program
    print("The program took {} seconds!\n".format(timeit.default_timer() - START_TIME))


#run main
main()