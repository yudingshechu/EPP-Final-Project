"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask

from epp_final.analysis.model import load_model
from epp_final.config import BLD
from epp_final.final.plot import plot_results, plot_results_regional, reformat_data

kwargs = {
    "produces1": BLD / "python" / "figures" / "A3.png",
    "produces2": BLD / "python" / "figures" / "PESR.png",
    "produces3": BLD / "python" / "figures" / "A3_regional.png",
    "produces4": BLD / "python" / "figures" / "PESR_regional.png",
}


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "models" / "coef1990.pickle",
        "dfa3_regional": BLD / "python" / "models" / "dfa3_regional.pickle",
        "dfpesr_regional": BLD / "python" / "models" / "dfpesr_regional.pickle",
    },
)
@pytask.mark.task(kwargs=kwargs)
def task_plot_results_all(depends_on, produces1, produces2, produces3, produces4):
    """Plot the regression results by age (Python version)."""
    data = load_model(depends_on["data"])
    a3_all, Pesr_all = reformat_data(data)
    x = [i + 1000 for i in range(980, 991)]
    dfa3 = pd.DataFrame({"x": x, "y": a3_all})
    dfpesr = pd.DataFrame({"x": x, "y": Pesr_all})
    fig1 = plot_results(
        dfa3,
        {"x": "Year", "y": "alpha 3"},
        "Policy Effect on Probability to be a male",
    )
    fig2 = plot_results(
        dfpesr,
        {"x": "Year", "y": "PESR"},
        "Policy Effect on Sex Ratio",
    )
    fig1.write_image(produces1)
    fig2.write_image(produces2)
    dfa3_regional = load_model(depends_on["dfa3_regional"])
    dfpesr_regional = load_model(depends_on["dfpesr_regional"])
    fig3 = plot_results_regional(
        dfa3_regional,
        {"x": "Year", "y": "alpha 3"},
        "Policy Effect on Probability to be a male",
    )
    fig4 = plot_results_regional(
        dfpesr_regional,
        {"x": "Year", "y": "PESR"},
        "Policy Effect on Sex Ratio",
    )
    fig3.write_image(produces3)
    fig4.write_image(produces4)
