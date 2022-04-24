import arcpy
from src.menu import Menu


arcpy.AddMessage("Booting...")

mainMenu = Menu()
while mainMenu.done is False:
    mainMenu.display()
    mainMenu.handle_input()

arcpy.AddMessage("Exiting...")










