from utils import generate_x_length_number


def generate_company_prefix(length=7) -> str:
    if isinstance(length, int) == False or length < 6 or length > 12:
        raise ValueError("length must be an int between 6 and 12")

    if length >= 7:
        company_prefix = "0" + generate_x_length_number(length - 1)
    else:
        company_prefix = generate_x_length_number(length)

    return company_prefix
