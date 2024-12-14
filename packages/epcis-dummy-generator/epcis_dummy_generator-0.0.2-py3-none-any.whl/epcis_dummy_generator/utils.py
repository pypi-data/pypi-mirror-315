from random import randint

def generate_x_length_number(x: int) -> str:
    number = ""
    for i in range(x):
        number += str(randint(0, 9))

    return number

def calculate_check_digit(base: str) -> str:
    weights = [3 if i % 2 == 0 else 1 for i in range(len(base))]
    total = sum(int(digit) * weight for digit, weight in zip(reversed(base), weights))
    remainder = total % 10
    return str(10 - remainder) if remainder != 0 else "0"