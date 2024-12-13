from tabulate import tabulate

class PersonalSummary:
    """
    The PersonalSummary will collect key information about the client, calculate their BMI, and display info

    """

    def __init__(self):
        #the init method is empty as there is nothing to initialize
        pass

    def collect_info(self):
        "Collect key information about the client"

        self.name = input("Enter your name:")
        self.height = float(input("Enter your height in cm"))
        self.weight = float(input("Enter your weight in kg"))
        self.age = int(input("Enter your age"))
        self.gender = input("Enter your gender, M or F")


    def calculate_BMI(self):
        "Calculate the client's BMI"
        #BMI equation
        self.BMI = round(self.weight/((self.height/100)**2))

    def display_ps(self):
        "Display client information"
        self.calculate_BMI()   #call calculate_BMI method in order to display it

        headers = ["Name", "Age", "Height", "Weight", "Gender", "BMI"]
        data = [[self.name, self.age, self.height, self.weight, self.gender, self.BMI]]

        print(tabulate(data, headers=headers, tablefmt="grid", colalign=("center", "center", "center", "center", "center", "center")))
