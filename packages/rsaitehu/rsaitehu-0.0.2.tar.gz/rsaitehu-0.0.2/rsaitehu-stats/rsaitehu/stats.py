'''
This module contains functions for statistical analysis.
'''
import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare, rankdata, chi2, norm
from scikit_posthocs import posthoc_nemenyi_friedman as posthoc_nemenyi
import pingouin as pg
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
import pyreadr
import subprocess
import os
from math import factorial
from itertools import combinations

# Create a custom function to convert the DataFrame to good data for a heatmap
# the values < 0.05 and "good" for the algorithm in the column are going to be 2 - value
# the values < 0.05 and "bad" for the algorithm in the row are going to be value
# the rest of values are going to be 1
# this function returns a DataFrame with the same shape as the original one
# always keep track of the name of the row and column of each cell,
# because the heatmap will be created using the row and column names
# a value is good if means[row_name] > means[col_name]
# a value is bad if means[row_name] < means[col_name]
def to_heatmap_custom(df, means):
    heatmap_data = pd.DataFrame(1, index=df.index, columns=df.columns)
    for i, row_name in enumerate(df.index):
        for j, col_name in enumerate(df.columns):
            value = df.loc[row_name, col_name]
            if value < 0.05:
                heatmap_data.loc[row_name, col_name] = 2 - value if means[i] > means[j] else value 
            if i == j:
                heatmap_data.loc[row_name, col_name] = 3      
    return heatmap_data

def to_image_custom(df_original, df_heatmap_data, filename, df_p_values = None):
    print("Entering to_image_custom")
    # Create a colormap from the list of colors
    cmap = ListedColormap(['red', 'gray', 'green', 'white'])
    sns.set(font_scale=1.2)
    plt.figure(figsize=(12, 10))
    col_labels = df_original.columns
    row_labels = df_original.index
    plt.tick_params(axis='both', which='major', labelsize=10, labelbottom=False, bottom=False, top=False, labeltop=True)
    # Create a copy of the p-values DataFrame to format the non-empty values
    p_values_formatted = df_p_values.copy()
    # Iterate over rows and columns to format non-empty values
    for i, row_name in enumerate(df_p_values.index):
        for j, col_name in enumerate(df_p_values.columns):
            val = df_p_values.loc[row_name, col_name]
            if val != "":
                p_values_formatted.loc[row_name, col_name] = f"{float(val):.2f}"

    if df_p_values is not None:
        sns.heatmap(df_heatmap_data, fmt="", linewidths=.5, cbar=False, cmap=cmap, xticklabels=col_labels, yticklabels=row_labels, annot=p_values_formatted.values)  # Use df_p_values as annotations
    else:
        sns.heatmap(df_heatmap_data, fmt="d", linewidths=.5, cbar=False, cmap=cmap, xticklabels=col_labels, yticklabels=row_labels)
    # save the figure
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

def rankMatrix(data, decreasing=True):
    def rank_rows(row):
        if decreasing:
            return rankdata(-row, method='average')
        else:
            return rankdata(row, method='average')
    
    ranked_data = data.apply(rank_rows, axis=1)
    return ranked_data

def friedmanTest(data):
    N, k = data.shape
    mr = rankMatrix(data).mean(axis=0)
    
    friedman_stat = 12 * N / (k * (k + 1)) * (np.sum(mr**2) - k * (k + 1)**2 / 4)
    p_value = 1 - chi2.cdf(friedman_stat, df=k - 1)

    result = {
        "Friedman's chi-squared": friedman_stat,
        "df": k - 1,
        "p-value": p_value,
        "method": "Friedman's rank sum test",
        "data_name": str(data.columns.values)
    }
    return result

def processControlColumn(data, control):
    if control is not None:
        if isinstance(control, str):
            if control in data.columns:
                control = data.columns.get_loc(control)
            else:
                raise ValueError("The name of the column to be used as control does not exist in the data matrix")
        elif control > data.shape[1] - 1 or control < 0:
            raise ValueError(f"Non-valid value for the control parameter. It has to be either the name of a column or a number between 0 and {data.shape[1] - 1}")
    return control

def generatePairs(k, control):
    if control is None:
        pairs = [(i, j) for i in range(k) for j in range(i + 1, k)]
    else:
        pairs = [(control, i) for i in range(k) if i != control]
    return pairs

def buildPvalMatrix(pvalues, k, pairs, cnames, control):
    if control is None:
        matrix_raw = pd.DataFrame(np.nan, index=cnames, columns=cnames)
        for (i, j), pval in zip(pairs, pvalues):
            matrix_raw.iloc[i, j] = pval
            matrix_raw.iloc[j, i] = pval
    else:
        matrix_raw = pd.DataFrame(np.nan, columns=cnames, index=[0])
        for _, j in pairs:
            matrix_raw.iloc[0, j] = pvalues[j]
    return matrix_raw

def correctForMonotocity(pvalues):
    for i in range(1, len(pvalues)):
        pvalues[i] = max(pvalues[i], pvalues[i - 1])
    return pvalues

def friedmanPost(data, control=None):
    k = data.shape[1]
    N = data.shape[0]
    control = processControlColumn(data, control)
    pairs = generatePairs(k, control)
    
    mean_rank = rankdata(-data.values, axis=1, method='average').mean(axis=0)
    sd = np.sqrt(k * (k + 1) / (6 * N))
    pvalues = [2 * (1 - norm.cdf(abs(mean_rank[i] - mean_rank[j]) / sd)) for i, j in pairs]

    matrix_raw = buildPvalMatrix(pvalues, k, pairs, data.columns, control)
    return matrix_raw

def setUpperBound(vector, bound):
    return np.minimum(vector, bound)

def countRecursively(k):
    res = [0]
    if k > 1:
        res += countRecursively(k - 1)
        for j in range(2, k + 1):
            additional_values = [int((x + factorial(j) / (2 * factorial(j - 2)))) for x in countRecursively(k - j)]
            res += additional_values
    return sorted(set(res))

def adjustShaffer(raw_matrix):
    if not isinstance(raw_matrix, (pd.DataFrame, np.ndarray)):
        raise ValueError("This correction method requires a DataFrame or ndarray with the p-values of all the pairwise comparisons.")
    
    if raw_matrix.shape[0] != raw_matrix.shape[1]:
        raise ValueError("This correction method requires a square matrix or DataFrame with the p-values of all the pairwise comparisons.")
    
    k = raw_matrix.shape[0]
    pairs = generatePairs(k, None)
    raw_pvalues = [raw_matrix.iloc[i, j] for i, j in pairs]

    sk = countRecursively(k)[1:]  # Exclude 0 from the count

    # Replicate elements of sk (excluding the last one) according to the differences between elements
    replicated = np.repeat(sk[:-1], np.diff(sk))

    # Get the last element of sk
    last_element = sk[-1]

    # Combine the replicated part with the last element
    t_i = np.concatenate([replicated, [last_element]])
    t_i = list(t_i)
    t_i.reverse()

    o = np.argsort(raw_pvalues)
    adj_pvalues = np.array(raw_pvalues)[o] * t_i
    adj_pvalues = setUpperBound(adj_pvalues, 1) 
    adj_pvalues = correctForMonotocity(adj_pvalues)

    # Restoring original order
    adj_pvalues = adj_pvalues[o.argsort()]

    # Regenerating the matrix
    adj_matrix = raw_matrix.copy()
    for (i, j), pval in zip(pairs, adj_pvalues):
        adj_matrix.iloc[i, j] = adj_matrix.iloc[j, i] = pval

    return adj_matrix

def friedman_shaffer_scmamp(df):
    '''
    This function performs the Friedman test and the Shaffer post hoc test
    using the scmamp package.

    :param df: a pandas DataFrame with the results of the experiments
    :type df: pandas.DataFrame
    :return: a dictionary with the results of the Friedman test and the Shaffer post hoc test
    :rtype: dict
    '''
    # Create a R script to perform the Friedman test and the Shaffer post hoc test
    r_script = """
    library(scmamp)

    data <- read.csv("temp_data.csv", header = TRUE, row.names = NULL)
    htest <- friedmanTest(data)
    saveRDS(htest, file = "temp_htest.rds")
    raw.pvalues <- friedmanPost(data)
    saveRDS(raw.pvalues, file = "temp_raw_pvalues.rds")
    adjusted.pvalues <- adjustShaffer(raw.pvalues)
    saveRDS(adjusted.pvalues, file = "temp_adjusted_pvalues.rds")
    """
    # save the script to a temporary file
    with open('temp_script.R', 'w') as f:
        f.write(r_script)
    # we do not need the DataFrame index
    df = df.reset_index(drop=True)
    df.to_csv('temp_data.csv', index=False)
    subprocess.run(["Rscript", "temp_script.R"])

    # Read the RDS file temp_htest.rds into a Python dictionary
    htest_R = pyreadr.read_r("temp_htest.rds")
    Friedman_test = dict()
    Friedman_test["statistic"] = htest_R[None]['statistic'][0]
    Friedman_test["parameter"] = htest_R[None]['parameter'][0]
    Friedman_test["pvalue"] = htest_R[None]['p.value'][0]
    Friedman_test["method"] = htest_R[None]['method'][0]
    Friedman_test["data_name"] = htest_R[None]['data.name'][0]

    # Read the RDS file temp_raw_pvalues.rds into a Python dataframe
    raw_pvalues = pyreadr.read_r("temp_raw_pvalues.rds")
    raw_pvalues = raw_pvalues[None]
    raw_pvalues.columns = df.columns
    raw_pvalues.index = df.columns

    # Read the RDS file temp_adjusted_pvalues.rds into a Python dataframe
    adjusted_pvalues = pyreadr.read_r("temp_adjusted_pvalues.rds")
    adjusted_pvalues = adjusted_pvalues[None]
    adjusted_pvalues.columns = df.columns
    adjusted_pvalues.index = df.columns

    # Clean up
    os.remove('temp_data.csv')
    os.remove('temp_script.R')
    os.remove('temp_htest.rds')
    os.remove('temp_raw_pvalues.rds')
    os.remove('temp_adjusted_pvalues.rds')

    results = {
        'Friedman_test': Friedman_test,
        'raw_pvalues': raw_pvalues,
        'adjusted_pvalues': adjusted_pvalues
    }
    return results



def determine_color(val, row_name, col_name, means):
    if val < 0.05:
        if means[row_name] > means[col_name]:
            return 'green'
        else:
            return 'red'
    else:
        return 'gray'
    
def format_text(val):
    return f"{val:.2f}"

def friedman_dunn_test(dataframe):
    # Make a copy of the dataframe to avoid modifying the original one
    df = dataframe.copy()
    # Transpose the DataFrame to get the algorithms as rows and datasets as columns
    df = df.T
    # Perform the Friedman test
    friedman_result = pg.friedman(df)

    # Display the Friedman test results
    print(friedman_result)
    # Get the p-value from the Friedman test result
    friedman_pvalue = friedman_result['p-unc'][0]

    # Perform the Bonferroni-Dunn post hoc test
    posthoc_dunn = pg.pairwise_ttests(data=df, parametric=False, padjust='bonferroni')

    # Display the post hoc test results
    print(posthoc_dunn)


def friedman_nemenyi_test(dataframe, already_transposed=False, filename="nemenyi.jpg"):
    # Make a copy of the dataframe to avoid modifying the original one
    df = dataframe.copy()
    
    # Replace '_' (not preceded by a backslash) with '\_' in column names for LaTeX compatibility
    df.columns = df.columns.str.replace(r'(?<!\\)_', r'\_')
    
    # Compute mean values for each algorithm
    means = df.mean()

    means_2 = means.copy()
    means_2.reset_index(drop=True, inplace=True)
    means_2.index = means_2.index.astype(str)

    # Perform Friedman test
    ranks = df.rank(axis=1, method='average', ascending=False)
    friedman_result = friedmanchisquare(*ranks.values.T)

    # Compute mean ranks
    mean_ranks = ranks.mean()

    # Transpose the DataFrame to get the algorithms as rows and datasets as columns
    if not already_transposed:
        df = df.T

    print(df)

    # Perform Nemenyi posthoc test
    nemenyi_result = posthoc_nemenyi(df.values)
    print("nemenyi_result")
    print(nemenyi_result)
    print(df.index)
    nemenyi_result.columns = df.columns
    nemenyi_result.index = df.columns

    # Create a DataFrame of the Nemenyi results
    nemenyi_df = pd.DataFrame(nemenyi_result)
    print("nemenyi_df")
    print(nemenyi_df)

    # Create a custom function to convert the DataFrame to good data for a heatmap
    # the values < 0.05 and "good" for the algorithm in the column are going to be 2 - value
    # the values < 0.05 and "bad" for the algorithm in the row are going to be value
    # the rest of values are going to be 1
    # this function returns a DataFrame with the same shape as the original one
    # always keep track of the name of the row and column of each cell,
    # because the heatmap will be created using the row and column names
    # a value is good if means[row_name] > means[col_name]
    # a value is bad if means[row_name] < means[col_name]
    def to_heatmap_custom(df, means):
        heatmap_data = pd.DataFrame(1, index=df.index, columns=df.columns)
        for i, row_name in enumerate(df.index):
            for j, col_name in enumerate(df.columns):
                value = df.loc[row_name, col_name]
                if value < 0.05:
                    heatmap_data.loc[row_name, col_name] = 2 - value if means[i] > means[j] else value 
                if i == j:
                    heatmap_data.loc[row_name, col_name] = 3      
        return heatmap_data

    # Create a custom function to convert the DataFrame to a LaTeX table
    def to_latex_custom(df, means):
        header = ' & ' + ' & '.join(df.columns) + ' \\\\ \\hline'
        rows = []
        for row_name, row in df.iterrows():
            formatted_values = []
            for col_name, val in row.iteritems():
                if val < 0.05:
                    direction = '+' if means[row_name] > means[col_name] else '-'
                    formatted_values.append(f"\\bf{{{val:.3f} {direction}}}")
                else:
                    formatted_values.append(f"{val:.3f}")
            rows.append(f"{row_name} & " + ' & '.join(formatted_values) + ' \\\\ \\hline')
        return '\\begin{tabular}{|' + 'c|' * (df.shape[1] + 1) + '}\n' + header + '\n' + '\n'.join(rows) + '\n\\end{tabular}'

    def to_image_custom(df_original, df_heatmap_data, filename):
        # Create a colormap from the list of colors
        cmap = ListedColormap(['red', 'gray', 'green', 'white'])
        sns.set(font_scale=1.2)
        plt.figure(figsize=(12, 10))
        col_labels = df_original.columns
        row_labels = df_original.index
        plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = False, labeltop=True)
        sns.heatmap(df_heatmap_data, fmt="d", linewidths=.5, cbar=False, cmap=cmap, xticklabels=col_labels, yticklabels=row_labels)
        # save the figure
        plt.savefig(filename, bbox_inches='tight')
        plt.show()

    # Convert the DataFrame to a LaTeX table
    nemenyi_table = to_latex_custom(nemenyi_df, means)

    nemenyi_df_2 = nemenyi_df.copy()
    nemenyi_df_2.reset_index(drop=True, inplace=True)
    nemenyi_df_2.columns = nemenyi_df_2.index
    # change the column names to strings
    nemenyi_df_2.columns = nemenyi_df_2.columns.astype(str)

    nemenyi_table_2 = to_latex_custom(nemenyi_df_2, means_2)
    nemenyi_df.columns = df.columns
    nemenyi_df.index = df.columns
    print("nemenyi_df_before_ordering")
    print(nemenyi_df)
    ordered_columns = ["RANSAC-LP-957", "RANSAC-LP-747", "RANSAC-LP-558", "RANSAC-LP-388", "RANSAC-LP-239", "RANSAC-LP-109", 
                    "RANSAC-957", "RANSAC-747", "RANSAC-558", "RANSAC-388", "RANSAC-239", "RANSAC-109"]
    nemenyi_df = nemenyi_df.loc[ordered_columns,ordered_columns]
    nemenyi_df_heatmap_data = to_heatmap_custom(nemenyi_df, means)
    print("nemenyi_df_heatmap_data")
    print(nemenyi_df_heatmap_data)
    to_image_custom(nemenyi_df, nemenyi_df_heatmap_data, filename)

    results = {
        'friedman_result': friedman_result,
        'mean_ranks': mean_ranks,
        'nemenyi_result': nemenyi_result,
        'nemenyi_df': nemenyi_df,
        'nemenyi_table': nemenyi_table,
        'nemenyi_df_2': nemenyi_df_2,
        'nemenyi_table_2': nemenyi_table_2
    }

    return results






