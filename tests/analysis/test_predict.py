"""Tests for the prediction model."""
import pandas as pd
import pytest
from epp_final.analysis.predict import (
    _PESR,
    data_processing,
    gen_plot_data,
    gen_plot_data_control,
    rural_urban_dataframe,
    year_data_split,
)
from epp_final.config import TEST_DIR


@pytest.fixture()
def data():
    data1990 = pd.read_csv(TEST_DIR / "analysis" / "data1990_raw_test.csv")
    sample2 = pd.read_csv(TEST_DIR / "analysis" / "Sample2_test.csv")
    out = {"data1990": data1990, "sample2": sample2}
    return out


def test_year_data_split(data):
    data_p = data_processing(data["data1990"])
    year_data = year_data_split(data_p)
    for i in range(980, 991):
        assert sum(year_data[f"Birth{i}"]["CN1990A_BIRTHY"] == (i + 1)) == 0


def test_PESR():
    a0 = 0.2
    a1 = 0.3
    a2 = 0.4
    a3 = 0.5
    assert _PESR(a0, a1, a2, a3) == -23 / 4 * 100


def test_gen_coefficient(data):
    data_p = data_processing(data["data1990"])
    year_data = year_data_split(data_p)
    coef = gen_plot_data(year_data)
    for i in range(980, 991):
        a0, a1, a2, a3, PESr = coef[f"{i}"]
        assert _PESR(a0, a1, a2, a3) == PESr


def test_regional_data_shape_name(data):
    data_p = data_processing(data["data1990"])
    year_data = year_data_split(data_p)
    dfa3_regional, dfpesr_regional = rural_urban_dataframe(year_data)
    assert dfa3_regional.shape == dfpesr_regional.shape
    assert dfa3_regional.columns[2] == dfpesr_regional.columns[2]


def test_only_with_control(data):
    year_data = year_data_split(data["sample2"])
    X_variables_c = data["sample2"].columns[[2, 8, 9, 11, 12, 13, 15, 16, 17, 3]]
    dfa3_control = gen_plot_data_control(year_data, X_variables_c)
    assert dfa3_control.shape[0] == 11
