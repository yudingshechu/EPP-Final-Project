"""Tasks running the core analyses."""

import pickle

import pandas as pd
import pytask

from epp_final.analysis.predict import (
    data_processing,
    gen_plot_data,
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
    """Fit a linear regression model (Python version)."""
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
    data = pd.read_csv(depends_on["data"])
    dataprocessed = data_processing(data)
    year_data = year_data_split(dataprocessed)
    dfa3_regional, dfpesr_regional = rural_urban_dataframe(year_data)
    with open(produces["produces1"], "wb") as f:
        pickle.dump(dfa3_regional, f)
    with open(produces["produces2"], "wb") as f:
        pickle.dump(dfpesr_regional, f)
