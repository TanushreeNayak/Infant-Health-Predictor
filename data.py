import pandas as pd

# Creating the Children table DataFrame
children_data = {
    "child_id": [1, 2, 3, 4, 5],
    "name": ["Ayaan", "Sara", "Rohan", "Meera", "Ishaan"],
    "age": [5, 6, 4, 7, 5],
    "date_of_birth": ["2019-04-10", "2018-06-15", "2020-02-20", "2017-12-01", "2019-07-25"]
}

df_children = pd.DataFrame(children_data)

# Creating the Vital_Signs table DataFrame
vital_signs_data = {
    "child_id": [1, 2, 3, 4, 5],
    "height": [110, 115, 102, 120, 108],  # in cm
    "weight": [18, 20, 16, 22, 19],  # in kg
    "date_taken": ["2025-04-01", "2025-04-01", "2025-04-01", "2025-04-01", "2025-04-01"]
}

df_vital_signs = pd.DataFrame(vital_signs_data)

# Display DataFrames
print("Children Table:\n", df_children)
print("\nVital Signs Table:\n", df_vital_signs)
