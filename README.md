# EPP-Final

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/yudingshechu/epp_final/main.svg)](https://results.pre-commit.ci/latest/github/yudingshechu/epp_final/main)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Usage

To get started, first clone this github repository in your computer, then open terminal
and change directory to where you cloned this repository, then create and activate the
environment with

```console
$ conda/mamba env create
$ conda activate epp_final
```

To build the project, type

```console
$ pytask
```

Then you can find generated results in the `bld` folder of `EPP-Final-Project`
directory.

## Credits

This project was created with [cookiecutter](https://github.com/audreyr/cookiecutter)
and the
[econ-project-templates](https://github.com/OpenSourceEconomics/econ-project-templates).

## *EPP* Final Project

This repository is created for the course *Effective Programming Practices for
Economists* in the University of Bonn. It contains a reproducible project of replication
of
[Li, H., Yi, J., & Zhang, J. (2011). Estimating the effect of the one-child policy on the sex ratio imbalance in China: Identification based on the difference-in-differences. Demography, 48(4), 1535-1557](https://read.dukeupress.edu/demography/article/48/4/1535/169759/Estimating-the-Effect-of-the-One-Child-Policy-on).
The programming language used here is python.

## Replication of Li, H., Yi, J., & Zhang, J. (2011)

There are 56 ethnic groups in China. Over 91.11% of the population are Han and the rest
is considered ethnic minorities(not Han Chinese). The one-child policy is launched in
1979 and only applied to the Han Chinese but not to the minorities. \
In this paper, the
ethnic minorities are treated as the control group, and the Han Chinese as the treatment
group. The authors contributed to identify the causal effect of the one-child policy on
the increase in sex ratio in China by a difference in difference (DD) estimator using
1990 census, 2000 census and 2005 mini-census data. We only found the 1990 and 2000 1%
sampled census data and the data is still very big. Therefore, the DD estimation
conducted in this project only use
[1990 0.05% sampled census data](https://international.ipums.org/international-action/sample_details/country/cn#tab_cn1990a).

| Avg prob of being a boy | Han               | Minority          |
| ----------------------- | ----------------- | ----------------- |
| Born before 1979        | $E(S_i\|H=1,T=0)$ | $E(S_i\|H=0,T=0)$ |
| Born after 1979         | $E(S_i\|H=1,T=1)$ | $E(S_i\|H=0,T=1)$ |

- $S_i$ is a child's gender status: $S_i=1$ if the child is a boy, otherwise $S_i=0$;
- $H$ is the ethnic indicator: $H=1$ if the child is Han Chinese, otherwise $H=0$;
- $T$ is the birth cohort indicator: $T=1$ if the child was born after 1979, otherwise
  $T=0$.
- $DD=\\bigg(E(S_i|H=1,T=1)-E(S_i|H=1,T=0)\\bigg)-\\bigg(E(S_i|H=0,T=1)-E(S_i|H=0,T=0)\\bigg)$;
- The regression-adjusted DD model is: $S_i=\\alpha_0+\\alpha_1 H_i+\\alpha_2
  T_i+\\alpha_3 (H_i * T_i)+\\epsilon_i$;
- Using the regression framework, control for the child's parents education level:
  $S_i=\\alpha_0+\\alpha_1 H_i+\\alpha_2 T_i+\\alpha_3 (H_i \*
  T_i)+X_i\\beta+\\epsilon_i$;
- $\\alpha_3$ is identical to $DD$.

| $\\frac{males}{females}$ | Han                                                                                            | Minority                                               |
| ------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| before 1979              | $\\frac{\\alpha_0+\\alpha_1}{1-(\\alpha_0+\\alpha_1)}$                                         | $\\frac{\\alpha_0}{1-\\alpha_0}$                       |
| after 1979               | $\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3)}$ | $\\frac{\\alpha_0+\\alpha_2}{1-(\\alpha_0+\\alpha_2)}$ |

- The policy effect on sex ratio (PESR) can be calculated as:
  $PESR=100\*\\bigg\[\\bigg(\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3)}-\\frac{\\alpha_0+\\alpha_1}{1-(\\alpha_0+\\alpha_1)}\\bigg)-\\bigg(\\frac{\\alpha_0+\\alpha_2}{1-(\\alpha_0+\\alpha_2)}-\\frac{\\alpha_0}{1-\\alpha_0}\\bigg)\\bigg\]$.

## Apply the Empirical Strategy in Li, H., Yi, J., & Zhang, J. (2011) in Estimating the effect of Two-Child Policy on Sex ratio in Han Chinese---Triple Diff-in-Diff

From 1979 until 2015, Chinese citizens were generally permiited to have only one child,
with certain exceptions such that:

- ethnic minorities(not Han) Chinese are usually reconmmand to have more than one child;
- the policy is more loose for a household with the agricultural Hukou(rural), they can
  have two children in many cases;
- in 1984, a married couple with non-agricultural Hukou(urban) are allowed to have two
  children if both of them were the only child in their family, namely the two-child
  policy.
- *Hukou is a system of household registration used in mainland China. Each citizen was
  classified in an agricultural or non-agricultural Hukou(commonly referred to as rural
  or urban)*

This unique affirmative two-child policy allows us to estimate the effect of the
two-child policy on the increase in sex ratio in China by a triple Diff-in-Diff method
(DDD) estimator using 1990 census data. The period included in this estimation is from
1980 to 1990. We set the Chinese citizens with non-ag Hukou as treatment group and the
Chinese citizens with ag Hukou as control group. The treatment group introduces the
two-child policy in 1984, while the control group does not have such a strongly limiting
policy. Furthermore, the population of each group can be subdivided into two groups, the
Han Chinese and ethnic minorities Chinese. Therefore, we have eight groups:

| Avg prob of being a boy    | Han with non-ag Hukou | Minority with non-ag Hukou | Han with ag Hukou     | Minority with ag Hukou |
| -------------------------- | --------------------- | -------------------------- | --------------------- | ---------------------- |
| Born between 1979 and 1984 | $E(S_i\|H=1,K=1,T=0)$ | $E(S_i\|H=0,K=1,T=0)$      | $E(S_i\|H=1,K=0,T=0)$ | $E(S_i\|H=0,K=0,T=0)$  |
| Born after 1984            | $E(S_i\|H=1,K=1,T=1)$ | $E(S_i\|H=0,K=1,T=1)$      | $E(S_i\|H=1,K=0,T=1)$ | $E(S_i\|H=0,K=0,T=1)$  |

- $S_i$ is a child's gender status: $S_i=1$ if the child is a boy, otherwise $S_i=0$;
- $H$ is the ethnic indicator: $H=1$ if the child is Han Chinese, otherwise $H=0$;
- $T$ is the birth cohort indicator: $T=1$ if the child was born after 1984, $T=0$ if
  the child was born before 1984 but after 1979;
- $K$ is the Hukou indicator: $K=1$ if the child was born in a household with
  non-agricultural Hukou, otherwise $K=0$.
- $DDD=\\bigg\[\\bigg(E(S_i|H=1,K=1,T=1)-E(S_i|H=1,K=1,T=0)\\bigg)$
  $-\\bigg(E(S_i|H=0,K=1,T=1)-E(S_i|H=0,K=1,T=0)\\bigg)\\bigg\]$
  $-\\bigg\[\\bigg(E(S_i|H=1,K=0,T=1)-E(S_i|H=1,K=0,T=0)\\bigg)$
  $-\\bigg(E(S_i|H=0,K=0,T=1)-E(S_i|H=0,K=0,T=0)\\bigg)\\bigg\]$
- The regression-adjusted DDD model is: $S_i=\\alpha_0+\\alpha_1 H_i+\\alpha_2
  T_i+\\alpha_3 K_i+\\alpha_4 (H_i * T_i)+\\alpha_5 (H_i * K_i)+\\alpha_6 (T_i \*
  K_i)+\\alpha_7 (H_i * T_i * K_i)+\\epsilon_i$;
- Using the regression framework, control for the child's parents education level:
  $S_i=\\alpha_0+\\alpha_1 H_i+\\alpha_2 T_i+\\alpha_3 K_i+\\alpha_4 (H_i \*
  T_i)+\\alpha_5 (H_i * K_i)+\\alpha_6 (T_i * K_i)+\\alpha_7 (H_i * T_i \*
  K_i)+X\*\\beta+\\epsilon_i$;
- $\\alpha_7$ is identical to $DDD$.

| $\\frac{males}{females}$ | Han with non-ag Hukou                                                                                                                                                          | Minority with non-ag Hukou                                                                     | Han with ag Hukou                                                                              | Minority with ag Hukou                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| Born before 1979         | $\\frac{\\alpha_0+\\alpha_1+\\alpha_3+\\alpha_5}{1-(\\alpha_0+\\alpha_1+\\alpha_3+\\alpha_5)}$                                                                                 | $\\frac{\\alpha_0+\\alpha_3}{1-(\\alpha_0+\\alpha_3)}$                                         | $\\frac{\\alpha_0+\\alpha_1}{1-(\\alpha_0+\\alpha_1)}$                                         | $\\frac{\\alpha_0}{1-\\alpha_0}$                       |
| Born after 1979          | $\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3+\\alpha_4+\\alpha_5+\\alpha_6+\\alpha_7}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3+\\alpha_4+\\alpha_5+\\alpha_6+\\alpha_7)}$ | $\\frac{\\alpha_0+\\alpha_2+\\alpha_3+\\alpha_4}{1-(\\alpha_0+\\alpha_2+\\alpha_3+\\alpha_4)}$ | $\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_4}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_4)}$ | $\\frac{\\alpha_0+\\alpha_2}{1-(\\alpha_0+\\alpha_2)}$ |

- The policy effect on sex ratio (PESR) can be calculated as:
  $PESR=100\*\\bigg\[\\bigg(\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3+\\alpha_4+\\alpha_5+\\alpha_6+\\alpha_7}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_3+\\alpha_4+\\alpha_5+\\alpha_6+\\alpha_7)}-\\frac{\\alpha_0+\\alpha_1+\\alpha_3+\\alpha_5}{1-(\\alpha_0+\\alpha_1+\\alpha_3+\\alpha_5)}-\\big(\\frac{\\alpha_0+\\alpha_2+\\alpha_3+\\alpha_4}{1-(\\alpha_0+\\alpha_2+\\alpha_3+\\alpha_4)}-\\frac{\\alpha_0+\\alpha_3}{1-(\\alpha_0+\\alpha_3)}\\big)\\bigg)-\\bigg(\\frac{\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_4}{1-(\\alpha_0+\\alpha_1+\\alpha_2+\\alpha_4)}-\\frac{\\alpha_0+\\alpha_1}{1-(\\alpha_0+\\alpha_1)}-\\big(\\frac{\\alpha_0+\\alpha_2}{1-(\\alpha_0+\\alpha_2)}-\\frac{\\alpha_0}{1-\\alpha_0}\\big)\\bigg)\\bigg\]$.

## Interpretation of Cleaned Data

1. Original data(path: src/data):

- **raw_data.csv** is collected from
  [IPUMS China 1990 and 2000 0.05% sampled census data](https://international.ipums.org/international-action/sample_details/country/cn#tab_cn1990a).
  It is a $2362403\\times47$ dataframe and contains individuals' information such as
  gender, ethnicity, birth year, relation with the household head, Hukou, and education
  level.
- **wage.xlsx** is collected from *Table 1a: Mean Gender Earnings, Earnings Gaps, and
  Ratios in Urban China, 1988-2004* in
  [Zhang, J., Han, J., Liu, P. W., & Zhao, Y. (2008). Trends in the gender earnings differential in urban China, 1988–2004. ILR Review, 61(2), 224-243](https://www.semanticscholar.org/paper/Trends-in-the-Gender-Earnings-Differential-in-Urban-Zhang-Han/89d6dc2c9310c48566154da9cc010a99ce880042).

2. Cleaned data(path: bld/python/data):

- **data1990_raw.csv** is the cleaned **raw_data.csv** with only 1990 census. It is a
  $1182237\\times8$ dataframe. The column variables are:
  - *CN1990A_SEX*: gender, 1 is male, 2 is female;
  - *CN1990A_NATION*: Han=1 or ethnic minorities (not Han=0);
  - *CN1990A_HHTYA* : Hukou , 1 is agricultural, 2 is non ag, 9 is unknown;
  - *CN1990A_BIRTHY*: birth year, i.e., 1982 is dnoted as 982. Only 973-990 are kept in
    this dataset;
  - *CN1990A_RELATE*: the relation with household head, 1 is Head of household, 2 is
    Spouse and 3 is Child (other relations are represented from 4 to 8, we only consider
    direct related family members in this project)
  - *CN1990A_EDLEV1*: education level, 0 is not in universe, 1 is illiterate or
    semi-literate, 2 is primary school, 3 is junior middle school, 4-7 is considered
    high education level.
- **Sample2.csv** includes all children aged from 0 to 17 in the Chinese population
  census in 1990 (1% sample) with age, gender, registration type and geographic location
  information. More importantly, only children satisfying the following conditions:
  - sons or daughters of the household head;
  - complete information of mother, father, and siblings;
  - mother's age is ranging from 20 to 38, will be kept in this dataset.
- **triple_did.csv** restricts children that were born between 1980 and 1990, and adds
  interact terms for triple diff-in-diff model in the columns for each row.
- **fig1_data.csv** is a $47\\times2$ dataframe including sex ratios in each year from
  1945 to 1990.
- **fig2_data.csv** is a $47\\times3$ dataframe including sex ratios of Han and ethnic
  minorities in each year from 1945 to 1990.
- **wage_gap.csv** is the mean earnings of female and of male from 1988 to 2004.

## Interpretation of Figures

- One-Child Policy Effect
  - **A3.png**: One-child policy effect of the probility to be a male. The x-axis is
    year from 1980 to 1990, y-axis is the $\\alpha_3$ and its range is from
    $(-0.005,0.035)$.
  - **A3_regional.png**: One-child policy effect of the probility to be a male, grouped
    by urban area and rural area. The x-axis is time, from 1980 to 1990, y-axis is the
    $\\alpha_3$.
  - **A3_control.png**: One-child policy effect of the probility to be a male, grouped
    by urban area and rural area and controlled for the education level of the child's
    parents. The x-axis is year from 1980 to 1990, y-axis is the $\\alpha_3$.
  - **A3_regional_control.png**: One-child policy effect of the probility to be a male,
    controlled for the education level of the child's parents.. The x-axis is year from
    1980 to 1990, y-axis is the $\\alpha_3$.
  - **PESR.png**: One-child policy effect on sex ratio(PESR). The x-axis is year from
    1980 to 1990, y-axis is the $PESR$.
  - **PESR_regional.png**: One-child policy effect on sex ratio(PESR), grouped by urban
    area and rural area. The x-axis is year from 1980 to 1990, y-axis is the $PESR$.
  - **PESR_regional_control.png**: One-child policy effect on sex ratio(PESR), grouped
    by urban area and rural area and controlled for the education level of the child's
    parents. The x-axis is year from 1980 to 1990, y-axis is the $PESR$.
- Two-Child Policy Effect

## References

****Minnesota Population Center. Integrated Public Use Microdata Series, International:
Version 7.3 \[dataset\]. Minneapolis, MN: IPUMS, 2020.****
[IPUMS data link](https://doi.org/10.18128/D020.V7.3)

****Li, H., Yi, J., & Zhang, J. (2011). Estimating the effect of the one-child policy on
the sex ratio imbalance in China: Identification based on the difference-in-differences.
Demography, 48(4), 1535-1557.****

****Zhang, J., Han, J., Liu, P. W., & Zhao, Y. (2008). Trends in the gender earnings
differential in urban China, 1988–2004. ILR Review, 61(2), 224-243.****
