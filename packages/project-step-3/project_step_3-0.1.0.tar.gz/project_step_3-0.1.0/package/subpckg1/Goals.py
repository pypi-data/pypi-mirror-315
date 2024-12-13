from package.subpckg1.PersonalSummary import PersonalSummary
from package.subpckg1.EnergyRequirements import EnergyRequirements
from tabulate import tabulate

class Goals(EnergyRequirements):
    """
    Goals will calculate the client's new caloric intake based on their goals of weight loss/gain
    and the timeline of when they want to acheive them. Goals will inherit EnergyRequirements

    """

    def __init__(self):
        #initialize the inheriance
        EnergyRequirements.__init__(self)

    def goal_setting(self):
        "Will ask user if their goal is weight loss or weight gain, how much weight differential, and the timeline"

        self.goal = input("What is your main goal: weight loss or weight gain?")

        #determine weight gain or weight loss, and timeline
        if self.goal == "weight loss":
            self.weight_loss = int(input("How much weight do you want to lose? Please enter in lbs"))
            self.timeline = int(input("By when do you want to acheive this? Please answer in days"))
        else:
            self.weight_gain = int(input("How much weight do you want to gain? Please enter in lbs"))
            self.timeline = int(input("By when do you want to acheive this? Please answer in days"))

        
    def caloric_change(self):
        "Calculate caloric change needed for goal weight loss/gain. This is based off that 1 lb = 3500 calories"
        
        # Calculate caloric change based on weight loss or gain
        if self.goal == "weight loss":
            # For weight loss, adding a negative sign for caloric reduction
            caloric_change_value = -((self.weight_loss * 3500) / self.timeline)
        else:
            # For weight gain
            caloric_change_value = (self.weight_gain * 3500) / self.timeline
       
       # Store the value in a distinct attribute
        self.caloric_change_value = caloric_change_value
        return self.caloric_change_value  # Return the calculated value
   
    def caloric_intake(self):
        "Calculate client's new caloric intake based on goals and maintenance calories"
       
        # Explicitly call the caloric_change method to get its value
        self.caloric_change()
        
        # Store new caloric intake as a separate attribute
        self.daily_caloric_intake = round(self.TDEE + self.caloric_change_value)
        print("Your new daily caloric intake is ", self.daily_caloric_intake)
        return self.daily_caloric_intake  # Return the value
