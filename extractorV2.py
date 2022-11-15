import pandas as pd
import os

folders = ["ZAsmt", "ZTrans"]

ZAsmt = ["AdditionalPropertyAddress", "BKManagedSpecific", "Building", "BuildingAreas", "MailAddress", "Main", "Name", "SaleData", "TaxDistrict", "TaxExemption", "TypeConstruction", "Value"]
ZTrans = ["BKManagedSpecific", "BuyerMailAddress", "BuyerName", "ForeclosureNameAddress", "Main", "SellerMailAddress", "SellerName", "SellerNameDescriptionCode"]

file_layout = {"ZAsmt": ZAsmt, "ZTrans": ZTrans}
vars_interest = {"Main": ["ImportParcelID", "RowID", "TransID", "AssessorParcelNumber", "State", "County", "PropertyCity", "PropertyZip", "PropertyZip4", "PropertyAddressCensusTrackAndBlock",
            "OriginalPropertyFullStreetAddress", "PropertyAddressLatitude", "PropertyAddressLongitude", "PropertyZoningSourceCode", "TaxIDNumber", "TaxAmount", "TaxYear", "TaxDelinquencyFlag",
            "TaxDelinquencyAmount", "TaxDelinquencyYear", "LotSizeSquareFeet", "ValueCertDate", "DocumentDate", "DocumentTypeStndCode", "LoanAmount", "LoanAmountStndCode", "MaximumLoanAmount",
            "LoanTypeClosedOpenEndStndCode", "LoanTypeFutureAdvancedFlag", "LoanTypeProgramStndCode", "LoanRateTypeStndCode", "LoanDueDate", "LoanTermMonths", "LoanTermYears"],
            "Building": ["PropertyCountyLandUseCode", "YearBuilt", "ArchitecturalStyleStndCode", "Number of beedroom", "Number of Bathroom", "Number of stories", "Number of Rooms", "Number of units NoOfUnits"],
            "BuildingArea": ["BuildingAreaSqft"], "SaleData": ["SalePriceAmount, BuyerFullName", "DocumentDate"], "Value": ["LandAssessedValue", "ImprovementAssessedValue", "TotalAssessedValue",
            "AssessmentYear", "TotalMarketValue", "LandAppraisalData", "TotalAppraisalValue", "AppraisalValueYear", "SalesPriceAmount"], "BuyerName": ["BuyerIndividualFullName",
            "BuyerNonIndividualName"], "BuyerMailAddress": ["BuyerMailFullStreetAddress", "BuyerMailCity", "BuyerMailState", "BuyerMailZip", "BuyerMailZip4", "BuyerMailAddressCensusTrackAndBlock"],
            "SellerMailAddress": ["SellerIndividualFullName", "SellerNonIndividualName", "SellerMailFullStreetAddress", "SellerMailCity", "SellerMailState", "SellerMailZip", "SellerMailZip4",
            "SellerMailAddressLatitude", "SellerMailAddressLongitude", "SellerMailAddressCensusTrackAndBlock"], "BKManagedSpecific": ["DeedTransType"], "ForeClosureNameAddress": ["FCMailIndividualFullName",
            "FCMailNonIndividualName", "FCMailFullStreetAddress", "FCMailCity", "FCMailState", "FCMailZip", "FCMailZip4"]}


def insert_headers(folder, file, columns):
    #Removes the 'ut' at the beginning of the file name, which was the format given in the layout file
    curr_file = file[2:]

    if curr_file not in vars_interest.keys():
        return None

    #Creates a DF of the current file
    try:
        file_df = pd.read_csv('' + folder + '\\' + curr_file + '.txt', sep='|', on_bad_lines='skip', low_memory=False, encoding='latin-1', header=None)
        print(curr_file, " opened successfully.")
        print("")
    except Exception as e:
        print(curr_file, " cannot be accessed. Skipping...")
        print(e)
        print("")
        return None

    #Adds column names to the DF
    file_df.columns = columns
    
    for column in columns:
        if column not in vars_interest[curr_file]:
            file_df.drop(column, axis=1)

    return file_df


def add_headers(files_df, folder):
    #Determines which separate excel layout file to use. Layout files contain a list of headers for each file within the folder.
    if folder == "ZAsmt":
        layout_file = pd.read_excel('asmt_layout.xlsx')
    else:
        layout_file = pd.read_excel('trans_layout.xlsx')

    #List of file names in given folder; file names are repeated once in the resultant list for each variable they have.
    #Data is taken from the layout file.
    #Example: if BuyerName has 6 variables, it will be repeated in file_names 6 times. This will make a later operation easier.
    file_names = (layout_file["TableName"].to_numpy()).tolist()

    #List of column names taken from the "FieldName" column of the layout file.
    column_headers = (layout_file["FieldName"].to_numpy()).tolist()

    #Initialized a dictionary with each file name being a key
    file_col_headers = dict.fromkeys(file_names)

    for key in file_col_headers:
        file_col_headers[key] = []
    
    #Determines the file's associated column and places it in a list on the associated dict key
    total_var_count = 0
    for file in file_names:
        file_col_headers[file].append(column_headers[total_var_count])
        total_var_count += 1

    #file_col_headers now contains a complete dict with key 'ut' + Filename (how the layout file formats the name)
    #and values equal to a list of column names.
    
    #log
    print(folder, total_var_count, ": This number should be equal to the number of rows in the layout file (for the given folder) minus 1")
    print("")

    #
    for file in file_col_headers.keys():
        curr_df = insert_headers(folder, file, file_col_headers[file])
        files_df.append(curr_df)
    return files_df
    


# ----------------
# MAIN
# ----------------

files_df = []
folder = "ZAsmt"

#for folder in folders:
    #DF containing all working data files, will be combined at ends
files_df = add_headers(files_df, folder)

#Combine files_df (merge files on key)
#-----------------
final_df = pd.concat(files_df)

print("Writing to file...")
final_df.to_csv("out.csv")