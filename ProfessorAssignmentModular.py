# -*- coding: utf-8 -*-
"""
Professor-Course Assignment Optimization using Linear Programming.

This script solves a classic assignment problem, specifically tailored for assigning
professors to university courses based on their preferences while respecting
various constraints like course demand and professor workload.

This version is modularized into functions to separate data loading, model building,
and results display, making it easier to maintain and adapt.
"""
import pulp
import pandas as pd  # Required for the CSV data loading function
# import sqlite3       # Required for the database data loading function

# --- 1. Data Loading Functions ---

def get_data_hardcoded():
    """
    Provides a hardcoded set of data for the optimization problem.
    This is useful for testing and simple examples.
    
    Returns:
        tuple: A tuple containing professors, courses, preferences,
               course_demand, and professor_load.
    """
    print("Loading hardcoded data set...")
    professors = [
        "Prof_A", "Prof_B", "Prof_C", "Prof_D", "Prof_E"
    ]

    courses = [
        "Intro_to_AI", "Advanced_Algorithms", "Databases", "Operating_Systems",
        "Linear_Algebra", "Web_Development", "Mobile_Apps", "Machine_Learning",
        "Cybersecurity", "Software_Engineering"
    ]

    preferences = {
        "Prof_A": {"Intro_to_AI": 1, "Advanced_Algorithms": 2, "Databases": 999, "Operating_Systems": 999, "Linear_Algebra": 3, "Web_Development": 2, "Mobile_Apps": 999, "Machine_Learning": 1, "Cybersecurity": 999, "Software_Engineering": 3},
        "Prof_B": {"Intro_to_AI": 2, "Advanced_Algorithms": 1, "Databases": 3, "Operating_Systems": 999, "Linear_Algebra": 999, "Web_Development": 999, "Mobile_Apps": 2, "Machine_Learning": 1, "Cybersecurity": 3, "Software_Engineering": 999},
        "Prof_C": {"Intro_to_AI": 999, "Advanced_Algorithms": 999, "Databases": 1, "Operating_Systems": 2, "Linear_Algebra": 3, "Web_Development": 1, "Mobile_Apps": 2, "Machine_Learning": 999, "Cybersecurity": 999, "Software_Engineering": 3},
        "Prof_D": {"Intro_to_AI": 3, "Advanced_Algorithms": 999, "Databases": 2, "Operating_Systems": 1, "Linear_Algebra": 999, "Web_Development": 999, "Mobile_Apps": 999, "Machine_Learning": 3, "Cybersecurity": 1, "Software_Engineering": 2},
        "Prof_E": {"Intro_to_AI": 1, "Advanced_Algorithms": 999, "Databases": 999, "Operating_Systems": 3, "Linear_Algebra": 2, "Web_Development": 3, "Mobile_Apps": 1, "Machine_Learning": 2, "Cybersecurity": 999, "Software_Engineering": 999},
    }

    course_demand = {
        "Intro_to_AI": 3, "Advanced_Algorithms": 2, "Databases": 3,
        "Operating_Systems": 2, "Linear_Algebra": 3, "Web_Development": 3,
        "Mobile_Apps": 2, "Machine_Learning": 3, "Cybersecurity": 2,
        "Software_Engineering": 2,
    }

    professor_load = {
        "Prof_A": 5, "Prof_B": 5, "Prof_C": 5, "Prof_D": 5, "Prof_E": 5,
    }
    
    return professors, courses, preferences, course_demand, professor_load

def get_data_from_csvs(folder_path="."):
    """
    Loads the optimization problem data from a set of CSV files.
    This function is a placeholder and demonstrates how you would implement it.

    Expected CSV formats:
    - professors.csv: A single column "ProfessorName"
    - courses.csv: A single column "CourseName"
    - course_demand.csv: Columns "CourseName", "Demand"
    - professor_load.csv: Columns "ProfessorName", "Load"
    - preferences.csv: Columns "ProfessorName", "CourseName", "Preference" (long format)

    Args:
        folder_path (str): The path to the directory containing the CSV files.

    Returns:
        tuple: A tuple containing the data structures for the problem.
    """
    print(f"Loading data from CSV files in '{folder_path}'...")
    # This is a placeholder implementation. To make it work, you would create
    # the CSV files with the described structure.
    # For example, preferences.csv would look like:
    # ProfessorName,CourseName,Preference
    # Prof_A,Intro_to_AI,1
    # Prof_A,Advanced_Algorithms,2
    # ...
    
    # Read the simple lists
    # professors_df = pd.read_csv(f"{folder_path}/professors.csv")
    # professors = professors_df['ProfessorName'].tolist()
    # courses_df = pd.read_csv(f"{folder_path}/courses.csv")
    # courses = courses_df['CourseName'].tolist()

    # Read the dictionaries
    # demand_df = pd.read_csv(f"{folder_path}/course_demand.csv")
    # course_demand = demand_df.set_index('CourseName')['Demand'].to_dict()
    # load_df = pd.read_csv(f"{folder_path}/professor_load.csv")
    # professor_load = load_df.set_index('ProfessorName')['Load'].to_dict()

    # Read the nested preference dictionary
    # prefs_df = pd.read_csv(f"{folder_path}/preferences.csv")
    # preferences = prefs_df.set_index(['ProfessorName', 'CourseName'])['Preference'].to_dict('index')
    # preferences = {k[0]: {} for k in preferences.keys()}
    # for (prof, course), pref in prefs_df.set_index(['ProfessorName', 'CourseName'])['Preference'].items():
    #     preferences[prof][course] = pref

    # raise NotImplementedError("This function is a placeholder. You need to create the CSV files.")
    # For now, we return the hardcoded data so the script can run.
    return get_data_hardcoded()

def get_data_from_database(db_path="university.db"):
    """
    Loads the optimization problem data from a SQLite database.
    This function is a placeholder and demonstrates how you would implement it.
    
    Expected Table Schemas:
    - Professors(ProfessorName TEXT PRIMARY KEY)
    - Courses(CourseName TEXT PRIMARY KEY, Demand INTEGER)
    - ProfessorLoad(ProfessorName TEXT, Load INTEGER)
    - Preferences(ProfessorName TEXT, CourseName TEXT, Preference INTEGER)
    
    Args:
        db_path (str): The path to the SQLite database file.

    Returns:
        tuple: A tuple containing the data structures for the problem.
    """
    print(f"Loading data from database '{db_path}'...")
    # This is a placeholder implementation.
    # conn = sqlite3.connect(db_path)
    # cursor = conn.cursor()
    # ... execute SQL queries to fetch data ...
    # conn.close()
    # raise NotImplementedError("This function is a placeholder. You need to set up the database.")
    # For now, we return the hardcoded data so the script can run.
    return get_data_hardcoded()

# --- 2. Model Building and Solving Functions ---

def build_and_solve_model(professors, courses, preferences, course_demand, professor_load):
    """
    Builds and solves the linear programming model for course assignment.

    Args:
        professors (list): A list of professor names.
        courses (list): A list of course names.
        preferences (dict): A nested dictionary of preferences.
        course_demand (dict): A dictionary of course demand.
        professor_load (dict): A dictionary of professor teaching loads.

    Returns:
        tuple: A tuple containing the solved model and the assignment variables.
    """
    # --- Model Setup ---
    model = pulp.LpProblem("Professor_Course_Assignment", pulp.LpMinimize)

    # --- Decision Variables ---
    assignment_vars = pulp.LpVariable.dicts(
        "Assignment", (professors, courses), cat='Binary'
    )

    # --- Objective Function ---
    objective_function = pulp.lpSum(
        [preferences[p][c] * assignment_vars[p][c] for p in professors for c in courses]
    )
    model += objective_function, "Total_Preference_Cost"

    # --- Constraints ---
    # Each course must meet its demand.
    for c in courses:
        model += (
            pulp.lpSum([assignment_vars[p][c] for p in professors]) == course_demand[c],
            f"Course_{c}_Demand_Constraint"
        )

    # Each professor must teach their required number of courses.
    for p in professors:
        model += (
            pulp.lpSum([assignment_vars[p][c] for c in courses]) == professor_load[p],
            f"Professor_{p}_Load_Constraint"
        )

    # --- Solve the model ---
    print("Solving the assignment problem...")
    model.solve()
    print("Solver finished.")
    
    return model, assignment_vars

# --- 3. Results Display Function ---

def display_results(model, assignment_vars, preferences, professors, courses):
    """
    Displays the results of the solved optimization model.
    """
    status = pulp.LpStatus[model.status]
    print(f"Solution Status: {status}\n")

    if model.status == pulp.LpStatusOptimal:
        print("Optimal Assignment Found:")
        assigned_count = 0
        for p in professors:
            print(f"\n--- Courses for {p} ---")
            prof_courses = []
            for c in courses:
                if assignment_vars[p][c].varValue == 1:
                    preference_score = preferences[p][c]
                    prof_courses.append(f"  - {c} (Preference: {preference_score})")
                    assigned_count += 1
            if prof_courses:
                for item in prof_courses:
                    print(item)
            else:
                print("  - No courses assigned.")
        
        objective_value = pulp.value(model.objective)
        print(f"\nTotal Preference Cost (minimized): {objective_value}")
        
        if assigned_count > 0:
            average_preference = objective_value / assigned_count
            print(f"Average Preference Score per Assignment: {average_preference:.2f}")

    else:
        print("No optimal solution found. The problem may be infeasible or unbounded.")

# --- 4. Main Execution Block ---

if __name__ == "__main__":
    # To change the data source, simply swap which function is called here.
    # For example, to use CSV files, you would change the line to:
    # professors, courses, preferences, course_demand, professor_load = get_data_from_csvs()
    
    # Step 1: Load the data
    professors, courses, preferences, course_demand, professor_load = get_data_hardcoded()
    
    # Step 2: Build and solve the model
    model, assignment_vars = build_and_solve_model(
        professors, courses, preferences, course_demand, professor_load
    )
    
    # Step 3: Display the results
    display_results(model, assignment_vars, preferences, professors, courses)

