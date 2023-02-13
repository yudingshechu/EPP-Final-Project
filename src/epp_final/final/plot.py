"""Functions plotting results."""


def reformat_data(data):
    """Reformat data into separated lists.

    Args:
        data (dict): regression coefficients

    Returns:
        list: list of coefficients for different years.

    """
    Pesr_all = []
    a3_all = []
    for i in range(980, 991):
        Pesr_all.append(data[f"{i}"][4])
        a3_all.append(data[f"{i}"][3])
    return a3_all, Pesr_all
