from utils import generate_x_length_number, calculate_check_digit
from companies import generate_company_prefix


def generate_gln(company_prefix=None, company_prefix_length=None) -> str:
    if company_prefix is None and company_prefix_length is None:
        raise ValueError("company_prefix and company_prefix_length cannot be both None")

    if company_prefix is not None and (
            company_prefix.isdigit() == False or len(company_prefix) < 6 or len(company_prefix) > 12):
        raise ValueError("company_prefix must be a string containing from 6 to 12 digits")

    elif company_prefix is None:
        company_prefix = generate_company_prefix(company_prefix_length)

    location_reference_length = 12 - len(company_prefix)
    location_reference = generate_x_length_number(location_reference_length)
    check_digit = calculate_check_digit(company_prefix + location_reference)

    return company_prefix + location_reference + check_digit


def generate_sgln(serial: str, gln=None, company_prefix=None, company_prefix_length=None) -> str:
    if serial is None or serial.isdigit() == False:
        raise ValueError("serial must be a digit string")

    if company_prefix is None and company_prefix_length is None:
        raise ValueError("Either company_prefix or just company_prefix_length must be informed")

    if gln is not None and (gln.isdigit() == False or len(gln) != 14):
        raise ValueError("gln must be a string with 13 digits")

    elif company_prefix is None and company_prefix_length is not None:
        company_prefix = generate_company_prefix(company_prefix_length)

    if gln is None:
        gln = generate_gln(company_prefix)

    gs1_id = gln.replace(company_prefix, "")
    sgln = f"urn:epc:id:sgln:{company_prefix}.{gs1_id[:-1]}.{serial}"
    return sgln
