import numpy as np
import pandas as pd
import pytest
from epp_final.analysis.predict import data_processing
from epp_final.config import TEST_DIR
from epp_final.data_management import clean_data_with_control


@pytest.fixture()
def data():
    return pd.read_csv(TEST_DIR / "data_management" / "data1990_raw_test.csv")


def test_only_child_left(data):
    working_data = clean_data_with_control(data)
    assert sum(working_data["CN1990A_RELATE"] != 3) == 0


def test_two_parents(data):
    working_data = clean_data_with_control(data)
    assert (
        sum(np.sum(working_data.iloc[:, [10, 11, 12, 13, 14, 15, 16, 17]], axis=1) != 2)
        == 0
    )


def test_18_columns(data):
    working_data = clean_data_with_control(data)
    assert working_data.shape[1] == 18


def test_year_after_1973(data):
    working_data = clean_data_with_control(data)
    assert working_data[working_data["CN1990A_BIRTHY"] < 973].shape[0] == 0


def test_interact(data):
    data_p = data_processing(data)
    assert (
        sum(data_p["OneChildInteract"] != data_p["Treat"] * data_p["CN1990A_NATION"])
        == 0
    )


def test_after_year_1973(data):
    data_p = data_processing(data)
    assert data_p[data_p["CN1990A_BIRTHY"] < 973].shape[0] == 0


def test_treatment(data):
    data_p = data_processing(data)
    after_1979 = sum(data_p["CN1990A_BIRTHY"] > 979)
    treated = sum(data_p["Treat"])
    assert after_1979 == treated
