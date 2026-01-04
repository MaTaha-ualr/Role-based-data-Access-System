import pandas as pd

# Load the files into pandas dataframes
file_a = pd.read_csv('file_a.csv')  # Data file
file_b = pd.read_csv('file_b.csv')  # Column sensitivity file
file_c = pd.read_csv('file_c.csv')  # User access file

# Step 3: Validate the user
def validate_user(username):
    # Check if the user exists in file_c and return their access status
    user_info = file_c[file_c['username'] == username]
    if user_info.empty:
        return None, False
    else:
        # Get the user's sensitivity access (yes or no)
        has_access_to_sensitive = user_info.iloc[0]['access_sensitive'] == 'yes'
        return user_info, has_access_to_sensitive

# Step 4: Get accessible columns based on user’s sensitivity access
def get_accessible_columns(has_access_to_sensitive):
    if has_access_to_sensitive:
        # User can access both sensitive and non-sensitive columns
        accessible_columns = file_b['column_name'].tolist()
    else:
        # Filter out sensitive columns
        accessible_columns = file_b[file_b['sensitivity'] == 'no']['column_name'].tolist()
    
    return accessible_columns

# Step 5: Show the user the available columns and let them choose
def display_options_to_user(accessible_columns):
    print(f"Accessible columns: {', '.join(accessible_columns)}")
    selected_columns = input("Enter the columns you want to view, separated by commas: ").split(',')
    selected_columns = [col.strip() for col in selected_columns if col.strip() in accessible_columns]
    return selected_columns

# Step 6: Display the selected columns' data
def display_selected_data(selected_columns):
    # Filter File A with selected columns
    if selected_columns:
        print(file_a[selected_columns])
    else:
        print("No valid columns selected.")

# Step 7: Main logic to bring everything together
def main():
    username = input("Enter your username: ")
    
    # Step 1: Validate the user
    user_info, has_access = validate_user(username)
    
    if user_info is None:
        print("User does not exist or is not allowed.")
        return
    
    # Step 2: Get the accessible columns
    accessible_columns = get_accessible_columns(has_access)
    
    # Step 3: Display the available columns and get user's selection
    selected_columns = display_options_to_user(accessible_columns)
    
    # Step 4: Display the data based on user's selection
    display_selected_data(selected_columns)

# Run the main function
if __name__ == "__main__":
    main()
