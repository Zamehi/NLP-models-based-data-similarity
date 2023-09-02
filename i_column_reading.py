import pandas as pd

# --------------------------- READING DISTINCT FROM EXCEL COLUMN FUNCTION ------------------------------
# .................................function..................................
def get_distinct_strings_from_column(excel_file, sheet_name, column_name):
    try:
        # Read the Excel file into a pandas DataFrame
        df = pd.read_excel(excel_file, sheet_name=sheet_name)

        # Get the specified column as a pandas Series
        column_data = df[column_name]

        # Extract distinct strings from the column
        distinct_strings = column_data.dropna().astype(str).unique()

        return distinct_strings

    except Exception as e:
        print("Error:", e)
        return None
# --------------------------------------------------------------------------

excel_file_path= 'bukhari.xlsx'
sheet_name  = 'Sheet1'
column_name = 'Chapter_Arabic'                    # Replace with the actual column name you want to extract from

distinct_strings = get_distinct_strings_from_column(excel_file_path, sheet_name, column_name)

# array of strings
i=1
if distinct_strings is not None:
    print("Distinct Strings:")
    for string in distinct_strings:
        print(i,". ",string)
        i+=1

print ("Do you want to chapter wise or the whole data?")
print ("1 for chapter wise..")
print ("2 for the whole data..")


choice =int (input())
while choice <1  or choice>2:
    choice = int (input ("Enter a valid number:"))
if choice== 1:
    ans = int(input("Please choose a chapter?"))

    print("The ans is ", ans)
    while ans < 1 or ans > distinct_strings.size:
        ans = int(input("Enter a valid number:"))

print("End of col reading")





