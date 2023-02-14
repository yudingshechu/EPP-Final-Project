"""Function(s) for cleaning the data set(s)."""

import pandas as pd


def clean_data(data, data_info):
    """Clean data set.

    Information on data columns is stored in ``data_management/data_info.yaml``.

    Args:
        data (pandas.DataFrame): The data set.
        data_info (dict): Information on data set stored in data_info.yaml. The
            following keys can be accessed:
            - 'outcome': Name of dependent variable column in data
            - 'outcome_numerical': Name to be given to the numerical version of outcome
            - 'columns_to_drop': Names of columns that are dropped in data cleaning step
            - 'categorical_columns': Names of columns that are converted to categorical
            - 'column_rename_mapping': Old and new names of columns to be renamend,
                stored in a dictionary with design: {'old_name': 'new_name'}
            - 'url': URL to data set

    Returns:
        pandas.DataFrame: The cleaned data set.

    """
    data = data.drop(columns=data_info["columns_to_drop"])
    data = data.dropna()
    for cat_col in data_info["categorical_columns"]:
        data[cat_col] = data[cat_col].astype("category")
    data = data.rename(columns=data_info["column_rename_mapping"])

    numerical_outcome = pd.Categorical(data[data_info["outcome"]]).codes
    data[data_info["outcome_numerical"]] = numerical_outcome

    return data


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

def to_decimal(x):
    return x/1000

def clean_wage_data(data):
    """Generate data for gender wage gap in urban China.
    
    Args:
        data (excel file): wage.xlsx
        
    Returns:
        pandas.DataFrame: The gender wage gap from 1988 to 2004.
    
    """
    wage_gap=data.transpose()
    wage_gap.columns=['female','male']
    wage_gap.reset_index(drop=True)
    wage_gap['year']=range(1988,2005)
    wage_gap['female']=wage_gap['female'].apply(to_decimal)
    wage_gap['male']=wage_gap['male'].apply(to_decimal)
    return wage_gap

def clean_fig1_data(data):
    """Generate data for figure 1.
    Args:
        data (pd.DataFrame): data1990.csv
        years: from 1945 to 1990
        birth: dictionary with individuals' birth year and sex
        birth_male: sum of male newborns by birth year
        birth_female: sum of female newborns by birth year
        birth_sex: sex ratio in each birth year

    Returns:
        pd.DataFrame: birth_sex--sex ratios by birth cohorts.
    
    """
    years=range(945,991)
    birth={}
    birth_male={}
    birth_female={}
    for year in years:
        birth[year]=data[data['CN1990A_BIRTHY']==year]
        birth[year]=birth[year][['CN1990A_BIRTHY','CN1990A_SEX']]
        print(birth[year])
    birth_df=pd.concat(list(birth.values()))

    for year in years:
        birth_male[year]=birth_df.loc[(birth_df['CN1990A_BIRTHY']==year)&(birth_df['CN1990A_SEX']==1)].sum()
        print(birth_male[year])
    birth_male=pd.DataFrame(birth_male)
    birth_male=birth_male.iloc[1:]

    for year in years:
        birth_female[year]=birth_df.loc[(birth_df['CN1990A_BIRTHY']==year)&(birth_df['CN1990A_SEX']==2)].sum()/2
        print(birth_female[year])
    birth_female=pd.DataFrame(birth_female)
    birth_female=birth_female.iloc[1:]
    birth_sex=pd.concat([birth_male,birth_female],axis=0)
    birth_sex=birth_sex.div(birth_sex.shift(-1))
    birth_sex.columns =range(1945,1991)
    
    birth_sex=birth_sex.dropna()
    birth_sex=birth_sex.transpose()
    birth_sex['Year']=range(1945,1991)
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
    years=range(945,991)
    nation={}
    han_male={}
    nohan_male={}
    han_female={}
    nohan_female={}

    for year in years:
        nation[year]=data[data['CN1990A_BIRTHY']==year]
        nation[year]=nation[year][['CN1990A_BIRTHY','CN1990A_SEX','CN1990A_NATION']]
        print(nation[year])
    nation_df=pd.concat(list(nation.values()))
    nation_df["CN1990A_NATION"].replace(list(range(2,100)),0, inplace=True)
    han = nation_df[nation_df['CN1990A_NATION'] == 1]
    nohan=nation_df[nation_df['CN1990A_NATION'] == 0]

    for year in years:
        han_male[year]=han.loc[(han['CN1990A_BIRTHY']==year)&(han['CN1990A_SEX']==1)].sum()
        print(han_male[year])
    han_male=pd.DataFrame(han_male)
    han_male=han_male.loc['CN1990A_SEX']

    for year in years:
        han_female[year]=han.loc[(han['CN1990A_BIRTHY']==year)&(han['CN1990A_SEX']==2)].sum()/2
        print(han_female[year])
    han_female=pd.DataFrame(han_female)
    han_female=han_female.loc['CN1990A_SEX']
    han_sex=han_male/han_female

    for year in years:
        nohan_male[year]=nohan.loc[(nohan['CN1990A_BIRTHY']==year)&(nohan['CN1990A_SEX']==1)].sum()
        print(nohan_male[year])
    nohan_male=pd.DataFrame(nohan_male)
    nohan_male=nohan_male.loc['CN1990A_SEX']

    for year in years:
        nohan_female[year]=nohan.loc[(nohan['CN1990A_BIRTHY']==year)&(nohan['CN1990A_SEX']==2)].sum()/2
        print(nohan_female[year])
    nohan_female=pd.DataFrame(nohan_female)
    nohan_female=nohan_female.loc['CN1990A_SEX']
    nohan_sex=nohan_male/nohan_female
    han_sex.name='Han'
    nohan_sex.name='Minorities'
    fig2_nation=pd.concat([han_sex,nohan_sex],axis=1).reset_index(drop=True)
    fig2_nation['Year']=range(1945,1991)
    return fig2_nation