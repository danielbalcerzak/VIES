# Pierwszy sposob

"""from pyVies import api

def check_response(obj, county_code, vat_number):
    result = obj.request(vat_number, county_code)
    return result

def main():
    vies = api.Vies()
    answer = "y"
    while answer == "y".lower():
        country_code = input("Enter country code: ")
        vat_number = input("Enter VAT number: ")

        try:
            response = check_response(vies, country_code, vat_number)
            if response["valid"] == 1:
                print(response)
            else:
                print("There is no trader in VIES system")
        except api.ViesValidationError:
            print("Invalid input data")
        finally:
            print("--------------------------------")

        answer = input("If you want to try again press [Y] ")

if __name__ == '__main__':
    main()
"""

# ("6390845P", "IE")

# Drugi sposob

import suds
import re


def check_num_algorithm_valid(country_code, vat_number):
    number_vat_algorithm = {
        'AT': re.compile(r'^U\d{8}$', re.IGNORECASE),
        'BE': re.compile(r'^\d{9,10}$'),
        'BG': re.compile(r'^\d{9,10}$'),
        'CY': re.compile(r'^\d{8}[a-z]$', re.IGNORECASE),
        'CZ': re.compile(r'^\d{8,10}$'),
        'DE': re.compile(r'^\d{9}$'),
        'DK': re.compile(r'^\d{8}$'),
        'EE': re.compile(r'^\d{9}$'),
        'EL': re.compile(r'^\d{9}$'),
        'ES': re.compile(r'^[\da-z]\d{7}[\da-z]$', re.IGNORECASE),
        'FI': re.compile(r'^\d{8}$'),
        'FR': re.compile(r'^[\da-hj-np-z]{2}\d{9}$', re.IGNORECASE),
        'GB': re.compile(r'^((\d{9})|(\d{12})|(GD\d{3})|(HA\d{3}))$', re.IGNORECASE),
        'HR': re.compile(r'^\d{11}$'),
        'HU': re.compile(r'^\d{8}$'),
        'IE': re.compile(r'^((\d{7}[a-z])|(\d[a-z]\d{5}[a-z])|(\d{6,7}[a-z]{2}))$', re.IGNORECASE),
        'IT': re.compile(r'^\d{11}$'),
        'LT': re.compile(r'^((\d{9})|(\d{12}))$'),
        'LU': re.compile(r'^\d{8}$'),
        'LV': re.compile(r'^\d{11}$'),
        'MT': re.compile(r'^\d{8}$'),
        'NL': re.compile(r'^\d{9}B\d{2,3}$', re.IGNORECASE),
        'PL': re.compile(r'^\d{10}$'),
        'PT': re.compile(r'^\d{9}$'),
        'RO': re.compile(r'^\d{2,10}$'),
        'SE': re.compile(r'^\d{12}$'),
        'SI': re.compile(r'^\d{8}$'),
        'SK': re.compile(r'^\d{10}$'),
    }
    if country_code not in number_vat_algorithm.keys():
        print("Invalid country code")
        raise ValueError('Invalid country code')

    if len(vat_number) > 2:
        if vat_number[:2].upper() == country_code:
            vat_number = vat_number[2:]

    if not number_vat_algorithm[country_code].match(vat_number):
        print("Invalid VAT number")
        raise ValueError("Invalid VAT number")


def not_exist(result):
    response = str(result)
    if response.find("False") == -1:
        return False
    else:
        return True


def main():
    url = "https://ec.europa.eu/taxation_customs/vies/checkVatService.wsdl"
    country_code = input("Enter country code: ")
    vat_number = input("Enter VAT number: ")
    client = suds.Client(url)
    #print(client)

    try:
        check_num_algorithm_valid(country_code, vat_number)
        result = client.service.checkVat(country_code, vat_number)
        if not_exist(result):
            print("There is no trader in VIES system")
        else:
            print(result)
    except ValueError:
        print("Invalid input data")
    finally:
        print("----------------------------")


if __name__ == '__main__':
    main()
