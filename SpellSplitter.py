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
    single_card = (20, 20, 520, 720) # (left, upper, right, lower)
    spell_page = ("./"+folder+"/"+image)
    print(spell_page)

    spell_page = Image.open(spell_page)
    single_card = spell_page.crop(single_card)

    # spell_page.show()
    single_card.show()
