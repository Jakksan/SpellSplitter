import os
from PIL import Image
import csv

# Folder to look in
folder = "Paladin_Spells"

# List of all the image names in the folder
images = os.listdir("./"+folder)

# File is .DS_Store, remove it from the pic_list array
if images[0] == ".DS_Store":
    images.remove(".DS_Store")


# Get the name of each card in the csv
with open('paladin.csv', 'r') as csvfile:
  spell_names = []

  csvReader = csv.reader(csvfile, delimiter=";")
  spell_list = list(csvReader)

  for row in spell_list:
        spell_name = row[1]

        spell_names.append(spell_name)


for i in range(len(spell_list)):
    print(spell_names[i])

# Do the following for each image
i = 0
while i < len(images):
    for image in images:

        if int(image[19:21]) == i+1:
            card_row = (20, 20, 1504, 720) # row of cards
            single_card = (20, 20, 520, 720) # size of a single card (left, upper, right, lower)
            spell_page = ("./"+folder+"/"+image)
            print(spell_page)

            spell_page = Image.open(spell_page)
            single_card = spell_page.crop(single_card)

            # spell_page.show()
            single_card.show()
            i = i + 1
