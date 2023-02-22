"""Tasks for managing the data."""

import pandas as pd
import pytask

from epp_final.config import BLD, SRC
from epp_final.data_management.clean_data import (
    clean_data_with_control,
    clean_fig1_data,
    clean_fig2_data,
    clean_raw_data,
    clean_wage_data,
)
from epp_final.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info1990.yaml",
        "data": SRC / "data" / "raw_data.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "data1990_raw.csv")
def task_clean_data_1990(depends_on, produces):
    """Clean the data (Python version)."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    data = clean_raw_data(data, data_info)
    data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {"scripts": ["clean_data.py"], "data": SRC / "data" / "wage.xlsx"},
)
@pytask.mark.produces(BLD / "python" / "data" / "wage_gap.csv")
def task_clean_wage_data(depends_on, produces):
    """Creat the wage gap data."""
    data = pd.read_excel(depends_on["data"], index_col=None)
    data = clean_wage_data(data)
    data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data": BLD / "python" / "data" / "data1990_raw.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "fig1_data.csv")
def task_clean_fig1_data(depends_on, produces):
    """Generate fig1 data."""
    data = pd.read_csv(depends_on["data"])
    data = clean_fig1_data(data)
    data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data": BLD / "python" / "data" / "data1990_raw.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "fig2_data.csv")
def task_clean_fig2_data(depends_on, produces):
    """Generate fig2 data."""
    data = pd.read_csv(depends_on["data"])
    data = clean_fig2_data(data)
    data.to_csv(produces, index=False)


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data": BLD / "python" / "data" / "data1990_raw.csv",
    },
)
@pytask.mark.produces(BLD / "python" / "data" / "Sample2.csv")
def task_clean_data_with_control(depends_on, produces):
    """Create sample 2 data (Python version)."""
    data = pd.read_csv(depends_on["data"])
    data = clean_data_with_control(data)
    data.to_csv(produces, index=False)
