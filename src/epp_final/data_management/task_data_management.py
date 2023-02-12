"""Tasks for managing the data."""

import pandas as pd
import pytask

from epp_final.config import BLD, SRC
from epp_final.data_management.clean_data import clean_raw_data
from epp_final.data_management.clean_data import clean_data
from epp_final.utilities import read_yaml


@pytask.mark.depends_on(
    {
        "scripts": ["clean_data.py"],
        "data_info": SRC / "data_management" / "data_info1990.yaml",
        "data": SRC / "data" / "raw_data.csv"
    }
)
@pytask.mark.produces(BLD / "python" / "data" / "data1990_raw.csv")
def task_clean_data_1990(depends_on, produces):
    """Clean the data (Python version)."""
    data_info = read_yaml(depends_on["data_info"])
    data = pd.read_csv(depends_on["data"])
    data = clean_raw_data(data, data_info)
    data.to_csv(produces, index=False)
