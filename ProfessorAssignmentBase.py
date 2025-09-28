# -*- coding: utf-8 -*-
"""
Professor-Course Assignment Optimization using Linear Programming.

This script solves a classic assignment problem, specifically tailored for assigning
professors to university courses based on their preferences while respecting
various constraints like course demand and professor workload.

The goal of this optimization model is to find an assignment that maximizes
the overall happiness or preference satisfaction across all faculty. This is
achieved by minimizing the sum of preference "costs". In our preference
system, a lower number indicates a higher preference (e.g., 1 is a first choice).

We will use the PuLP library, which is a popular open-source linear programming
modeler for Python.

This script is structured to be easily understood and adapted for educational
purposes, such as in a Python notebook.
"""

# First, we need to import the PuLP library. If you don't have it installed,
# you can install it using pip: pip install pulp
import pulp

# --- 1. Define the Problem Data ---
# In a real-world scenario, this data would likely come from a database,
# CSV files, or a university information system. For this educational example,
# we will define it directly in the script.

# A list of all professors available for assignment.
PROFESSORS = [
    "Prof_A",
    "Prof_B",
    "Prof_C",
    "Prof_D",
    "Prof_E"
]

# A list of all courses that need to be taught.
COURSES = [
    "Intro_to_AI",
    "Advanced_Algorithms",
    "Databases",
    "Operating_Systems",
    "Linear_Algebra",
    "Web_Development",
    "Mobile_Apps",
    "Machine_Learning",
    "Cybersecurity",
    "Software_Engineering"
]

# --- 2. Define Preferences and Constraints ---

# Professor Preferences:
# This is a critical piece of data. We represent preferences as a dictionary
# where keys are professor names. The values are another dictionary where keys
# are course names and values are the preference ranking.
# A lower number means a higher preference. For example, a '1' is a top choice.
# We can use a high number (like 999) to indicate that a professor cannot or
# will not teach a specific course (e.g., they are not qualified).
preferences = {
    "Prof_A": {"Intro_to_AI": 1, "Advanced_Algorithms": 2, "Databases": 999, "Operating_Systems": 999, "Linear_Algebra": 3, "Web_Development": 2, "Mobile_Apps": 999, "Machine_Learning": 1, "Cybersecurity": 999, "Software_Engineering": 3},
    "Prof_B": {"Intro_to_AI": 2, "Advanced_Algorithms": 1, "Databases": 3, "Operating_Systems": 999, "Linear_Algebra": 999, "Web_Development": 999, "Mobile_Apps": 2, "Machine_Learning": 1, "Cybersecurity": 3, "Software_Engineering": 999},
    "Prof_C": {"Intro_to_AI": 999, "Advanced_Algorithms": 999, "Databases": 1, "Operating_Systems": 2, "Linear_Algebra": 3, "Web_Development": 1, "Mobile_Apps": 2, "Machine_Learning": 999, "Cybersecurity": 999, "Software_Engineering": 3},
    "Prof_D": {"Intro_to_AI": 3, "Advanced_Algorithms": 999, "Databases": 2, "Operating_Systems": 1, "Linear_Algebra": 999, "Web_Development": 999, "Mobile_Apps": 999, "Machine_Learning": 3, "Cybersecurity": 1, "Software_Engineering": 2},
    "Prof_E": {"Intro_to_AI": 1, "Advanced_Algorithms": 999, "Databases": 999, "Operating_Systems": 3, "Linear_Algebra": 2, "Web_Development": 3, "Mobile_Apps": 1, "Machine_Learning": 2, "Cybersecurity": 999, "Software_Engineering": 999},
}

# Course Load (Demand):
# This dictionary defines how many sections of each course need to be taught.
# The total demand must equal the total number of courses taught by professors.
# (5 professors * 5 courses/prof) = 25 total sections needed.
course_demand = {
    "Intro_to_AI": 3,
    "Advanced_Algorithms": 2,
    "Databases": 3,
    "Operating_Systems": 2,
    "Linear_Algebra": 3,
    "Web_Development": 3,
    "Mobile_Apps": 2,
    "Machine_Learning": 3,
    "Cybersecurity": 2,
    "Software_Engineering": 2,
}

# Professor Workload (Supply):
# This dictionary defines the exact number of courses each professor must teach.
professor_load = {
    "Prof_A": 5,
    "Prof_B": 5,
    "Prof_C": 5,
    "Prof_D": 5,
    "Prof_E": 5,
}

# --- 3. Set up the Linear Programming Model ---

# We create an instance of a PuLP problem. We can give it a name.
# The `LpMinimize` argument tells PuLP that our objective is to minimize a value.
# In our case, we want to minimize the total preference "cost" of the assignments.
model = pulp.LpProblem("Professor_Course_Assignment", pulp.LpMinimize)

# --- 4. Define the Decision Variables ---

# The core of the model is the set of decision variables. These are the quantities
# we want the solver to determine.
#
# Our decision is "Do we assign Professor P to Course C?" This is a binary choice
# (yes or no), so we use binary variables.
#
# The variable `x_pc` will be 1 if Professor P is assigned to Course C, and 0 otherwise.
# We will create one such variable for every possible professor-course pair.
# We use a dictionary to store these variables for easy access.
assignment_vars = pulp.LpVariable.dicts(
    "Assignment",  # A prefix for the variable names
    (PROFESSORS, COURSES), # A tuple defining the indices of the dictionary
    cat='Binary'  # The category of variable: Binary (0 or 1)
)

# --- 5. Define the Objective Function ---

# The objective function is the value we want to minimize or maximize.
# We want to minimize the sum of the preference scores for all assignments made.
#
# The formula is: SUM ( preference_pc * assignment_vars_pc ) for all p in PROFESSORS and c in COURSES.
#
# The `pulp.lpSum()` function is a convenient way to build this summation expression.
# We iterate through all professor-course pairs and add their contribution
# (preference cost * decision variable) to the total sum.
objective_function = pulp.lpSum(
    [preferences[p][c] * assignment_vars[p][c] for p in PROFESSORS for c in COURSES]
)

# We add the objective function to our model.
model += objective_function, "Total_Preference_Cost"


# --- 6. Define the Constraints ---

# Constraints are the rules that our solution must follow.

# Constraint 1: Each course must be taught the required number of times.
# For each course 'c', the sum of assignments from all professors to that course
# must equal the demand for that course.
# SUM ( assignment_vars_pc ) for all p in PROFESSORS == course_demand_c
for c in COURSES:
    model += (
        pulp.lpSum([assignment_vars[p][c] for p in PROFESSORS]) == course_demand[c],
        f"Course_{c}_Demand_Constraint" # A descriptive name for the constraint
    )

# Constraint 2: Each professor cannot be assigned more courses than their maximum load.
# For each professor 'p', the sum of their assignments across all courses
# must be less than or equal to their maximum teaching load.
# for all c in COURSES <= professor_max_load_p
for p in PROFESSORS:
    model += (
        pulp.lpSum([assignment_vars[p][c] for c in COURSES]) == professor_load[p],
        f"Professor_{p}_Load_Constraint" # A descriptive name for the constraint
    )

# --- 7. Solve the Problem ---

# The model is now fully defined. We can ask PuLP to solve it.
# PuLP will call an underlying solver (like CBC, which is included, or others like Gurobi/CPLEX).
# The `solve()` method will run the optimization and store the results in the model and variables.
print("Solving the assignment problem...")
model.solve()
print("Solver finished.")

# --- 8. Display the Results ---

# We can check the status of the solution.
status = pulp.LpStatus[model.status]
print(f"Solution Status: {status}\n")

# If an optimal solution was found, we can inspect the results.
if model.status == pulp.LpStatusOptimal:
    print("Optimal Assignment Found:")
    total_cost = 0
    assigned_count = 0
    # We iterate through the decision variables.
    # The `varValue` attribute holds the optimal value (0 or 1) found by the solver.
    for p in PROFESSORS:
        for c in COURSES:
            if assignment_vars[p][c].varValue == 1:
                preference_score = preferences[p][c]
                print(f"  - Assign {p} to {c} (Preference Score: {preference_score})")
                total_cost += preference_score
                assigned_count += 1
    
    # Print the final objective value, which is the total preference cost.
    objective_value = pulp.value(model.objective)
    print(f"\nTotal Preference Cost (minimized): {objective_value}")
    
    # Calculate and print the average preference score.
    if assigned_count > 0:
        average_preference = objective_value / assigned_count
        print(f"Average Preference Score per Assignment: {average_preference:.2f}")

else:
    print("No optimal solution found. The problem may be infeasible or unbounded.")

# You can also print the entire model definition to see the equations.
# This is very useful for debugging.
# print("\n--- Model Definition ---")
# print(model)

