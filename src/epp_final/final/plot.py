"""Functions plotting results."""
import plotly.express as px
import plotly.graph_objects as go


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


def plot_fig1(df):
    """Plot fig 1.

    Args:
        df (pd.DataFrame): dataframe for figure 1

    Returns:
        px.fig: figure 1

    """
    y = df["CN1990A_SEX"]
    x = df["Year"]
    fig1 = px.line(x=x, y=y, title="Sex ratios by birth cohorts")
    fig1 = fig1.update_layout(xaxis_title="Year", yaxis_title="Sex Ratio")
    return fig1


def plot_fig2(df):
    """Plot fig 2.

    Args:
        df (pd.DataFrame): dataframe for figure 2

    Returns:
        px.fig: figure 2

    """
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["Year"], y=df["Han"], name="Han", mode="lines"))
    fig2.add_trace(
        go.Scatter(x=df["Year"], y=df["Minorities"], name="Minorities", mode="lines"),
    )
    fig2 = fig2.update_layout(
        title="Sex ratios by Han and other minorities",
        xaxis_title="Year",
        yaxis_title="Sex Ratio",
        legend_title="Nation",
    )
    return fig2


def plot_figqpp(df):
    """Plot figure for male female wage gap.

    Args:
        df (pd.DataFrame): wage gap data frame

    Returns:
        px.fig: figure for wage gap

    """
    figapp = go.Figure()
    figapp.add_trace(
        go.Scatter(x=df["year"], y=df["male"], mode="lines", name="Male wage"),
    )
    figapp.add_trace(
        go.Scatter(x=df["year"], y=df["female"], mode="lines", name="Female wage"),
    )
    figapp = figapp.update_layout(
        title="Chinese urban gender wage gap 1988-2004",
        xaxis_title="Year",
        yaxis_title="Mean wage",
        legend_title="Gender",
    )
    return figapp
