# **REGISTRATION STATUSES OF DRUGS (MEDICINAL PRODUCTS)**

## Video Demo:  <URL https://www.youtube.com/watch?v=XmiTP9TJxVg>

## **The Project Description:**
The project was designed to fulfill the needs of pharmaceutical industry and aim to properly maintain the data, in particular to: store data; access data; modify data, if needed; and analyse data. The main focus was made on drugs (medicinal products) that are registered or not registered in certain countries. All data are stored in csv file. Drugs have attributes, such as drug name, dosage strength (*e.g.* 10 mg, 5 mg/ml *etc.*) and dosage form (*e.g.* tablet, solution for injection, dragee *etc.*). The list of countries was chosen to represent European Union area. The final column is *Test Country* as to properly run pytest. For example, Drug can be registered in France, where the expiry date of registration is mentioned, but not registered in Italy, where value None is written.
## **The Code Composition:**
The code consists of main function whereby prompting user to choose one of 5 available options; 5 functions that implement those options and 6 small checker functions.
### **Main function:**
Main function prompts the user to choose one of 5 available options or quit program if invalid output was typed:
1) Add DRUG,
2) Modify expiry registration date of the DRUG,
3) Browse DRUG,
4) Browse COUNTRY,
5) Browse EXPIRY YEAR of registration.

**Options 1&2** provide possibility for data storage and modification. **Options 3&4** rather give a general statistics and overview. **Option 3** provides information IN HOW MANY COUNTRIES the specific drug is registered. It becomes handy once we want to register the drug in new country that has a requirement on having prior registration in (for example) 3 other countries. So, basically, you are not even allowed to submit registration dossier if the drug doesn`t have a vaid registration in 3 different countries. **Option 4** provides information on HOW MANY DRUGS are registered in specific country. We may have a broad list of registered products in some countries while none registrations in other countries. **Option 5** allows to skim the expiry registration date and plan in advance document preparation for extension of registration, since it is very time consuming process and usually take months.
### **Option 1 - Function: add_new_drug**
Read the csv file and create default list containing 1 dictionary with keys == fieldnames (correspond to the 1st line of the file) and all values == None. Get values from the user (*drug_name, dosage_strength, dosage_form*) and assign them to the corresponding keys. Extract the obtained dictionary from the list and append it to the file as a row. Notify user by popping up successful message.
### **Option 2 - Function: modify_drug**
Get values from the user: *drug_name, dosage_strength, dosage_form* - To find needed drug; *country_name* - To find country where we want to modify expiry registration date; *expiry_date* - To add expiry registration date. Read the content of a file and extract 1 row (drug in which the expiry date will be modified) as dict and append it to the list. Check the content of the list. Should contain 1 element (1 dictionary). To re-write the expiry date by assigning new value to the dict key. drug_list[0] is the first (and only one) element in the list that is also a dictionary. drug_list[0][country_name] is a dict key. To transfer all data of csv file to new list, except 1 row (drug in which the expiry date will be modified). To write back all data to the csv file, except 1 row (drug in which the expiry date was modified). To append 1 row (drug in which the expiry date was modified) to the csv file. Notify user by popping up successful message.
### **Option 3 - Function: browse_drug**
Get values from the user: *drug_name* - To find needed drug. Read the content of a file and extract rows with menioned drug name. Store rows as dictionaries in the list. Check the content of the list. Access list of dictionaries and extract data ignoring 'None' values. Visualise data using DataFrame.
### **Option 4 - Function: browse_country**
Get values from the user: *country_name* - To find needed country and check if country is in the file. Read the content of the file and extract rows with menioned country name. Store rows as dictionaries in the list. Check the content of the list. Visualise data using DataFrame.
### **Option 5 - Function: browse_exp_year**
Get values from the user: *expiry year*. Read the content of the file and extract rows with menioned expiry year. Store rows as dictionaries in the list. Check the content of the list. Access list of dictionaries and extract data 1) omitting 'None' values 2) omitting expiry year that is out of the interest. Visualise data using DataFrame.
### Additional check Function: list_check
Check the content of the list if needed rows were uppanded to it.
### Additional check Function: date_check
Check the date format (YYYY-MM-DD) as well as months(01 -12) and days (01-31).
### Additional check Function: file_check
File is named as drugs.csv.
### Additional check Function: country_check
Check if country listed in the file
### Additional check Function: Dosage_Strength_check
Check dosage strength. Usually starts with numbers. Sometimes this value is not appropriate for drugs, may type 0.
### Additional check Function: Dosage_Form_check
Check dosage form. Starts with letters.

## **Running Pytest**
Pytest checks all implemented functions thus influecing the file composition. The column "Test Country" and row "Test Drug" are added for this purpose.
Before running: **"pytest test_project.py"** make sure you delete row in the file **drugs.csv** - *Test Drug,50 mg,dragee,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,2050-05-20*. Otherwise pytest will throw some Errors. If you run pytest for the first time, this row is absent.