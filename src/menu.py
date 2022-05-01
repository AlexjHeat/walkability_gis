import arcgisscripting
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
        self.score_raster = ""

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
        name_valid = False
        while name_valid is False:
            try:
                name = raw_input("City name: ")
                city = City(name)
            except WindowsError:
                print "Name already taken, please choose another."
                continue
            name_valid = True
        # Waits for user to input a valid spatial reference
        # LA = GCS WGS 1984
        sr_valid = False
        while sr_valid is False:
            # TODO sr = raw_input("Enter in the spatial reference: ")
            sr = ("Sinusoidal (world)")
            sr_valid = city.set_spatial_reference(sr)

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
                fc_valid = False
                while fc_valid is False:
                    try:
                        fc = raw_input("Input the name of the feature class (without extension): ")
                        city.add_feature_class(fc)
                    except arcgisscripting.ExecuteError:
                        print("Feature class not found")
                        continue
                    fc_valid = True

            elif option == 2:
                city.combine_feature_classes()
                city.save()
                break

            else:
                print("Invalid option")
                continue


    def view_city(self):
        pass

