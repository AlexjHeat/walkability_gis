import arcpy
from city import City

class Menu:
    # TODO change options from list to dict
    def __init__(self):
        self.done = False
        self.options = ['Exit',
                        'Add New City',
                        'View City',
                        'Edit City',
                        'Remove City']


    def display(self):
        print "Please select one of the following: "
        for i in range(len(self.options)):
            print '\t', i+1, '\t', self.options[i]

    def handle_input(self):
        choice = input()
        if choice == 1:
            self.done = True
        elif choice == 2:
            self.add_city()
        elif choice == 3:
            self.view_city()
        else:
            print("Invalid option")

    def add_city(self):
        print("\n// ADDING NEW CITY //")
        name = input("City name: ")
        city = City(name)

        while True:
            print "\n// ADDING NEW CITY:", city.name, "//"
            print "Please select one of the following: "
            print "\t1\tAdd a new feature class"
            print "\t2\tDone"
            print "\t0\tCancel"

            option = input()
            if option == 0:
                # TODO clean up, delete necessary files, city.cancel() or somethin
                pass
            elif option == 1:
                # TODO let users grab file from directory
                fc = input("Input the name of the feature class: ")
                city.add_feature_class(fc)
            elif option == 2:
                break
            else:
                print("Invalid option")
                continue

    def view_city(self):
        pass

