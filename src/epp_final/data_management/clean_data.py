"""Function(s) for cleaning the data set(s)."""

import numpy as np
import pandas as pd


def clean_raw_data(data, data_info):
    """Generate data for year 1990.

    Args:
        data (pandas.DataFrame): raw data

    Returns:
        pandas.DataFrame: The 1990 data set.

    """
    data1990 = data[data["YEAR"] == 1990].copy()
    data1990_2000 = data1990.filter(like="2000", axis=1).copy()
    data1990_no2000 = data1990.drop(data1990_2000.columns, axis=1).copy()
    data1990_no2000 = data1990_no2000[data_info["variable1990"]].copy()
    data1990_no2000 = data1990_no2000.astype("int64")
    return data1990_no2000


def _to_decimal(x):
    return x / 1000


def clean_wage_data(data):
    """Generate data for gender wage gap in urban China.

    Args:
        data (excel file): wage.xlsx

    Returns:
        pandas.DataFrame: The gender wage gap from 1988 to 2004.

    """
    wage_gap = data.transpose()
    wage_gap.columns = ["female", "male"]
    wage_gap.reset_index(drop=True)
    wage_gap["year"] = range(1988, 2005)
    wage_gap["female"] = wage_gap["female"].apply(_to_decimal)
    wage_gap["male"] = wage_gap["male"].apply(_to_decimal)
    return wage_gap


def clean_fig1_data(data):
    """Generate data for figure 1.

    Args:
        data (pd.DataFrame): data1990.csv
        years: from 1945 to 1990
        birth: dictionary with individuals' birth year and sex
        birth_male: sum of male newborns by birth year
        birth_female: sum of female newborns by birth year
        birth_sex: sex ratio in each birth year.

    Returns:
        pd.DataFrame: birth_sex--sex ratios by birth cohorts.

    """
    years = range(945, 991)
    birth = {}
    birth_male = {}
    birth_female = {}
    for year in years:
        birth[year] = data[data["CN1990A_BIRTHY"] == year]
        birth[year] = birth[year][["CN1990A_BIRTHY", "CN1990A_SEX"]]
    birth_df = pd.concat(list(birth.values()))

    for year in years:
        birth_male[year] = birth_df.loc[
            (birth_df["CN1990A_BIRTHY"] == year) & (birth_df["CN1990A_SEX"] == 1)
        ].sum()
    birth_male = pd.DataFrame(birth_male)
    birth_male = birth_male.iloc[1:]

    for year in years:
        birth_female[year] = (
            birth_df.loc[
                (birth_df["CN1990A_BIRTHY"] == year) & (birth_df["CN1990A_SEX"] == 2)
            ].sum()
            / 2
        )
    birth_female = pd.DataFrame(birth_female)
    birth_female = birth_female.iloc[1:]
    birth_sex = pd.concat([birth_male, birth_female], axis=0)
    birth_sex = birth_sex.div(birth_sex.shift(-1))
    birth_sex.columns = range(1945, 1991)

    birth_sex = birth_sex.dropna()
    birth_sex = birth_sex.transpose()
    birth_sex["Year"] = range(1945, 1991)
    return birth_sex


def clean_fig2_data(data):
    """Generate data for figure 1.

    Args:
        data (pd.DataFrame): data1990.csv
        years: from 1945 to 1990
        nation: dictionary with individuals' birth year, sex and nation
        han_male: sum of han male newborns by birth year
        han_female: sum of han female newborns by birth year
        nohan_male: sum of minority male newborns by birth year
        nohan_female:

    Returns:
        pd.DataFrame: birth_sex--sex ratios by birth cohorts.

    """
    years = range(945, 991)
    nation = {}
    han_male = {}
    nohan_male = {}
    han_female = {}
    nohan_female = {}

    for year in years:
        nation[year] = data[data["CN1990A_BIRTHY"] == year]
        nation[year] = nation[year][["CN1990A_BIRTHY", "CN1990A_SEX", "CN1990A_NATION"]]
    nation_df = pd.concat(list(nation.values()))
    nation_df["CN1990A_NATION"].replace(list(range(2, 100)), 0, inplace=True)
    han = nation_df[nation_df["CN1990A_NATION"] == 1]
    nohan = nation_df[nation_df["CN1990A_NATION"] == 0]

    for year in years:
        han_male[year] = han.loc[
            (han["CN1990A_BIRTHY"] == year) & (han["CN1990A_SEX"] == 1)
        ].sum()
    han_male = pd.DataFrame(han_male)
    han_male = han_male.loc["CN1990A_SEX"]

    for year in years:
        han_female[year] = (
            han.loc[(han["CN1990A_BIRTHY"] == year) & (han["CN1990A_SEX"] == 2)].sum()
            / 2
        )
    han_female = pd.DataFrame(han_female)
    han_female = han_female.loc["CN1990A_SEX"]
    han_sex = han_male / han_female

    for year in years:
        nohan_male[year] = nohan.loc[
            (nohan["CN1990A_BIRTHY"] == year) & (nohan["CN1990A_SEX"] == 1)
        ].sum()
    nohan_male = pd.DataFrame(nohan_male)
    nohan_male = nohan_male.loc["CN1990A_SEX"]

    for year in years:
        nohan_female[year] = (
            nohan.loc[
                (nohan["CN1990A_BIRTHY"] == year) & (nohan["CN1990A_SEX"] == 2)
            ].sum()
            / 2
        )
    nohan_female = pd.DataFrame(nohan_female)
    nohan_female = nohan_female.loc["CN1990A_SEX"]
    nohan_sex = nohan_male / nohan_female
    han_sex.name = "Han"
    nohan_sex.name = "Minorities"
    fig2_nation = pd.concat([han_sex, nohan_sex], axis=1).reset_index(drop=True)
    fig2_nation["Year"] = range(1945, 1991)
    return fig2_nation


def clean_data_with_control(data1990_no2000):
    """Create the cleaned data with control variables.

    Args:
        data1990_no2000 (pd.DataFrame): 1990 raw data.

    Returns:
        pd.DataFrame: Sample 2 data in original paper.

    """
    data1990_no2000["CN1990A_SEX"].replace({2: 0}, inplace=True)
    data1990_no2000["CN1990A_NATION"].replace(list(range(2, 100)), 0, inplace=True)
    data1990_no2000["CN1990A_HHTYA"].replace([2, 9], 0, inplace=True)
    data1990_no2000["Treat"] = np.zeros(data1990_no2000.shape[0], dtype="int")
    data1990_no2000.loc[data1990_no2000["CN1990A_BIRTHY"] > 979, "Treat"] = 1
    data1990_no2000["OneChildInteract"] = (
        data1990_no2000["Treat"] * data1990_no2000["CN1990A_NATION"]
    )
    data1990_no2000.drop(
        data1990_no2000[data1990_no2000["CN1990A_RELATE"] > 3].index,
        inplace=True,
    )
    data1990_no2000.reset_index(drop=True, inplace=True)
    sample2_data = data1990_no2000.copy()
    NIU_edu = sample2_data[sample2_data["CN1990A_RELATE"] != 3]["CN1990A_EDLEV1"] == 0
    drop_index = sample2_data[sample2_data["CN1990A_RELATE"] != 3].loc[NIU_edu, :].index
    sample2_data.drop(drop_index, inplace=True)
    data1990_group = sample2_data.groupby(["SERIAL"])
    wl = np.array(list(data1990_group.groups.values()), dtype=object)
    get_len = np.vectorize(len)
    wl_drop = wl[get_len(wl) < 3]
    wlf = [j for i in wl_drop for j in i]
    sample2_true = sample2_data.drop(wlf)
    sample2_true.reset_index(drop=True, inplace=True)
    sample2_true["CN1990A_EDLEV1"].replace([4, 5, 6, 7], 4, inplace=True)
    sample2_true["CN1990A_EDLEV1"].replace(
        {1: "Illiterate", 2: "Primary", 3: "Junior", 4: "High"},
        inplace=True,
    )
    HHH = sample2_true["CN1990A_RELATE"] == 1
    HHS = sample2_true["CN1990A_RELATE"] == 2
    HHC = sample2_true["CN1990A_RELATE"] == 3
    HHM = sample2_true["CN1990A_SEX"] == 1
    HHF = sample2_true["CN1990A_SEX"] == 0
    HHH_male = HHH * HHM
    HHH_female = HHH * HHF
    HHSpouse_male = HHS * HHM
    HHSpouse_female = HHS * HHF
    Child = HHC
    sample_father = sample2_true[HHH_male + HHSpouse_male].copy()
    sample_mother = sample2_true[HHH_female + HHSpouse_female].copy()
    sample_mother.drop(
        sample_mother[sample_mother["CN1990A_BIRTHY"] < 952].index,
        inplace=True,
    )
    sample_child = sample2_true[Child].copy()
    sample_father_d = pd.get_dummies(sample_father, columns=["CN1990A_EDLEV1"]).copy()
    sample_mother_d = pd.get_dummies(sample_mother, columns=["CN1990A_EDLEV1"]).copy()
    edu = sample_father_d.iloc[:, [0, 9, 10, 11, 12]].columns
    sample_parents_d = (
        sample_father_d[edu]
        .merge(
            sample_mother_d[edu],
            how="inner",
            on="SERIAL",
            suffixes=("_father", "_mother"),
        )
        .copy()
    )
    working_data = sample_child.merge(sample_parents_d, how="inner", on="SERIAL").copy()
    working_data.drop(
        working_data[working_data["CN1990A_BIRTHY"] < 973].index,
        inplace=True,
    )
    return working_data
