import os
import shutil
import pandas as pd

# Directory where files will be cached
CACHE_DIRECTORY = 'cache/'

# Ensure the cache directory exists
if not os.path.exists(CACHE_DIRECTORY):
    os.makedirs(CACHE_DIRECTORY)

def cache_file(file_path):
    """Cache the given file by copying it to the cache directory."""
    # Check if the file is a temporary Excel file (starts with ~$)
    if os.path.basename(file_path).startswith('~$'):
        # Get the original file name by removing the ~$
        original_file_name = file_path[2:]  # Remove the first two characters (~$)
        original_file_path = os.path.join(os.path.dirname(file_path), original_file_name)  # Construct original file path
        
        print(f"Trying to access original file: {original_file_path}")  # Debugging line
        
        # Check if the original file exists
        if os.path.exists(original_file_path):
            try:
                # Copy the original file to the cache directory
                cached_file_path = os.path.join(CACHE_DIRECTORY, os.path.basename(original_file_path))
                shutil.copy2(original_file_path, cached_file_path)
                print(f"Cached: {original_file_path}")  # Print when the original file is cached
            except Exception as e:
                print(f"Failed to cache {original_file_path}: {e}")
        else:
            print(f"Original file does not exist: {original_file_path}")
    else:
        # If it's not a temporary file, proceed normally
        if os.path.exists(file_path):
            try:
                # Copy the file to the cache directory
                cached_file_path = os.path.join(CACHE_DIRECTORY, os.path.basename(file_path))
                shutil.copy2(file_path, cached_file_path)
                print(f"Cached: {file_path}")  # Print when a file is cached
            except Exception as e:
                print(f"Failed to cache {file_path}: {e}")
        else:
            print(f"File does not exist: {file_path}")

def cache_files_based_on_predictions(df):
    """Cache files based on the 'To Cache' column in the DataFrame."""
    # Iterate over the predictions and cache files
    for idx, should_cache in enumerate(df['To Cache']):
        file_path = df.iloc[idx]['File Path']
        if should_cache == 1:  # Column indicates to cache this file
            cache_file(file_path)  # Print the file being cached

# Example usage:
if __name__ == "__main__":
    # Load the dataset (replace with the path to your CSV file)
    df = pd.read_csv(r"C:\Users\akash\OneDrive\Documents\coding\C++\file_access_log2.csv")

    # Call the function to cache files based on the 'To Cache' column
    cache_files_based_on_predictions(df)
