"""Functions for predicting outcomes based on the estimated model."""

import numpy as np
from sklearn.linear_model import LinearRegression


def data_processing(data):
    """Basic data processing for 1990 data.

    Args:
        data (pd.DataFrame): 1990 raw data.

    Returns:
        pd.DataFrame: Processed data for this study.

    """
    data["CN1990A_SEX"].replace({2: 0}, inplace=True)
    data["CN1990A_NATION"].replace(list(range(2, 100)), 0, inplace=True)
    data["CN1990A_HHTYA"].replace([2, 9], 0, inplace=True)
    data.drop(data[data["CN1990A_RELATE"] != 3].index, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data.drop(data[data["CN1990A_BIRTHY"] < 973].index, inplace=True)
    data.reset_index(drop=True, inplace=True)
    data["Treat"] = np.zeros(data.shape[0], dtype="int")
    data.loc[data["CN1990A_BIRTHY"] > 979, "Treat"] = 1
    data["OneChildInteract"] = data["Treat"] * data["CN1990A_NATION"]
    return data


def _PESR(a0, a1, a2, a3):
    """The policy ef fect on sex ratio (PESR), male number over 100 female.

    Args:
        a0 (float): intercept
        a1 (float): Han effect
        a2 (float): 1979 dummy
        a3 (float): One child policy on Han after 1979

    Returns:
        PES: policy effect on sex ratio

    """
    PES = 100 * (
        ((a0 + a1 + a2 + a3) / (1 - a0 - a1 - a2 - a3) - (a0 + a1) / (1 - a0 - a1))
        - ((a0 + a2) / (1 - a0 - a2) - a0 / (1 - a0))
    )
    return PES


def year_data_split(data):
    """Split data by year.

    Args:
         data (pd.DataFrame): 1990 processed data.

    Returns:
         dict: Split data by years.

    """
    compare = (data["CN1990A_BIRTHY"] <= 979) * (data["CN1990A_BIRTHY"] >= 973)
    year_data = {}
    for i in range(980, 991):
        year_data[f"Birth{i}"] = data[(data["CN1990A_BIRTHY"] == i) + compare].copy()
    return year_data


def gen_plot_data(data):
    """Generate data used for plot.

    Args:
        data (dict): data split by year.

    Returns:
        dict: regression coefficients

    """
    X_variables = ["CN1990A_NATION", "Treat", "OneChildInteract"]
    year_results_all = {}
    for i in range(980, 991):
        workdf = data[f"Birth{i}"].copy()
        Obs = workdf.shape[0]
        Y = workdf["CN1990A_SEX"].values.reshape(Obs, 1)
        X = workdf[X_variables].values.reshape(Obs, 3)
        reg_all = LinearRegression().fit(X, Y)
        a0 = reg_all.intercept_[0]
        a1, a2, a3 = reg_all.coef_[0]
        Pesr = _PESR(a0, a1, a2, a3)
        year_results_all[f"{i}"] = [a0, a1, a2, a3, Pesr]
    return year_results_all
