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

# for i in range(len(spell_list)):
#     print(spell_names[i])

# Do the following for each image
i = 0


while i < len(images):
    for image in images:
        if int(image[19:21]) == i+1:
            single_card = [20, 20, 520, 720] # (left, upper, right, lower)
            new_cards = []
            for count in range(9):
                column = int(count/3)
                row = count % 3
                new_cards.append(((single_card[0] + row*500+row), (single_card[1] + column*700+ column), (single_card[2] + row*500 + row), (single_card[3] + column*700 + column)))

            # print(new_cards)
            spell_page = ("./"+folder+"/"+image)
            # print(spell_page)

            spell_page = Image.open(spell_page)

            card_images = []
            for j in range(len((new_cards))):
                card_images.append(spell_page.crop(new_cards[j]))
                # card_images[i].show()
                print(spell_names[9*i+j])
            i = i + 1
