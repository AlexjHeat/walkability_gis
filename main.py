from src.menu import Menu


print("Booting...")

mainMenu = Menu()
while mainMenu.done is False:
    mainMenu.display()
    mainMenu.handle_input()

print("Exiting...")

# TODO add clipping
# TODO Figure out how to project spatial reference without breaking raster
# TODO Build GUI
# TODO Figure out better algorithm for computing score
