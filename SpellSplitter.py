import os
from PIL import Image

# Folder to look in
folder = "Paladin_Spells"

# List of all the image names in the folder
images = os.listdir("./"+folder)

# File is .DS_Store, remove it from the pic_list array
if images[0] == ".DS_Store":
    images.remove(".DS_Store")

# Do the following for each image
for image in images:
    single_card = [20, 20, 520, 720] # (left, upper, right, lower)
    new_cards = []
    for count in range(9):
        column = int(count/3)
        row = count % 3
        new_cards.append(((single_card[0] + row*500), (single_card[1] + column*700), (single_card[2] + row*500), (single_card[3] + column*700)))

    print(new_cards)
    spell_page = ("./"+folder+"/"+image)
    print(spell_page)

    spell_page = Image.open(spell_page)

    card_images = []
    for i in range(len((new_cards))):
        card_images.append(spell_page.crop(new_cards[i]))
        card_images[i].show()

    # spell_page.show()
    # single_card.show()
