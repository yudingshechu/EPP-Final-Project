"""Tasks running the results formatting (tables, figures)."""

import pandas as pd
import pytask

from epp_final.analysis.model import load_model
from epp_final.config import BLD
from epp_final.final.plot import (
    plot_fig1,
    plot_fig2,
    plot_figqpp,
    plot_results,
    plot_results_regional,
    reformat_data,
)

kwargs = {
    "produces": {
        "produces1": BLD / "python" / "figures" / "A3.png",
        "produces2": BLD / "python" / "figures" / "PESR.png",
        "produces3": BLD / "python" / "figures" / "A3_regional.png",
        "produces4": BLD / "python" / "figures" / "PESR_regional.png",
        "produces5": BLD / "python" / "figures" / "A3_control.png",
        "produces6": BLD / "python" / "figures" / "A3_regional_control.png",
    },
}


@pytask.mark.depends_on(
    {
        "data": BLD / "python" / "models" / "coef1990.pickle",
        "dfa3_regional": BLD / "python" / "models" / "dfa3_regional.pickle",
        "dfpesr_regional": BLD / "python" / "models" / "dfpesr_regional.pickle",
        "dfa3_control": BLD / "python" / "models" / "dfa3_control.pickle",
        "dfa3_reg_control": BLD / "python" / "models" / "dfa3_regional_control.pickle",
    },
)
@pytask.mark.task(kwargs=kwargs)
def task_plot_results_all(depends_on, produces):
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
    fig1.write_image(produces["produces1"])
    fig2.write_image(produces["produces2"])
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
    fig3.write_image(produces["produces3"])
    fig4.write_image(produces["produces4"])
    dfa3_control = load_model(depends_on["dfa3_control"])
    fig5 = plot_results(
        dfa3_control,
        {"x": "Year", "y": "alpha 3"},
        "Policy Effect on Probability to be a male (with control)",
    )
    fig5.write_image(produces["produces5"])
    dfa3_reg_control = load_model(depends_on["dfa3_reg_control"])
    fig6 = plot_results_regional(
        dfa3_reg_control,
        {"x": "Year", "y": "alpha 3"},
        "Policy Effect on Probability to be a male (with control)",
    )
    fig6.write_image(produces["produces6"])


kwargs2 = {
    "produces": {
        "produces1": BLD / "python" / "figures" / "fig1.png",
        "produces2": BLD / "python" / "figures" / "fig2.png",
        "produces3": BLD / "python" / "figures" / "fig_app.png",
    },
}


@pytask.mark.depends_on(
    {
        "fig1_data": BLD / "python" / "data" / "fig1_data.csv",
        "fig2_data": BLD / "python" / "data" / "fig2_data.csv",
        "fig_app": BLD / "python" / "data" / "wage_gap.csv",
    },
)
@pytask.mark.task(kwargs=kwargs2)
def task_plot_fig(depends_on, produces):
    """Plot sex ratio by birth year."""
    fig1_data = pd.read_csv(depends_on["fig1_data"])
    fig2_data = pd.read_csv(depends_on["fig2_data"])
    figapp = pd.read_csv(depends_on["fig_app"])
    fig1 = plot_fig1(fig1_data)
    fig2 = plot_fig2(fig2_data)
    figapp = plot_figqpp(figapp)
    fig1.write_image(produces["produces1"])
    fig2.write_image(produces["produces2"])
    figapp.write_image(produces["produces3"])
