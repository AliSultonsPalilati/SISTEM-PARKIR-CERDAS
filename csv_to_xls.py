import pandas as pd

# Read the CSV file
csv_file = "test.csv"  # Replace with your CSV file path
xls_file = "hasilanalisiswireshark.xlsx"  # Desired output file name

# Convert CSV to XLS
df = pd.read_csv(csv_file)
df.to_excel(xls_file, index=False, engine='openpyxl')

print(f"File converted successfully to {xls_file}")
