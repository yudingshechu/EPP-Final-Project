"""Tasks running the core analyses."""

import pickle

import pandas as pd
import pytask

from epp_final.analysis.predict import (
    data_processing,
    gen_plot_data,
    gen_plot_data_control,
    rural_urban_dataframe,
    year_data_split,
)
from epp_final.config import BLD


@pytask.mark.depends_on(
    {
        "scripts": ["predict.py"],
        "data": BLD / "python" / "data" / "data1990_raw.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "models" / "coef1990.pickle")
def task_fit_model_1990(depends_on, produces):
    """Fit a linear regression model (without controls and regional split)."""
    data = pd.read_csv(depends_on["data"])
    dataprocessed = data_processing(data)
    year_data = year_data_split(dataprocessed)
    coef = gen_plot_data(year_data)
    with open(produces, "wb") as f:
        pickle.dump(coef, f)


@pytask.mark.depends_on(
    {
        "scripts": ["predict.py"],
        "data": BLD / "python" / "data" / "data1990_raw.csv",
    },
)
@pytask.mark.produces(
    {
        "produces1": BLD / "python" / "models" / "dfa3_regional.pickle",
        "produces2": BLD / "python" / "models" / "dfpesr_regional.pickle",
    },
)
def task_urabn_rural_data(depends_on, produces):
    """Fit regression model for rural and urban regions separately."""
    data = pd.read_csv(depends_on["data"])
    dataprocessed = data_processing(data)
    year_data = year_data_split(dataprocessed)
    dfa3_regional, dfpesr_regional = rural_urban_dataframe(year_data)
    with open(produces["produces1"], "wb") as f:
        pickle.dump(dfa3_regional, f)
    with open(produces["produces2"], "wb") as f:
        pickle.dump(dfpesr_regional, f)


@pytask.mark.depends_on(
    {
        "scripts": ["predict.py"],
        "data": BLD / "python" / "data" / "Sample2.csv",
    },
)
@pytask.mark.produces(
    {"produces1": BLD / "python" / "models" / "dfa3_control.pickle"},
)
def task_data_with_control(depends_on, produces):
    """Fit a regression model with educational controls."""
    data = pd.read_csv(depends_on["data"])
    year_data = year_data_split(data)
    X_variables_c = data.columns[[2, 8, 9, 11, 12, 13, 15, 16, 17, 3]]
    dfa3_control = gen_plot_data_control(year_data, X_variables_c)
    with open(produces["produces1"], "wb") as f:
        pickle.dump(dfa3_control, f)


@pytask.mark.depends_on(
    {
        "scripts": ["predict.py"],
        "data": BLD / "python" / "data" / "Sample2.csv",
    },
)
@pytask.mark.produces(
    {
        "produces1": BLD / "python" / "models" / "dfa3_regional_control.pickle",
        "produces2": BLD / "python" / "models" / "dfpesr_regional_control.pickle",
    },
)
def task_urabn_rural_control(depends_on, produces):
    """Fit regression model with educational controls for rural and urban."""
    data = pd.read_csv(depends_on["data"])
    year_data = year_data_split(data)
    X_variables_c = data.columns[[2, 8, 9, 11, 12, 13, 15, 16, 17, 3]]
    dfa3_regional_c, dfpesr_regional_c = rural_urban_dataframe(year_data, X_variables_c)
    with open(produces["produces1"], "wb") as f:
        pickle.dump(dfa3_regional_c, f)
    with open(produces["produces2"], "wb") as f:
        pickle.dump(dfpesr_regional_c, f)
