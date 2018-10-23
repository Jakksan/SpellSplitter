import os
from PIL import Image
import pytesseract
import platform

# pytesseract.pytesseract.tesseract_cmd = pytesseract_location

operating_system = platform.system()

if  operating_system == "Windows":
    print("Your OS sucks amigo. G3t mor l33t. ")
    pytesseract_location = r"C:\Program Files (x86)\Tesseract-OCR\tesseract"

elif operating_system == "Darwin":
    print("At least you aren't using Windows...")
    print("If you run into errors related to Tesseract, make sure you've run 'brew install tesseract' and possibly 'pip3 install pytesseract.' ")

elif operating_system == "Linux":
    print("You are the superior human being. Please enjoy this program and use it to it's fullest potential. ")


# Folder to look in
folder = "Paladin_Spells"

# List of all the image names in the folder
images = os.listdir("./"+folder)

# File is .DS_Store, remove it from the pic_list array
if images[0] == ".DS_Store":
    images.remove(".DS_Store")

try:
    os.makedirs("./" + folder + "_Finished")
except:
    print(folder + "_Finished already exists. Please delete the folder to continue")

# Do the following for each image
for image in images:
    single_card = [20, 20, 520, 720] # (left, upper, right, lower)
    single_name = [50, 40, 480, 90]
    new_cards = []
    new_names = []

    # finds the coordinated of the 9 cards and card names and puts them into separate lists
    for count in range(9):
        column = int(count/3)
        row = count % 3
        new_cards.append(((single_card[0] + row*500 + row*2), (single_card[1] + column*700 + column*2), (single_card[2] + row*500 + row*2), (single_card[3] + column*700 + column*2)))
        new_names.append(((single_name[0] + row*500 + row), (single_name[1] + column*700 + column), (single_name[2] + row*500 + row), (single_name[3] + column*700 + column)))

    #print(new_cards)
    spell_page = ("./"+folder+"/"+image)
    # print(spell_page)

    spell_page = Image.open(spell_page)

    card_images = []
    card_names = []

    for i in range(len((new_cards))):
        card_images.append(spell_page.crop(new_cards[i]))
        spell_page.crop(new_names[i]).save("temp.bmp")
        file_name = pytesseract.image_to_string("temp.bmp")
        # print(file_name)
        file_name = file_name + ".png"
        file_name = file_name.replace("/", "^")

        card_images[i].save("./"+ folder + "_Finished/" + file_name, "PNG")
