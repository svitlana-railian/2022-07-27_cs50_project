import sys
import re
import csv
from datetime import datetime
import pandas as pd


# Main function
def main():
    # To check if file "drugs.csv" exists
    file_check()

    # To choose one option from 5 possible options
    chose_option = input("Would you like to 1) Add DRUG, 2) Modify expiry registration date of the DRUG, 3) Browse DRUG, 4) Browse COUNTRY or 5) Browse EXPIRY YEAR of registration?\nPress 1, 2, 3, 4 or 5: ")

    # Based on the output (from 1 to 5), the program will run further or quit if invalid number is typed
    if chose_option == str(1):
        drug_name = input("Name of the drug: ")
        dosage_strength = input("Dosage Strength: ")
        dosage_form = input("Dosage Form: ")
        add_new_drug_info = add_new_drug(drug_name, dosage_strength, dosage_form)
        print(add_new_drug_info)

    elif chose_option == str(2):
        drug_name = input("Name of the drug: ")
        dosage_strength = input("Dosage Strength: ")
        dosage_form = input("Dosage Form: ")
        country_name = input("Type country: ")
        expiry_date = input("Expiry date of Registration YYYY-MM-DD: ")
        modify_drug_info = modify_drug(drug_name, dosage_strength, dosage_form, country_name, expiry_date)
        print(modify_drug_info)

    elif chose_option == str(3):
        browse_drug_info = browse_drug(input("Type name of drug: "))
        print(browse_drug_info)

    elif chose_option == str(4):
        browse_country_info = browse_country(input("Type country: "))
        print(browse_country_info)

    elif chose_option == str(5):
        browse_exp_year_info = browse_exp_year(input("Type YEAR: "))
        print(browse_exp_year_info)

    else:
        sys.exit("Invalid number")




# Option 1 - Function: add_new_drug
def add_new_drug(drug_name, dosage_strength, dosage_form):

    # Create default list containing 1 dictionary with keys == fieldnames (correspond to the 1st line of the file) and all values == None
    default_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for fieldname in fieldnames:
            default_list.append({fieldname: "None"})

    # Get values from the user and assign them to the corresponding keys
    drug_name = drug_name.title().strip()
    dosage_strength = dosage_strength_check(dosage_strength)
    dosage_form = dosage_form_check(dosage_form)

    default_list[0] = {"Drug": drug_name}
    default_list[1] = {"Dosage Strength": dosage_strength}
    default_list[2] = {"Dosage Form": dosage_form}

    # Extract this dictionary from the list
    dict = {key: value for dict in default_list for key, value in dict.items()}

    # Add this dictionary to the file as one row
    with open("drugs.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(dict)

    # Popup successful message
    return "Drug was added to the file"




# Option 2 - Function: modify_drug
def modify_drug(drug_name, dosage_strength, dosage_form, country_name, expiry_date):

    # Get values from the user: drug_name, dosage_strength, dosage_form - To find needed drug; country_name - To find country where we want to modify expiry registration date; expiry_date - To add expiry registration date
    drug_name = drug_name.title().strip()
    dosage_strength = dosage_strength_check(dosage_strength)
    dosage_form = dosage_form_check(dosage_form)
    country_name = country_check(country_name)
    expiry_date = date_check(expiry_date)

    # Read the content of a file and extract 1 row (drug in which the expiry date will be modified) as dict and append it to the list
    drug_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        for dict_row in reader:
            if dict_row["Drug"] == drug_name and dict_row["Dosage Strength"] == dosage_strength and dict_row["Dosage Form"] == dosage_form:
                drug_list.append(dict_row)

    # Check the content of the list. Should contain 1 element (1 dictionary)
    if len(drug_list) == 1:
        pass
    else:
        sys.exit("Drug was not found")

    # To re-write the expiry date by assigning new value to the dict key. drug_list[0] is the first (and only one) element in the list that is also a dictionary. drug_list[0][country_name] is a dict key
    drug_list[0][country_name] = expiry_date

    # To transfer all data of csv file to new list, except 1 row (drug in which the expiry date will be modified)
    file_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for dict_row in reader:
            if dict_row["Drug"] != drug_name and dict_row["Dosage Strength"] != dosage_strength and dict_row["Dosage Form"] != dosage_form:
                file_list.append(dict_row)

    # To write back all data to the csv file, except 1 row (drug in which the expiry date was modified)
    with open("drugs.csv", "w") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_list)

    # To append 1 row (drug in which the expiry date was modified) to the csv file
    with open("drugs.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(drug_list[0])

    # Popup successful message
    return "Expiry date of Drug was updated in the file"



# Option 3 - Function: browse_drug
def browse_drug(drug_name):

    # Get values from the user: drug_name - To find needed drug
    drug_name = drug_name.title().strip()

    # Read the content of a file and extract rows with menioned drug name. Store rows as dictionaries in the list
    drugs_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        for dict_row in reader:
            if dict_row["Drug"] == drug_name:
                drugs_list.append(dict_row)

    # Check the content of the list
    list_length_check(drugs_list, "Drug was not found")

    # Access list of dictionaries and extract data ignoring 'None' values.
    output = [{key: value for key, value in dictionary.items() if value != "None"} for dictionary in drugs_list]

    # To visualise data using DataFrame
    df = pd.DataFrame(output)
    df = df.fillna("-")
    df.index = df.index + 1
    return df



# Option 4 - Function: browse_country
def browse_country(country_name):

    # Get values from the user: country_name - To find needed country and check if country is in the file
    country_name = country_check(country_name)

    # Read the content of the file and extract rows with menioned country name. Store rows as dictionaries in the list
    drugs_in_country_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        for dict_row in reader:
            if dict_row[country_name] != "None":
                drugs_in_country_list.append(dict_row)

    # Check the content of the list
    list_length_check(drugs_in_country_list, f"Drugs are not registered in {country_name}")

    # To visualise data using DataFrame
    df = pd.DataFrame(drugs_in_country_list)
    df = df[["Drug", "Dosage Strength", "Dosage Form", country_name]]
    df.index = df.index + 1
    return df



# Option 5 - Function: browse_exp_year
def browse_exp_year(year):

    # Get values from the user: expiry year
    year = year.strip()

    # Read the content of the file and extract rows with menioned expiry year. Store rows as dictionaries in the list
    drugs_exp_year_list = []
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        for dict_row in reader:
            for key, value in dict_row.items():
                if value.startswith(year):
                    drugs_exp_year_list.append(dict_row)

    # Check the content of the list
    list_length_check(drugs_exp_year_list, f"Drugs were not found with expiry year of: {year}")

    # Access list of dictionaries and extract data 1) omitting 'None' values 2) omitting expiry year that is out of the interest
    first_output = [{key: value for key, value in dictionary.items() if value != "None"} for dictionary in drugs_exp_year_list]
    second_output = [{key: value for key, value in dictionary.items() if value == dictionary["Drug"] or value == dictionary["Dosage Strength"] or value == dictionary["Dosage Form"] or value.startswith(year)} for dictionary in first_output]


    # To visualise data using DataFrame
    df = pd.DataFrame(second_output)
    df = df.fillna("-")
    df.index = df.index + 1
    return df




# Additional check Function: list_check
def list_length_check(list, error_message):
    if len(list) > 0:
        pass
    else:
        sys.exit(error_message)


# Additional check Function: date_check
def date_check(date):
    date = date.strip()
    match = re.search(r"^([0-9]){4}-([0-9]){2}-([0-9]){2}$", date)
    if not match:
        sys.exit("Invalid date format")

    try:
        date = datetime.strptime(date, "%Y-%m-%d") # check date correctness
        date = date.strftime("%Y-%m-%d")           # convert date type to str type
    except ValueError:
        sys.exit("Invalid date")

    return date


# Additional check Function: file_check
def file_check():
    try:
        file = open("drugs.csv")
        file.close()
    except FileNotFoundError:
        sys.exit("File 'drugs.csv' was not found")


# Additional check Function: country_check
def country_check(country_name):
    country_name = country_name.title().strip()
    with open("drugs.csv", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        if country_name not in fieldnames:
            sys.exit("Country was not found.\nThe list of available countries: Austria, Belgium, Bulgaria, Croatia, Republic of Cyprus, Czech Republic, Denmark, Estonia, Finland, France, Germany, Greece, Hungary, Ireland, Italy, Latvia, Lithuania, Luxembourg, Malta, Netherlands, Poland, Portugal, Romania, Slovakia, Slovenia, Spain, Sweden")
        else:
            return country_name


# Additional check Function: Dosage_Strength_check
def dosage_strength_check(dosage_strength):
    dosage_strength = dosage_strength.lower().strip()
    match = re.search(r"^[0-9]", dosage_strength)
    if not match:
        sys.exit("Dosage Strength should contain number")
    return dosage_strength


# Additional check Function: Dosage_Form_check
def dosage_form_check(dosage_form):
    dosage_form = dosage_form.lower().strip()
    match = re.search(r"^[a-z]", dosage_form)
    if not match:
        sys.exit("Dosage Form should contain letters")
    return dosage_form


if __name__ == "__main__":
    main()

