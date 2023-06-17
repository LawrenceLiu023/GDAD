"""
本文件中的各种功能用于检查数据的格式等信息。
"""
import re
import typing
import os
import numpy as np
import pandas as pd
import tqdm


def bed_get_length_series(bed_file_path: str) -> pd.Series:
    """读取BED文件获取长度的Series

    Args:
        file_path (str): 文件的路径.

    Returns:
        length_series (pandas.Series): 序列长度统计。
    """
    print("bed_get_length_series开始。")
    if (os.path.exists(bed_file_path) and os.path.isfile(bed_file_path)) is False:
        print(f"bed_get_length_series错误：路径错误：{bed_file_path}")
        return pd.Series([])

    bed_file_df = pd.read_csv(
        bed_file_path,
        header=None,
        index_col=None,
        sep="\t",
        na_filter=False,
        encoding="utf-8",
    )

    bed_file_df = bed_file_df.iloc[:, 1:3]
    bed_file_df = bed_file_df.apply(lambda x: x.astype("int"), axis=0)
    length_series = bed_file_df.apply(lambda x: x.iloc[1] - x.iloc[0], axis=1)
    print("bed_get_length_series完成。")
    return length_series


def df_columns_length_analyse(df: pd.DataFrame) -> dict:
    """分析数据框所有列的字符串长度

    Args:
        df (pandas.DataFrame): 输入DataFrame。

    Returns:
        columns_length_description_dict (dict): 分析的结果。每个键是列名，每个值都是分析结果的文本。
    """
    df = df.astype("str")  # 似乎必须赋值才能修改变量本身

    def series_length_analyse(s: pd.Series) -> str:
        s_length = s.apply(lambda x: len(x))
        return str(s_length.describe())

    columns_length_description_series = df.apply(series_length_analyse, axis=0)
    columns_length_description_dict = {}
    for i, value in enumerate(columns_length_description_series):
        columns_length_description_dict.update(
            {columns_length_description_series.index[i]: value}
        )
    return columns_length_description_dict


def remap_bed_to_df(remap_bed_file_path: str) -> pd.DataFrame:
    """把ReMap数据库的BED文件，转换成DataFrame。
    把第4列的"<TF>:<细胞系>"拆分成两列。第5列的score及以后的数据剔除。格式为["chr","start", "end", "tf", "cell_line"]。其中细胞系名称是用","隔开的。

    Args:
        remap_bed_file_path (str): ReMap数据库的BED文件路径。

    Returns:
        remap_df (pandas.DataFrame): 读取ReMap的BED文件得到的DataFrame，把第4列的"<TF>:<细胞系>"拆分成两列。格式为["chr","start", "end", "tf", "cell_line"]
    """
    print("remap_bed_to_df开始。")
    if (
        os.path.exists(remap_bed_file_path) and os.path.isfile(remap_bed_file_path)
    ) is False:
        print(f"remap_bed_to_df错误：输入路径错误：{remap_bed_file_path}")
        return pd.DataFrame([])

    remap_df = pd.read_csv(
        remap_bed_file_path, header=None, index_col=None, sep="\t", dtype=str
    )
    remap_df = remap_df.iloc[:, :4]  # 剔除使用不到的数据

    tf_cell_split_df = remap_df.iloc[:, 3].str.split(
        pat=":", expand=True
    )  # 如果不加expand参数，得到的会是一个Series，每个元素为分隔后的列表
    remap_df = pd.concat([remap_df.iloc[:, :3], tf_cell_split_df], axis=1)
    remap_df.columns = ["chr", "start", "end", "tf", "cell_line"]
    print("remap_bed_to_df完成。")
    return remap_df


def df_columns_number_range_analyse(df: pd.DataFrame) -> dict:
    """分析数值型列的范围。

    Args:
        df (pandas.DataFrame): 输入数据，每一列都应该是可以转换为数值型的

    Returns:
        columns_number_range_dict (dict): 分析结果，键为列名，值为分析结果的字符串。
    """
    df = df.astype("float")

    columns_number_range_description_series = df.apply(
        lambda x: str(x.describe()), axis=0
    )
    columns_number_range_dict = {}
    for i, value in enumerate(columns_number_range_description_series):
        columns_number_range_dict.update(
            {columns_number_range_description_series.index[i]: value}
        )
    return columns_number_range_dict


def ccle_sample_info_cell_line_name_standardise(
    ccle_sample_info_file_path: str, cell_line_name_array: list | pd.Series | np.ndarray
) -> dict:
    """根据CCLE提供的sample_info.csv文件标准化一系列细胞系名称。

    Args:
        ccle_sample_info_file_path (str): CCLE数据库的sample_info.csv的路径。第2-5列包含了细胞系名称和别名的信息，依次为["cell_line_name","stripped_cell_line_name","CCLE_Name","alias"]
        cell_line_name_array (list|pd.Series|np.ndarray): 一系列细胞系名称，只要可以转换为列表即可。

    Returns:
        standardised_cell_line_name_dict (dict): 标准化过后的细胞系名称字典，键为之前的名称，值为标准化之后的名称。标准全部使用CCLE的sample_info.csv的第二列"cell_line_name"，如果没找到的话值为None。
    """
    print("ccle_sample_nifo_cell_line_name_standardise开始。")
    if (
        os.path.exists(ccle_sample_info_file_path)
        and os.path.isfile(ccle_sample_info_file_path)
    ) is False:
        print(
            f"ccle_sample_info_cell_line_name_standardise错误：输入的sample_info.csv路径错误:{ccle_sample_info_file_path}"
        )
        return dict()

    cell_line_name_list = list(cell_line_name_array)
    ccle_sample_info_df = pd.read_csv(
        ccle_sample_info_file_path,
        header=0,
        index_col=None,
        sep=",",
        na_filter=False,
        encoding="utf-8",
        dtype=str,
    )
    ccle_sample_info_df = ccle_sample_info_df.loc[
        :, ["cell_line_name", "stripped_cell_line_name", "CCLE_Name", "alias"]
    ]

    def ccle_sample_info_row_match(
        row_series: pd.Series, pattern: str
    ) -> typing.Union[str, float]:
        """对sample_info.csv的每一行进行正则表达式的检查，如果没有匹配就返回np.nan，方便直接使用dropna()剔除。"""
        row_cell_line_name = row_series.iloc[0]  # 标准化的细胞系名称
        current_name_match = None
        for current_name in row_series:
            current_name_match = re.match(
                pattern=pattern, string=current_name, flags=re.IGNORECASE
            )
            if current_name_match:
                return row_cell_line_name
        return np.nan

    cell_line_name_match_result_list = []
    for curr_cell_line_name in tqdm.tqdm(cell_line_name_list, desc="比较目标细胞系名列表"):
        curr_cell_line_name_match_series = ccle_sample_info_df.apply(
            ccle_sample_info_row_match, pattern=curr_cell_line_name, axis=1
        )
        curr_cell_line_name_match_series.dropna(
            inplace=True
        )  # 剔除所有np.nan就可以判断到底有没有匹配成功
        if curr_cell_line_name_match_series.shape[0] > 0:  # 如果找到了就返回标准化的名字
            cell_line_name_match_result_list.append(
                curr_cell_line_name_match_series.iloc[0]
            )
        else:  # 如果没找到就返回None
            cell_line_name_match_result_list.append(None)

    standardised_cell_line_name_dict = zip(
        cell_line_name_list, cell_line_name_match_result_list
    )
    standardised_cell_line_name_dict = dict(standardised_cell_line_name_dict)
    print("ccle_sample_nifo_cell_line_name_standardise完成。")
    return standardised_cell_line_name_dict

# 以下写的语句，只有执行本脚本时才会执行，如果import本脚本不会执行
if __name__ == "__main__":  
    print("Hello!")  # 没啥用，只是不写这句的话，IDE会提示我有语法错误
