# -*- coding: utf-8 -*-
"""
Script to generate sample data files for the professor-course assignment problem.

This script creates:
1. A set of CSV files in the current directory.
2. A SQLite database file (`university.db`) in the current directory.

These generated files can be used to test the data loading functions in the
main optimization script.
"""
import pandas as pd
import sqlite3
import os

def get_data():
    """Returns the hardcoded data as pandas DataFrames."""
    # Using the same data from the main script's hardcoded function
    preferences_long = [
        ('Prof_A', 'Intro_to_AI', 1), ('Prof_A', 'Advanced_Algorithms', 2), ('Prof_A', 'Databases', 999),
        ('Prof_A', 'Operating_Systems', 999), ('Prof_A', 'Linear_Algebra', 3), ('Prof_A', 'Web_Development', 2),
        ('Prof_A', 'Mobile_Apps', 999), ('Prof_A', 'Machine_Learning', 1), ('Prof_A', 'Cybersecurity', 999),
        ('Prof_A', 'Software_Engineering', 3),
        ('Prof_B', 'Intro_to_AI', 2), ('Prof_B', 'Advanced_Algorithms', 1), ('Prof_B', 'Databases', 3),
        ('Prof_B', 'Operating_Systems', 999), ('Prof_B', 'Linear_Algebra', 999), ('Prof_B', 'Web_Development', 999),
        ('Prof_B', 'Mobile_Apps', 2), ('Prof_B', 'Machine_Learning', 1), ('Prof_B', 'Cybersecurity', 3),
        ('Prof_B', 'Software_Engineering', 999),
        ('Prof_C', 'Intro_to_AI', 999), ('Prof_C', 'Advanced_Algorithms', 999), ('Prof_C', 'Databases', 1),
        ('Prof_C', 'Operating_Systems', 2), ('Prof_C', 'Linear_Algebra', 3), ('Prof_C', 'Web_Development', 1),
        ('Prof_C', 'Mobile_Apps', 2), ('Prof_C', 'Machine_Learning', 999), ('Prof_C', 'Cybersecurity', 999),
        ('Prof_C', 'Software_Engineering', 3),
        ('Prof_D', 'Intro_to_AI', 3), ('Prof_D', 'Advanced_Algorithms', 999), ('Prof_D', 'Databases', 2),
        ('Prof_D', 'Operating_Systems', 1), ('Prof_D', 'Linear_Algebra', 999), ('Prof_D', 'Web_Development', 999),
        ('Prof_D', 'Mobile_Apps', 999), ('Prof_D', 'Machine_Learning', 3), ('Prof_D', 'Cybersecurity', 1),
        ('Prof_D', 'Software_Engineering', 2),
        ('Prof_E', 'Intro_to_AI', 1), ('Prof_E', 'Advanced_Algorithms', 999), ('Prof_E', 'Databases', 999),
        ('Prof_E', 'Operating_Systems', 3), ('Prof_E', 'Linear_Algebra', 2), ('Prof_E', 'Web_Development', 3),
        ('Prof_E', 'Mobile_Apps', 1), ('Prof_E', 'Machine_Learning', 2), ('Prof_E', 'Cybersecurity', 999),
        ('Prof_E', 'Software_Engineering', 999)
    ]
    prefs_df = pd.DataFrame(preferences_long, columns=['ProfessorName', 'CourseName', 'Preference'])

    professors_df = pd.DataFrame({'ProfessorName': ["Prof_A", "Prof_B", "Prof_C", "Prof_D", "Prof_E"]})
    
    courses_df = pd.DataFrame({'CourseName': [
        "Intro_to_AI", "Advanced_Algorithms", "Databases", "Operating_Systems", "Linear_Algebra",
        "Web_Development", "Mobile_Apps", "Machine_Learning", "Cybersecurity", "Software_Engineering"
    ]})

    demand_data = {
        "CourseName": ["Intro_to_AI", "Advanced_Algorithms", "Databases", "Operating_Systems", "Linear_Algebra",
                       "Web_Development", "Mobile_Apps", "Machine_Learning", "Cybersecurity", "Software_Engineering"],
        "Demand": [3, 2, 3, 2, 3, 3, 2, 3, 2, 2]
    }
    demand_df = pd.DataFrame(demand_data)

    load_data = {
        "ProfessorName": ["Prof_A", "Prof_B", "Prof_C", "Prof_D", "Prof_E"],
        "Load": [5, 5, 5, 5, 5]
    }
    load_df = pd.DataFrame(load_data)

    return professors_df, courses_df, demand_df, load_df, prefs_df

def create_csv_files(professors_df, courses_df, demand_df, load_df, prefs_df):
    """Saves the dataframes to CSV files."""
    print("Creating CSV files...")
    professors_df.to_csv("professors.csv", index=False)
    courses_df.to_csv("courses.csv", index=False)
    demand_df.to_csv("course_demand.csv", index=False)
    load_df.to_csv("professor_load.csv", index=False)
    prefs_df.to_csv("preferences.csv", index=False)
    print("CSV files created successfully.")

def create_database(professors_df, courses_df, demand_df, load_df, prefs_df):
    """Creates and populates a SQLite database."""
    db_file = "university.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"Removed existing database file '{db_file}'.")
        
    print(f"Creating SQLite database '{db_file}'...")
    conn = sqlite3.connect(db_file)
    
    # We need separate tables for courses and demand to match the SQL schema
    courses_for_db = courses_df[['CourseName']]
    
    professors_df.to_sql("Professors", conn, index=False, if_exists='replace')
    courses_for_db.to_sql("Courses", conn, index=False, if_exists='replace')
    demand_df.to_sql("CourseDemand", conn, index=False, if_exists='replace')
    load_df.to_sql("ProfessorLoad", conn, index=False, if_exists='replace')
    prefs_df.to_sql("Preferences", conn, index=False, if_exists='replace')
    
    conn.close()
    print("Database created and populated successfully.")

if __name__ == "__main__":
    # Get data as pandas DataFrames
    professors, courses, demand, load, prefs = get_data()
    
    # Create the CSV files
    create_csv_files(professors, courses, demand, load, prefs)
    
    print("-" * 20)
    
    # Create the SQLite database
    create_database(professors, courses, demand, load, prefs)
    
    print("\nSample data generation complete.")
