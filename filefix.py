import pandas as pd

def process_file_names(input_file, output_file):
    # Step 1: Load the CSV file
    df = pd.read_csv(input_file)

    # Step 2: Remove ~$ from 'File Path'
    df['File Path'] = df['File Path'].str.replace(r'~\$', '', regex=True)

    # Step 3: Save the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processed file names and saved to {output_file}")

# Example usage:
if __name__ == "__main__":
    input_file = r"C:\Users\akash\OneDrive\Documents\coding\C++\file_access_log1.csv"
    output_file = r"C:\Users\akash\OneDrive\Documents\coding\C++\file_access_log2.csv"
    
    process_file_names(input_file, output_file)
