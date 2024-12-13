from package.subpckg1.PersonalSummary import PersonalSummary
from tabulate import tabulate

class EnergyRequirements(PersonalSummary):
    """
    EnergyRequirements will calculate the client's maintenance calories, based off of their RMR and activity level.
    It will inherit PersonalSummary, as those key metrics are required for the calculations

    """

    def __init__(self):
        #initialize the inheritance
        PersonalSummary.__init__(self)

        self.RMR = 0
        self.TDEE = 0
        self.activitylevel = ""

    def calculate_RMR(self):
        "Calculate client's Resting Metabolic Rate, which is the minimum calories burned at rest"

        if self.gender == "M":
            #RMR equation for males
            self.RMR = (9.99*self.weight) + (6.25*self.height) - (4.92*self.age) + 5
            return self.RMR
        else:
            #RMR equation for females
            self.RMR = (9.99*self.weight) + (6.25*self.height) - (4.92*self.age) - 161
            return self.RMR

    def activity_level(self):
        "Will display a table and ask for user to input the accurate activity level"

        #create table
        columns = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
        table = [["little to no activity",
                  "1-3 days per week of light activity",
                  "moderate exercise 3-5 days per week",
                  "rigorous exercise, 6-7 days per week",
                  "professional athlete, labor job, 2-3 times per day"]]

        transposed_table = list(zip(*table))

        #display table
        print("Please pick the appropriate activity level:")
        print(tabulate(transposed_table, headers=["Activity Level", "Description"], tablefmt="grid", showindex=columns))

        #ask user to input their activity level
        self.activitylevel = input("Activity Level:")


    def calculate_TDEE(self):
        "Calculate client's Total Daily Energy Expenditure also known as maintenance calories (no weight loss or weight gain)"

        #call the activity_level method to determine client's current activity level
        self.activity_level()

        #call calculate_RMR method, which is needed for TDEE calculation
        self.calculate_RMR()

        if self.activitylevel == "Sedentary":
            self.TDEE = self.RMR * 1.2
            #return self.TDEE
        elif self.activitylevel == "Lightly Active":
            self.TDEE = self.RMR * 1.375
            #return self.TDEE
        elif self.activitylevel == "Moderately Active":
            self.TDEE = self.RMR * 1.55
            #return self.TDEE
        elif self.activitylevel == "Very Active":
            self.TDEE = self.RMR * 1.725
            #return self.TDEE
        elif self.activitylevel == "Extra Active":
            self.TDEE = self.RMR * 1.9

        print("Your maintenance calories are ", round(self.TDEE))
