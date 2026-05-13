import numpy as np  # type: ignore
from scripts.vars import *


def significant_round(x, sig=1):
    """Round to significant digits"""
    if x == 0:
        return 0
    return round(x, sig - int(np.floor(np.log10(abs(x)))) - 1)


def round_error(err):
    """Round error to 1 significant digit, or 2 if first digit is 1"""
    if err == 0:
        return 0

    first_digit = int(str(abs(err)).replace(".", "").lstrip("0")[0])

    sig_digits = 2 if first_digit == 1 else 1
    return significant_round(err, sig_digits)


def match_decimal_places(mean, err):
    """Round mean to same decimal precision as error"""
    err_str = f"{err:.10f}".rstrip("0")
    if "." in err_str:
        decimals = len(err_str.split(".")[1])
    else:
        decimals = 0

    return round(mean, decimals)
