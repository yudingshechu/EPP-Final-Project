"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import plotly.express as px
import pytask

from epp_final.analysis.model import load_model
from epp_final.config import BLD
from epp_final.final import reformat_data

kwargs = {
    "produces1": BLD / "python" / "figures" / "A3.png",
    "produces2": BLD / "python" / "figures" / "PESR.png",
}


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "models" / "coef1990.pickle",
    },
)
@pytask.mark.task(kwargs=kwargs)
def task_plot_results_all(depends_on, produces1, produces2):
    """Plot the regression results by age (Python version)."""
    data = load_model(depends_on["data"])
    a3_all, Pesr_all = reformat_data(data)
    x = [i + 1000 for i in range(980, 991)]
    dfa3 = pd.DataFrame({"x": x, "y": a3_all})
    dfpesr = pd.DataFrame({"x": x, "y": Pesr_all})
    fig1 = px.line(
        dfa3,
        x="x",
        y="y",
        labels={"x": "Year", "y": "alpha 3"},
        title="Policy Effect on Probability to be a male",
    )
    fig2 = px.line(
        dfpesr,
        x="x",
        y="y",
        labels={"x": "Year", "y": "PESR"},
        title="Policy Effect on Sex Ratio",
    )
    fig1.write_image(produces1)
    fig2.write_image(produces2)
