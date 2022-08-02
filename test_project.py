import sys
import re
import csv
from datetime import datetime
import pandas as pd
from project import add_new_drug, modify_drug, browse_drug, browse_country, browse_exp_year, list_length_check, date_check, country_check, dosage_strength_check, dosage_form_check
import pytest
import datatest as dt

# !!!!! Before running: "pytest test_project.py" make sure you delete row in file drugs.csv - Test Drug,50 mg,dragee,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,2050-05-20
# Otherwise pytest will throw some Errors. 

def test_list_length_check():
    assert list_length_check([1, 2, 3], "ErrorMessage") == None

def test_list_length_check_Error():
    with pytest.raises(SystemExit):
        list_length_check([], "ErrorMessage")



def test_date_check():
    assert date_check("2020-10-20") == "2020-10-20"
    assert date_check("   2020-10-20  ") == "2020-10-20"

def test_date_check_DateFormatError():
    with pytest.raises(SystemExit):
        date_check("20-10-2020")

def test_date_check_ValueError():
    with pytest.raises(SystemExit):
        date_check("2020-00-10")
    with pytest.raises(SystemExit):
        date_check("2020-13-10")
    with pytest.raises(SystemExit):
        date_check("2020-01-00")
    with pytest.raises(SystemExit):
        date_check("2020-12-32")



def test_country_check():
    assert country_check("Belgium") == "Belgium"
    assert country_check("latvia") == "Latvia"
    assert country_check("  denmark  ") == "Denmark"

def test_country_check_Error():
    with pytest.raises(SystemExit):
        country_check("Ukraine")



def test_dosage_strength_check():
    assert dosage_strength_check("0.5 g") == "0.5 g"
    assert dosage_strength_check("1 G") == "1 g"
    assert dosage_strength_check("100 mg") == "100 mg"

def test_dosage_strength_check_Error():
    with pytest.raises(SystemExit):
        dosage_strength_check("tablet")



def test_dosage_form_check():
    assert dosage_form_check("tablet") == "tablet"
    assert dosage_form_check("Tablet") == "tablet"
    assert dosage_form_check("TABLET") == "tablet"

def test_dosage_form_check_Error():
    with pytest.raises(SystemExit):
        dosage_form_check("1 g")



def test_add_new_drug():
    assert add_new_drug("test drug", "50 mg", "dragee") == "Drug was added to the file"



def test_modify_drug():
    assert modify_drug("test drug", "50 mg", "dragee", "test country", "2050-05-20") == "Expiry date of Drug was updated in the file"

def test_modify_drug_Error_name():
    with pytest.raises(SystemExit):
        modify_drug("drug", "50 mg", "dragee", "test country", "2050-05-20")

def test_modify_drug_Error_dosage_strength():
    with pytest.raises(SystemExit):
        modify_drug("test drug", "100 mg", "dragee", "test country", "2050-05-20")

def test_modify_drug_Error_dosage_form():
    with pytest.raises(SystemExit):
        modify_drug("test drug", "50 mg", "tablet", "test country", "2050-05-20")

def test_modify_drug_Error_country():
    with pytest.raises(SystemExit):
        modify_drug("test drug", "50 mg", "dragee", "Ukraine", "2050-05-20")

def test_modify_drug_Error_date():
    with pytest.raises(SystemExit):
        modify_drug("test drug", "50 mg", "dragee", "test country", "2050-00-00")


# For "Test Drug" browse_drug(), browse_country() & browse_exp_year() functions will return the same data output
def test_browse_drug_columns():
    dt.validate(browse_drug("test drug").columns, {"Drug", "Dosage Strength", "Dosage Form", "Test Country"},)

def test_browse_drug_exp_date():
    dt.validate.regex(browse_drug("test drug")["Test Country"], r"^([0-9]){4}-([0-9]){2}-([0-9]){2}$")

def test_browse_drug_data_type():
    dt.validate(browse_drug("test drug")["Drug"], str)
    dt.validate(browse_drug("test drug")["Dosage Strength"], str)
    dt.validate(browse_drug("test drug")["Dosage Form"], str)
    dt.validate(browse_drug("test drug")["Test Country"], str)

def test_browse_drug_superset():
    dt.validate(browse_drug("test drug")["Drug"], {"Test Drug"})
    dt.validate(browse_drug("test drug")["Dosage Strength"], {"50 mg"})
    dt.validate(browse_drug("test drug")["Dosage Form"], {"dragee"})
    dt.validate(browse_drug("test drug")["Test Country"], {"2050-05-20"})

def test_browse_country_no_drug_match():
    with pytest.raises(SystemExit):
        browse_exp_year("drug")



def test_browse_country_columns():
    dt.validate(browse_country("test country").columns, {"Drug", "Dosage Strength", "Dosage Form", "Test Country"},)

def test_browse_country_exp_date():
    dt.validate.regex(browse_country("test country")["Test Country"], r"^([0-9]){4}-([0-9]){2}-([0-9]){2}$")

def test_browse_country_data_type():
    dt.validate(browse_country("test country")["Drug"], str)
    dt.validate(browse_country("test country")["Dosage Strength"], str)
    dt.validate(browse_country("test country")["Dosage Form"], str)
    dt.validate(browse_country("test country")["Test Country"], str)

def test_browse_country_superset():
    dt.validate(browse_country("test country")["Drug"], {"Test Drug"})
    dt.validate(browse_country("test country")["Dosage Strength"], {"50 mg"})
    dt.validate(browse_country("test country")["Dosage Form"], {"dragee"})
    dt.validate(browse_country("test country")["Test Country"], {"2050-05-20"})

def test_browse_country_no_country_match():
    with pytest.raises(SystemExit):
        browse_exp_year("Ukraine")



def test_browse_exp_year_columns():
    dt.validate(browse_exp_year("2050").columns, {"Drug", "Dosage Strength", "Dosage Form", "Test Country"},)

def test_browse_exp_year_exp_date():
    dt.validate.regex(browse_exp_year("2050")["Test Country"], r"^([0-9]){4}-([0-9]){2}-([0-9]){2}$")

def test_browse_exp_year_data_type():
    dt.validate(browse_exp_year("2050")["Drug"], str)
    dt.validate(browse_exp_year("2050")["Dosage Strength"], str)
    dt.validate(browse_exp_year("2050")["Dosage Form"], str)
    dt.validate(browse_exp_year("2050")["Test Country"], str)

def test_browse_exp_year_superset():
    dt.validate(browse_exp_year("2050")["Drug"], {"Test Drug"})
    dt.validate(browse_exp_year("2050")["Dosage Strength"], {"50 mg"})
    dt.validate(browse_exp_year("2050")["Dosage Form"], {"dragee"})
    dt.validate(browse_exp_year("2050")["Test Country"], {"2050-05-20"})

def test_browse_exp_year_no_year_match():
    with pytest.raises(SystemExit):
        browse_exp_year("3050")

