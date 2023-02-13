"""Tasks running the core analyses."""

import pickle

import pandas as pd
import pytask

from epp_final.analysis.predict import data_processing, gen_plot_data, year_data_split
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
