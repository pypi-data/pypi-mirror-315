# Author: B站 元蓝先生
# Date: 2024-12-13

import pandas as pd


def order_var1_var2(df, var1, var2):
    '''
    排序变量，将 var2 排在 var1 后面
    '''

    columns = df.columns.tolist()
    columns.remove(var2)
    columns.insert(columns.index(var1) + 1, var2)
    df = df[columns]
    return df


def gen_year(df, var_date):
    '''
    生成 Year 变量，保留年度数据，删除 var_date变量
    '''

    df = df.copy()
    df = df[df[var_date].str.endswith('-12-31')]
    df['Year'] = df[var_date].str[:4]
    df = df.drop(columns=[var_date])
    return df


def var_to_numeric(df, vars_int=None, vars_float=None):
    '''
    将变量转为数值型
    '''

    df = df.copy()
    if vars_int:
        for var in vars_int:
            df[var] = df[var].astype(int)
    if vars_float:
        for var in vars_float:
            df[var] = pd.to_numeric(df[var], errors='coerce')
    return df


def filtered_a_stock(df):
    '''
    保留 A 股数据
    '''

    df = df.copy()
    df = df[
        (df['ID'] < 200000) |
        ((df['ID'] >= 300000) & (df['ID'] < 400000)) |
        ((df['ID'] >= 600000) & (df['ID'] < 700000))
        ]
    return df


def check_year_distribution(df):
    '''
    按年分布情况
    '''

    result = df['Year'].value_counts().sort_index()
    return result


def check_duplicated(df, subset):
    '''
    是否有重复记录
    '''

    result = df.duplicated(subset=subset).any()
    return result


def check_missing(df):
    '''
    缺失值情况
    '''

    summary = pd.DataFrame({
        'Data Type': df.dtypes,
        'Missing Values': df.isnull().sum(),
        'Missing Percentage': (df.isnull().sum() / len(df) * 100).round(1)
    })
    return summary


def print_check(df, subset_duplicated):
    print('-' * 50)
    print('查看按年分布情况')
    print('-' * 50)
    result = check_year_distribution(df)
    print(result)

    print('\n\n')
    print('-' * 50)
    print('查看是否有重复记录')
    print('-' * 50)
    result = check_duplicated(df, subset_duplicated)
    print(result)

    print('\n\n')
    print('-' * 50)
    print('查看缺失值情况')
    print('-' * 50)
    result = check_missing(df)
    print(result)


def get_sample_list(file):
    '''
    获得 样本 列表
    '''

    df = pd.read_excel(file)
    return df


def check_describe1(df, column):
    '''
    查看 连续变量 描述性统计
    '''

    print('-' * 50)
    print('查看统计信息')
    print('-' * 50)
    print(df[column].describe())

    print('\n\n')
    print('-' * 50)
    print('查看缺失值情况')
    print('-' * 50)
    missing_count = df[column].isnull().sum()
    missing_ratio = (missing_count / len(df[column])) * 100
    print(f'缺失值数量: {missing_count}')
    print(f'缺失值比例: {missing_ratio:.2f}%')


def check_describe2(df, groupby, column):
    '''
    查看 类别变量 描述性统计
    '''

    print('-' * 50)
    print('查看统计信息')
    print('-' * 50)
    result = df.groupby(groupby).size().unstack()
    result['Total'] = result.sum(axis=1)
    print(result)

    print('\n\n')
    print('-' * 50)
    print('查看缺失值情况')
    print('-' * 50)
    missing_count = df[column].isnull().sum()
    missing_ratio = (missing_count / len(df[column])) * 100
    print(f'缺失值数量: {missing_count}')
    print(f'缺失值比例: {missing_ratio:.2f}%')


def check_describe3(df, column):
    '''
    查看 类别分布情况
    '''

    print('-' * 50)
    print('查看类别分布情况')
    print('-' * 50)

    counts = df[column].value_counts(dropna=False)
    percentages = df[column].value_counts(normalize=True, dropna=False) * 100
    result = pd.DataFrame({'Count': counts, 'Percentage': percentages})
    result = result.sort_index()
    print(result)


def winsorize(df, columns, quantile=None, inplace=True):
    '''
    处理异常值
    '''

    df = df.copy()

    if quantile is None:
        lower_quantile = 0.01
        upper_quantile = 0.99
    else:
        lower_quantile, upper_quantile = quantile

    for col in columns:
        lower_bound = df[col].quantile(lower_quantile)
        upper_bound = df[col].quantile(upper_quantile)

        if inplace:
            name = col
        else:
            name = f'{col}_winsorized'

        df[name] = df[col].clip(lower=lower_bound, upper=upper_bound)
    return df


def format_describe(df, vars_all, vars_int):
    '''
    生成 描述性统计表
    '''

    describe = df[vars_all].describe(percentiles=[0.25, 0.5, 0.75]).T
    describe = describe[['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']]

    columns = {
        'count': '样本量',
        'mean': '均值',
        'std': '标准差',
        'min': '最小值',
        '25%': 'P25',
        '50%': '中位数',
        '75%': 'P75',
        'max': '最大值'
    }
    describe = describe.rename(columns=columns)

    describe = describe.map(lambda x: f'{x:.3f}')

    describe['样本量'] = describe['样本量'].apply(lambda x: f'{float(x):.0f}')

    cols = ['最小值', 'P25', '中位数', 'P75', '最大值']
    for row in vars_int:
        describe.loc[row, cols] = describe.loc[row, cols].apply(lambda x: f'{float(x):.0f}')

    describe = describe.reset_index()
    describe = describe.rename(columns={'index': '变量'})
    return describe
