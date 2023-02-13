"""Functions plotting results."""
import plotly.express as px


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


def plot_results(df, label, title):
    """Plot with plotly.

    Args:
        df (pd.DataFrame): coefficients (y) and year (x)
        label (dict): dict for x and y
        title (string): figure title

    Returns:
        px.fig: figure

    """
    return px.line(df, x="x", y="y", labels=label, title=title)


def plot_results_regional(df, label, title):
    """Plot with plotly, with groups of urban and rural.

    Args:
        df (pd.DataFrame): coefficients (y) and year (x)
        label (dict): dict for x and y
        title (string): figure title

    Returns:
        px.fig: figure

    """
    return px.line(df, x="x", y="y", labels=label, title=title, color="region")
