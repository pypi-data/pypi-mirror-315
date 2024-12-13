
#Comments and Documentation implemented with ChatGPT



from tabulate import tabulate
from package.subpckg1.Goals import Goals

class Macros:
    """
    Macros class calculates macronutrient requirements and generates a nutrition plan
    based on the user's goals and customized macro distribution.
    """

    def __init__(self, goals_instance):

        if not isinstance(goals_instance, Goals):
            raise TypeError("The provided goals_instance must be an instance of the Goals class.")
        self.goals = goals_instance
        self.custom_distribution = {}  # Initialize as an empty dict
        self.meal_ratios = [0.3, 0.3, 0.3, 0.1]  # Default meal ratios for breakfast, lunch, dinner, and snacks
        if not (0.99 <= sum(self.meal_ratios) <= 1.01):
            raise ValueError("Meal ratios must sum to 1 and be between 0 and 1.")

        self.goals = goals_instance
        self.custom_distribution = {}  # Initialize as an empty dict
        self.meal_ratios = [0.3, 0.3, 0.3, 0.1]  # Default meal ratios for breakfast, lunch, dinner, and snacks


    def ensure_goals_populated(self):
        """
        Ensure that the Goals instance is populated with necessary information.
        """
        required_attrs = ["daily_caloric_intake"]
        for attr in required_attrs:
            if not hasattr(self.goals, attr):

                raise AttributeError(
                    f"Goals instance is missing required attribute '{attr}'. "
                    "Ensure Goals is properly initialized and populated before using Macros."
                )
            if getattr(self.goals, attr) is None:
                raise ValueError(f"Goals attribute '{attr}' is None. Populate it before proceeding.")

                raise ValueError(
                    f"Goals instance is missing required attribute '{attr}'. "
                    "Ensure Goals is properly initialized and populated before using Macros."
                )


    def calculate_macro_requirements(self):
        """
        Ensure caloric intake is populated and calculate macros based on default or customized ratios.
        """

        try:
            self.ensure_goals_populated()
            caloric_intake = self.goals.daily_caloric_intake
            if not isinstance(caloric_intake, (int, float)) or caloric_intake <= 0:
                raise ValueError("Daily caloric intake must be a positive number.")

            # Calculate macronutrient breakdown (protein, carbs, fats)
            protein_calories = caloric_intake * 0.3
            carbs_calories = caloric_intake * 0.4
            fats_calories = caloric_intake * 0.3

            # Convert calories to grams
            protein_grams = round(protein_calories / 4)
            carbs_grams = round(carbs_calories / 4)
            fats_grams = round(fats_calories / 9)

            self.macros = {
                "Protein (g)": protein_grams,
                "Carbs (g)": carbs_grams,
                "Fats (g)": fats_grams
            }

            # Display macronutrient requirements
            print("\nMacronutrient Requirements:")
            print(tabulate([self.macros], headers="keys", tablefmt="grid"))
            return self.macros
        except Exception as e:
            print(f"Error in calculate_macro_requirements: {e}")
            raise

        if not hasattr(self.goals, "daily_caloric_intake"):
            print("Caloric intake is not populated. Populating it now...")
            self.goals.calculate_TDEE()
            self.goals.goal_setting()
            self.goals.caloric_intake()
        
        caloric_intake = self.goals.daily_caloric_intake

        # Calculate macronutrient breakdown (protein, carbs, fats)
        protein_calories = caloric_intake * 0.3
        carbs_calories = caloric_intake * 0.4
        fats_calories = caloric_intake * 0.3

        # Convert calories to grams
        protein_grams = round(protein_calories / 4)
        carbs_grams = round(carbs_calories / 4)
        fats_grams = round(fats_calories / 9)

        self.macros = {
            "Protein (g)": protein_grams,
            "Carbs (g)": carbs_grams,
            "Fats (g)": fats_grams
        }

        # Display macronutrient requirements
        print("\nMacronutrient Requirements:")
        print(tabulate([self.macros], headers="keys", tablefmt="grid"))
        return self.macros

    def customize_macro_distribution(self):
        """
        Allow the user to customize the distribution of macronutrients for each meal.
        """
        
        try:
            print("\nCustomizing macro distribution for meals.")

            # Get customized protein distribution
            print("\nCustomizing Protein distribution:")
            self.custom_distribution["Protein"] = self._get_custom_distribution("Protein")

            # Get customized carbs distribution
            print("\nCustomizing Carbs distribution:")
            self.custom_distribution["Carbs"] = self._get_custom_distribution("Carbs")

            # Get customized fats distribution
            print("\nCustomizing Fats distribution:")
            self.custom_distribution["Fats"] = self._get_custom_distribution("Fats")

            print("Macro distribution customized successfully.")
        except Exception as e:
            print(f"Error in customize_macro_distribution: {e}")
            raise

        print("\nCustomizing macro distribution for meals.")

        # Get customized protein distribution
        print("\nCustomizing Protein distribution:")
        self.custom_distribution["Protein"] = self._get_custom_distribution("Protein")

        # Get customized carbs distribution
        print("\nCustomizing Carbs distribution:")
        self.custom_distribution["Carbs"] = self._get_custom_distribution("Carbs")

        # Get customized fats distribution
        print("\nCustomizing Fats distribution:")
        self.custom_distribution["Fats"] = self._get_custom_distribution("Fats")

        print("Macro distribution customized successfully.")


    def _get_custom_distribution(self, macro):
        """
        Helper method to handle getting valid input for the macro distribution.
        """
        distribution = []
        total = 0

        for meal in ["Breakfast", "Lunch", "Dinner", "Snacks"]:
            while True:
                try:
                    percentage = int(input(f"Enter the percentage of {macro} for {meal} (0-100): "))
                    if percentage < 0 or percentage > 100:
                        raise ValueError(f"Invalid input for {meal}. Percentage must be between 0 and 100.")
                    if total + percentage > 100:
                        raise ValueError("Total percentage exceeds 100%.")
                    distribution.append(percentage)
                    total += percentage
                    break
                except ValueError as e:
                    print(e)


        if total != 100:
            raise ValueError(f"The total percentage for {macro} must equal 100%. Got {total}%.")

        return distribution

    def generate_nutrition_plan(self):
        """
        Generate a nutrition plan based on calculated macros and user-defined distribution.
        """

        try:
            self.ensure_goals_populated()  # Validate that Goals is ready

            caloric_intake = self.goals.daily_caloric_intake

            # Check if custom macro distribution is set; otherwise, use default ratios
            if not self.custom_distribution:
                print("Using default macro distribution.")
                self.custom_distribution = {
                    "Protein": [25, 25, 25, 25],
                    "Carbs": [25, 25, 25, 25],
                    "Fats": [25, 25, 25, 25]
                }

            # Validate custom distribution
            for macro, values in self.custom_distribution.items():
                if not isinstance(values, list) or len(values) != 4 or sum(values) != 100:
                    raise ValueError(
                        f"Custom distribution for {macro} is invalid. Ensure it is a list of 4 percentages summing to 100."
                    )

            # Calculate calories and macro breakdown for each meal
            meal_plan = []
            meal_names = ["Breakfast", "Lunch", "Dinner", "Snacks"]

            for i, meal in enumerate(meal_names):
                meal_calories = round(caloric_intake * self.meal_ratios[i])
                protein_calories = meal_calories * (self.custom_distribution["Protein"][i] / 100)
                carbs_calories = meal_calories * (self.custom_distribution["Carbs"][i] / 100)
                fats_calories = meal_calories * (self.custom_distribution["Fats"][i] / 100)

                # Convert calories to grams
                protein_grams = round(protein_calories / 4)
                carbs_grams = round(carbs_calories / 4)
                fats_grams = round(fats_calories / 9)

                # Append meal info
                meal_plan.append([
                    meal,
                    f"{meal_calories} calories",
                    f"{protein_grams}g protein",
                    f"{carbs_grams}g carbs",
                    f"{fats_grams}g fats"
                ])

            # Display the nutrition plan
            print("\nGenerated Nutrition Plan:")
            headers = ["Meal", "Calories", "Protein", "Carbs", "Fats"]
            print(tabulate(meal_plan, headers=headers, tablefmt="grid"))
        except Exception as e:
            print(f"Error in generate_nutrition_plan: {e}")
            raise

        self.ensure_goals_populated()  # Validate that Goals is ready

        caloric_intake = self.goals.daily_caloric_intake

        # Check if custom macro distribution is set; otherwise, use default ratios
        if not self.custom_distribution:
            print("Using default macro distribution.")
            self.custom_distribution = {
                "Protein": [25, 25, 25, 25],  
                "Carbs": [25, 25, 25, 25],
                "Fats": [25, 25, 25, 25]
            }

        # Calculate calories and macro breakdown for each meal
        meal_plan = []
        meal_names = ["Breakfast", "Lunch", "Dinner", "Snacks"]

        for i, meal in enumerate(meal_names):
            meal_calories = round(caloric_intake * self.meal_ratios[i])
            protein_calories = meal_calories * (self.custom_distribution["Protein"][i] / 100)
            carbs_calories = meal_calories * (self.custom_distribution["Carbs"][i] / 100)
            fats_calories = meal_calories * (self.custom_distribution["Fats"][i] / 100)

            # Convert calories to grams
            protein_grams = round(protein_calories / 4)
            carbs_grams = round(carbs_calories / 4)
            fats_grams = round(fats_calories / 9)

            # Append meal info
            meal_plan.append([
                meal,
                f"{meal_calories} calories",
                f"{protein_grams}g protein",
                f"{carbs_grams}g carbs",
                f"{fats_grams}g fats"
            ])

        # Display the nutrition plan
        print("\nGenerated Nutrition Plan:")
        headers = ["Meal", "Calories", "Protein", "Carbs", "Fats"]
        print(tabulate(meal_plan, headers=headers, tablefmt="grid"))

