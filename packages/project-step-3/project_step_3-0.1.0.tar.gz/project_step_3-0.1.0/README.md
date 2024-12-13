## Fitness and Nutrition Management System
Aamna Amer 74871567 Suneet D’Silva - 51059153

Create a tool for personal trainers to help their clients satisfy their personal fitness and nutrition goals.

Our program enables trainers to populate a database with key metrics about their clients, such as height, weight, age, and gender.

It will utilize various metrics to guide the client’s fitness and nutrition plan.

The client can set goals and timelines for achieving those goals


### System  Key Features: 
- Personal Summary
- Calorie Calculator
- Resting Metabolic Rate
- Total Daily Energy Expenditure
- Macros
- Workout Schedule

## Sub Package 1
### Module 1 - Personal Summary

Contains the class PersonalSummary that collects and stores client details.

Its methods include:

**collect_info():** Prompt user for data such as height, weight, age, gender, and name.

**calculate_BMI():** Calculate client's Body Mass Index

**display_ps():** Will display client information and BMI in a table for easy reading. Will always call method calculate_BMI() in case that hasn't been calculated already.


### Module 2 - Energy Requirements

Contains the class EnergyRequirements that calculates key caloric information about the client needed for baseline. It will inherit the PersonalSummary class. 

It's methods include:

**calculate_RMR():** Calculates client's Resting Metabolic Rate, which is calories burned at rest.

**activity_level:** Determines the client's current activity level. This is needed to estimate average calories burned. 

**calculate_TDEE():** Calculates client's Total Daily Energy Expenditure, which takes into account a client's RMR and activity level. It is essentially their maintenance calories; no weight loss or weight gain. 

### Module 3 - Goals

Contains the class Goals which will determine what the client's new caloric intake should be given their goal of weight loss or weight gain and their timeline. It will inherit the EnergyRequirements class. 

It's methods include:

**goal():** Will ask user if their goal is weight loss or weight gain, how much weight differential, and the timeline

**caloric_change():** Calculates caloric change needed for goal weight loss/gain. This is based off that 1 lb = 3500 calories. Formula used is caloric change = desired weight loss/gain (pounds) x 3500/ number of days

**caloric_intake():** Calculate client's new caloric intake based on goals and maintenance calories. This will call caloric_change() first to avoid redundancy. Formula used is new caloric intake = maintenance calories - caloric change


## Sub Package 2
### Module 1 - Macros

Contains the class Macros, which calculates macronutrient requirements and creates personalized nutrition plans based on user goals.

It's methods include:

**calculate_macro_requirements()**
  Ensures the caloric intake is populated and calculates the macronutrient requirements (proteins, carbs, and fats) based on the client's caloric intake.  
  Default distribution:  
  - 30% Protein  
  - 40% Carbs  
  - 30% Fats  

**customize_macro_distribution()**  
  Allows the user to distribute macronutrients (proteins, carbs, and fats) across meals (e.g., breakfast, lunch, dinner, snacks). Ensures the distribution percentages are valid.

**generate_nutrition_plan()**  
  Generates a detailed nutrition plan based on the calculated macronutrient requirements and customized meal distributions. Displays calories and macronutrients for each meal.

### Module 2 - Workout Schedule

Contains the class WorkoutSchedule, which helps users create, display, and customize workout schedules based on their preferences.

It's methods include:

**generate_training_split()**  
  Prompts the user to generate a workout schedule by specifying daily workout time, number of workout days per week, preferred time of day, and activity type.

**display_workout_schedule()**  
  Displays the workout schedule in an easy-to-read format, showing the planned activity, duration, and time of day for each day.

**customize_workout_schedule()**  
  Allows the user to customize their workout schedule by editing individual days, changing the activity, duration, and time of day. Ensures input is validated before saving updates.

[![Build Status](https://app.travis-ci.com/aamna-amer/project-step-3.svg?token=QxFbpBhgrrJecX6pobud&branch=main)](https://app.travis-ci.com/aamna-amer/project-step-3)
