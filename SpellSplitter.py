import os # used to create and read files and directories in the OS
from PIL import Image # used to interact with the images in the something_Spells folder
import pytesseract # used for finding card names using optical character recognition (OCR)
import csv # used to easily sort through csv file
import platform # used for determining operating system
from fuzzywuzzy import fuzz # used to match OCR names to the CSV names



################################################################################
# Determine OS
operating_system = platform.system()

if  operating_system == "Windows":
    print("Your OS sucks amigo. G3t mor l33t. ")
    pytesseract_location = r"C:\Program Files (x86)\Tesseract-OCR\tesseract"

elif operating_system == "Darwin":
    print("At least you aren't using Windows...")
    print("If you run into errors related to Tesseract, make sure you've run 'brew install tesseract' and possibly 'pip3 install pytesseract.' ")

elif operating_system == "Linux":
    print("You are the superior human being. Please enjoy this program and use it to it's fullest potential. ")


################################################################################
# Look into the working directory and make any nessessary changes

# Folder containing untouched images
folder = "Paladin_Spells"

# List of all the image names in the folder
images = os.listdir("./"+folder)
images.sort()

# File is .DS_Store, remove it from the pic_list array
if images[0] == ".DS_Store":
    images.remove(".DS_Store")

# If it's possible to make a new directory (one doesn't already exist with that name), make one to store our edited images
try:
    os.makedirs("./" + folder + "_Finished")
except:
    print(folder + "_Finished already exists. If this creates problems, please delete this folder. ")







################################################################################
# Get needed CSV information

cards = []

# Get the name of each card in the csv, once we match the card to their csv counterpart, we will be able to sort by their characteristics or level
with open('paladin.csv', 'r') as csvfile:
  spell_names = []
  spell_levels = []

  csvReader = csv.reader(csvfile, delimiter=";")
  spell_list = list(csvReader)

  for row in spell_list:
        spell_name = row[1]
        spell_level = row[0]

        spell_names.append(spell_name)
        spell_levels.append(spell_level)



################################################################################
# Pull out the images of each individual card and get it's name using OCR



ocr_names = []
card_images = []

# For each untouched image
for image in images:
    single_card = [20, 20, 520, 720]    # dimensions of a single card
    single_name = [50, 40, 480, 90]     # dimensions of a spell's name box
    new_cards = []
    new_names = []

    # finds the coordinated of the 9 cards and card names and puts them into separate lists
    for count in range(9):
        column = int(count/3)
        row = count % 3
        new_cards.append(((single_card[0] + row*500 + row*2), (single_card[1] + column*700 + column*2), (single_card[2] + row*500 + row*2), (single_card[3] + column*700 + column*2)))
        new_names.append(((single_name[0] + row*500 + row), (single_name[1] + column*700 + column), (single_name[2] + row*500 + row), (single_name[3] + column*700 + column)))


    # Open the spell page image that needs to be worked on
    card_pictures = []

    spell_page = ("./"+folder+"/"+image)
    spell_page = Image.open(spell_page)

    # Use OCR to find the names of each card
    for i in range(len((new_cards))):
        cropped_image = spell_page.crop(new_cards[i])
        card_pictures.append(cropped_image)
        card_images.append(cropped_image)
        print(card_pictures[i])
        spell_page.crop(new_names[i]).save("temp.bmp")
        file_name = pytesseract.image_to_string("temp.bmp")
        ocr_name = file_name.lower()
        file_name = ocr_name + ".png"
        file_name = file_name.replace("/", " of ") # when a '/' is in the file_name, bad things happen

        # add each card name to the ocr_names list, and leave off .png
        characters_in_name = len(file_name)
        ocr_names.append(ocr_name)

        # Save the individual cards to their own folder, using their OCR names
        card_pictures[i].save("./"+ folder + "_Finished/" + file_name, "PNG")


    card_number = 0


    print("Finished page --- " + image)



################################################################################
# Match each ocr name to the csv file information

for ocr_name in ocr_names:
    string_similarity_ratio = 0
    i = 0
    ratios = []
    keep_going = True



    print("\n" + ocr_name)
    print("____________________________")

    while keep_going == True:
        string_similarity_ratio = fuzz.ratio(ocr_name, spell_names[i])
        ratios.append(string_similarity_ratio)


        if (i == len(spell_list) - 1) or (max(ratios) > 75):
            keep_going = False
            # print(i, len(ocr_names), string_similarity_ratio, spell_names[i]) # use for debugging

        i = i + 1


    if max(ratios) < 5:
        print("There was no match for: " + ocr_name)
    else:
        closest_match_val = max(ratios)
        closest_match_index = ratios.index(closest_match_val)

        # Display the program thinks about the matches



        print("OCR name: " + ocr_name)
        print("CSV name: " + spell_names[closest_match_index], "Level " + spell_levels[closest_match_index])
        print("Match confidence: " + str(closest_match_val) + "%")
        print("Length of spell names: " + str(len(spell_names)))
        print("Index Value: " + str(closest_match_index))
        card_number = card_number + 1

        cards.append((closest_match_index, ocr_name, spell_names[closest_match_index], spell_levels[closest_match_index], card_images[closest_match_index]))
# ocr_names = ['daylight', 'dispel magic', 'elemental weapon', 'fear', 'haste', 'hypnotic pattern',
# 'magic circle[1 of 2]', 'magic circle [2 of 2]', 'plant growth',
# 'hold monster', 'holy weapon', 'raise dead', 'scrying [1 of 2]',
# 'scrying [2 of 2]', 'tree stride', 'wallof force', '', '',
# 'animate dead [2 of 2]', 'au ra of vltallty',
# 'beacon of hope', 'bestowcurse [1 of 2]', 'bestow curse [2 of 2]',
# 'bllnding smite', 'counterspell', 'create food and water', "crusader's mantle",
# 'ice storm', 'locate creature', "otiluke's resilient sphere", 'staggering smite',
# 'stoneskin', 'banishing smite', 'circle of power', 'cloudkill', 'commune (ritual)',
# 'aid', 'branding smite', 'calm emotions', 'crown of madness', 'darkness',
# 'findsteed [1 of 2]', 'find steed [2 of 2]', 'hold person', 'lesser resto ration',
# 'locate obj ect', 'magic weapon', 'misty step', 'moonbeam', 'protection from poison',
# 'spiritual weapon', 'warding bond', 'zone oftruth', 'animate dead [1 of 2]',
# 'commune with nature (ritual)', 'contagion [1 of 2]', 'contagion [2 of 2]',
# 'destructive wave', 'dispel eviland good', 'dominate person [1 of 2]', 'dominate person [2 of 2]',
# 'flame strike', 'geas', 'armor of agathys', 'bane', 'bless', 'ceremony(r|tual) [1 of 2]',
# 'ceremony(ritual) [2 of 2]', 'command[1 of 2]', 'command [2 of 2]', 'compelled duel',
# 'cure wounds', 'detect ev] l and good', 'detect magic (ritual)',
# 'detect poison and disease', 'divine favor', 'ensnaring strike',
# 'hellish rebuke', 'heroism', "hunter's mark", 'inflictwounds',
# 'protection from eviland good', 'purify food and drink (ritual)',
# 'sanctuary', 'searing smite', 'shield of faith', 'sleep', 'speak with animals (ritual)',
# 'thunderous smite', 'wrathful smite', 'protection from energy', 'remove curse',
# 'revivify', 'spirit guardians', 'auraof life', 'aura of purity',
# 'banishment', 'blight', 'confusion [1 of 2]', 'confusion [2 of 2]', 'death ward',
# 'dimension door', 'dom | nate beast [1 of 2]', 'dominate beast [2 of 2]',
# 'find greater steed [1 of 2]', 'find greater steed [2 of 2]', 'freedom of movement', 'guardian of faith']
# print(ocr_names)

################################################################################
# Start matching the OCR names to their CSV counterparts




# Note: the values in ocr_names are the OCR names determined earlier
#       the values in spell_names are the CSV names pulled from the .csv file

#
#
# print(cards[0])
# card = cards[0]
# cardpic = card[4]
# cardpic.show()
# print("Total cards matched: " + str(card_number))

print("\n\n____________________________________________________\n")




chosen_cards = []
spell_levels_to_show = []
chosen_level = "ignore me"
chosen_card = "ignore me"


# Find out what level of cards the user wants displayed
while chosen_level != " ":
    try:
        chosen_level = int(input("Which spell levels should be displayed? "))
        spell_levels_to_show.append(chosen_level)
    except:
        chosen_level = " "

print(spell_levels_to_show)


# Find out which cards the user wants to display
while chosen_card != " ":
    card_counter = 0

    for level in spell_levels_to_show:

        print(str(level) + "\n--------------------")

        for card in cards:
            ocr_name = card[2]
            card_level = card[3]

            if int(card_level) == level:
                print(str(card[0])+ ": " + ocr_name, card_level, card[4])

            card_counter = card_counter + 1



    try:
        chosen_card = int(input("Please choose a card from the list: "))
        chosen_cards.append(chosen_card)
    except:
        chosen_card = " "


print(chosen_cards)

# Work in progress, does not always display correct image or output correct card
for card_number in chosen_cards:
    card = cards[int(card_number)]

    card_index_val = card[0]
    card_ocr_name = card[1]
    card_true_name = card[2]
    card_spell_level = card[3]
    card_image = card[4]


    card_image.show()
    print(card_ocr_name, card_true_name, card_spell_level)
