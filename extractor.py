import pandas as pd

folders = ["ZAsmt", "ZTrans"]

ZAsmt = ["AdditionalPropertyAddress", "BKManagedSpecific", "Building", "BuildingAreas", "MailAddress", "Main", "Name", "SaleData", "TaxDistrict", "TaxExemption", "TypeConstruction", "Value"]
ZTrans = ["BKManagedSpecific", "BuyerMailAddress", "BuyerName", "ForeclosureNameAddress", "Main", "SellerMailAddress", "SellerName", "SellerNameDescriptionCode"]

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

layouts = [asmt_layout, trans_layout]

def add_headers_per_layout(files_df, folder, layout_file):
    layout_file = pd.read_excel(layout_file + '.xlsx')

    #list of file names
    files = (layout_file["TableName"].to_numpy()).tolist()
    #list of columns
    column_headers = (layout_file["FieldName"].to_numpy()).tolist()
    file_col_headers = dict.fromkeys(files)
    for key in file_col_headers:
        file_col_headers[key] = []

    #creates a dictionary with files and their associated column headers
    for index, file in enumerate(files):
        file_col_headers[file].append(column_headers[index])

    #add column headers to the files
    #-----------------

    for file in folder:
        curr_file = pd.read_csv(folder + '\\' + file + '.txt', sep='|', header=None)
        curr_file.columns = file_col_headers["ut" + file]
        curr_file = curr_file[vars_interest[file]]
        files_df.append(curr_file)


def add_headers(files_df, folder):
    #get column headers and the file they are associated with
    #-----------------
    for layout_file in layouts:
        add_headers_per_layout(files_df, folder, layout_file)


for folder in folders:
    files_df = []
    add_headers(files_df, folder)

#merge files on key
#-----------------
final_df = pd.concat(files_df)
print(final_df.head)
