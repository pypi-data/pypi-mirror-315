from utils import generate_x_length_number, calculate_check_digit
from companies import generate_company_prefix


def generate_gtin(company_prefix=None, company_prefix_length=None) -> str:
    if company_prefix is None and company_prefix_length is None:
        raise ValueError("company_prefix and company_prefix_length cannot be both None")

    if company_prefix is not None and (
            company_prefix.isdigit() == False or len(company_prefix) < 6 or len(company_prefix) > 12):
        raise ValueError("company_prefix must be a string containing from 6 to 12 digits")

    elif company_prefix is None:
        company_prefix = generate_company_prefix(company_prefix_length)

    gs1_id_length = 13 - len(company_prefix)
    gs1_id = generate_x_length_number(gs1_id_length)
    check_digit = calculate_check_digit(company_prefix + gs1_id)

    return gs1_id[0] + company_prefix + gs1_id[1:] + check_digit


def get_company_prefix_and_gs1_id_from_gtin(gtin: str, company_prefix_length: int):
    if gtin is None or company_prefix_length is None:
        raise ValueError("gtin and company_prefix_length must both be informed")

    if isinstance(company_prefix_length, int) == False or company_prefix_length < 6 or company_prefix_length > 12:
        raise ValueError("company_prefix_length must be an int between 6 and 12")

    gs1_id = gtin[0] + gtin[company_prefix_length + 1:]
    gcp = gtin[1:company_prefix_length + 1]

    return {"gs1_id": gs1_id, "company_prefix": gcp}


def generate_sgtin(serial: str, gtin=None, company_prefix=None, company_prefix_length=None) -> str:
    if serial is None or serial.isdigit() == False:
        raise ValueError("serial must be a digit string")

    if company_prefix is None and company_prefix_length is None:
        raise ValueError("Either company_prefix or just company_prefix_length must be informed")

    if gtin is not None and (gtin.isdigit() == False or len(gtin) != 14):
        raise ValueError("gtin must be a string with 14 digits")

    elif company_prefix is None and company_prefix_length is not None:
        company_prefix = generate_company_prefix(company_prefix_length)

    if gtin is None:
        gtin = generate_gtin(company_prefix)

    gs1_id = gtin.replace(company_prefix, "")
    sgtin = f"urn:epc:id:sgtin:{company_prefix}.{gs1_id[:-1]}.{serial}"
    return sgtin
