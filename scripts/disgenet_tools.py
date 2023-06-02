"""
GDAD数据库脚本，用于从DisGeNET获取Gene-Disease Association数据，以及对数据进行处理。
"""
import os
import re
import typing

import numpy as np
import pandas as pd
import requests
import swifter
import tqdm


def disgenet_read(disgenet_file_path: str) -> typing.Union[pd.DataFrame, None]:
    """读取DisGeNET数据库的数据。TSV文件，带有列名，全部读取为str类型。

    Args:
        disgenet_file_path (str): DisGeNET数据库的文件路径。

    Returns:
        disgenet_df (pd.DataFrame|None)：读取得到的DataFrame，全部元素为str类型。
    """
    print("disgenet_read开始。")
    if (
        os.path.exists(disgenet_file_path) and os.path.isfile(disgenet_file_path)
    ) is False:
        print(f"disgenet_read错误：输入的DisGeNET文件路径错误：{disgenet_file_path}")
        return None
    disgenet_df = pd.read_csv(
        filepath_or_buffer=disgenet_file_path,
        sep="\t",
        header=0,
        index_col=None,
        encoding="utf-8",
        na_filter=False,
        dtype=str,
    )

    print("disgenet_read完成。")
    return disgenet_df


def disgenet_response_json_to_dataframe(
    response_json: list,
) -> pd.DataFrame:
    """把DisGeNET的响应值的json的列表转换成DataFrame。

    Args:
        response_json (list[dict[str]]): 使用DisGeNET REST API得到的response.json()。为一个包含多个字典的列表，字典的键值都是字符串。

    Returns:
        disgenet_response_df (pd.DataFrame): 结果的DataFrame。列名为原先的每个字典的键，应该是相同的，原先的每一个字典的值变成每一行元素。
    """
    series_list = []  # 存放所有Series的列表，防止每次pd.concat()，效率会很低。
    for curr_dict in response_json:
        curr_series = pd.Series(curr_dict)
        series_list.append(curr_series)

    # 如果是空的，无论是何种原因，返回也是空的
    if series_list == []:
        disgenet_response_df = pd.DataFrame([])
        return disgenet_response_df

    disgenet_response_df = pd.concat(series_list, axis=1)
    disgenet_response_df = disgenet_response_df.T
    disgenet_response_df.reset_index(drop=True, inplace=True)
    return disgenet_response_df


def disgenet_api(
    gene_symbol: str,
) -> list:
    """官方的DisGeNET REST API，发起一次查询请求。
    使用给定的基因名称列表，支持list|np.ndarray|pd.Series类型。使用DisGeNET REST API接口查询与给定基因相关的全部基因信息。

    Args:
        gene_symbol (str): 给定的基因名，符合gene symbol标准。

    Returns:
        associated_disease_list (list): 与给定的基因相关的全部疾病的信息。

    代码使用了DisGeNET REST API，使用了新的认证系统。
    """
    # 这个例子中使用了python的默认http库
    # 使用下面的格式创建一个字典，把两个键的值改成DisGeNET的账号密码，如果没有账号密码，可以在这里创建一个：https://www.disgenet.org/signup/
    auth_params = {
        "email": "LawrenceLiu_023@outlook.com",
        "password": "liujiahuan104530",
    }
    api_host = "https://www.disgenet.org/api"
    api_key = None
    session = requests.Session()

    try:
        response = session.post(api_host + "/auth/", data=auth_params)
        if response.status_code == 200:
            # Lets store the api key in a new variable and use it again in new requests
            # 保存API密钥，在新的requests中再次使用
            json_response = response.json()
            api_key = json_response.get("token")
            # Comment following two lines if you don't want your API key to show up in the terminal
            # print(api_key + "This is your user API key.")
            # print(f"disgenet_api: This is your user API key:{api_key}")
        else:
            # 返回码200: Successful operation.
            # 返回码400: Validation exception.
            # 返回码404: Gene/s not found.
            print(response.status_code)
            print(response.text)
    except requests.exceptions.RequestException as req_ex:
        print(req_ex)
        print("disgenet_api: Something went wrong with the request.")

    if api_key:
        # Add the api key to the requests headers of the requests Session object in order to use the restricted endpoints.
        # 在requests Session对象的requests header中添加API密钥，来使用受限的endpoints
        session.headers.update({"Authorization": "Bearer %s" % api_key})

        # Lets get all the diseases associated to a gene eg. APP (EntrezID 351) and restricted by a source.
        # 获得一个基因相关的所有及疾病，可以限制数据源。这里是范例。
        # gda_response = session.get(api_host + '/gda/gene/351', params={'source': 'UNIPROT'})
        # gda_response = session.get(
        #     api_host + "/gda/gene/BRCA1", params={"source": "UNIPROT"}
        # )

        # 可以选择的数据来源参见https://www.disgenet.org/dbinfo#section44
        # 这里选择GDA（Gene-Disease Associations）数据，数据源选择“CURATED”，包含了UNIPROT等多个数据库的实验信息，不想要计算预测的INFERRED信息
        gda_response = session.get(
            api_host + f"/gda/gene/{gene_symbol}", params={"source": "CURATED"}
        )
        gda_response_json = gda_response.json()

        # 输入的是BRCA1的时候，本结果是包含五个字典的列表，字典都是每个疾病相关的信息，字典的key完全相同。
        # 如果没有找到，response.json()={'detail': "The query didn't return any results", 'status_code': 404}
    else:  # 如果有意外也返回空列表
        print(f"disgenet_api错误：api_key获取失败。")
        return []

    # 关闭会话
    if session:
        session.close()

    if isinstance(gda_response_json, dict):  # 如果是单个字典，统一成列表类型
        associated_disease_list = [gda_response_json]
    elif isinstance(gda_response_json, list):  # 如果是列表，保持格式即可
        associated_disease_list = gda_response_json
    else:  # 没有遇到过的其他类型，报错然后返回空列表即可
        print(f"disgenet_api错误：出现了预期以外的response.json:{gda_response_json}")
        return []

    # 如果找到数据，列表肯定至少有一个元素。如果是没找到数据，会有"status_code"键，返回空列表。
    if associated_disease_list[0].get("status_code", None) != None:
        return []

    return associated_disease_list


def disgenet_api_gene_symbol_array_search(
    gene_symbol_array: list | np.ndarray | pd.Series,
    cache_file_path: str,
    start_index: int = 0,
) -> pd.DataFrame:
    """查询一系列的gene symbol在DisGeNET中相关疾病的信息。
    查询结果实时写入同一个文件中。可以设置开始的位置，结合之前执行的日志，能从响应中断的地方继续进行查询。

    Args:
        gene_symbol_array (list | np.ndarray | pd.Series): 基因名的列表或者其他能转换成列表的数据。
        cache_file_path (str): 缓存文件，保存每一个已经请求到的gene_symbol的相关信息。
        start_index (int, optional): 开始查询的索引0-based，可以结合日志信息从中断的地方继续进行查询。默认为0，从头开始查询。

    Returns:
        gene_symbol_array_df (pd.DataFrame): 每一行为一个基因与疾病的相互关系。
    """
    print("disgenet_api_gene_symbol_array_search开始。")
    # 读取基因名称数据
    gene_symbol_list = list(gene_symbol_array)  # 去除重复的基因名称
    gene_symbol_num = len(gene_symbol_list)  # 记录全部基因名称个数
    if start_index >= gene_symbol_num:
        print(
            f"disgenet_api_gene_symbol_array_search错误：输入的起始索引错误{start_index}，总基因个数为{gene_symbol_num}"
        )
        return pd.DataFrame([])

    p_bar = tqdm.tqdm(total=len(gene_symbol_list))  # 按照全部基因名称的列表创建进度条
    p_bar.set_description("查询基因名")
    cache_file_buffer = open(cache_file_path, mode="w", encoding="utf-8")
    gene_df_list = []  # 保存所有的查询结果的列表
    first = True
    for curr_gene_index in range(gene_symbol_num):  # 使用下标索引的方式，可以实现跳过一部分，从指定的索引开始查询
        p_bar.update(1)

        # 如果还没有达到起始的索引，进行跳过
        if curr_gene_index < start_index:
            continue

        curr_gene = gene_symbol_list[curr_gene_index]
        curr_gene_list = disgenet_api(curr_gene)

        # 直接跳过没有找到的基因
        if curr_gene_list == []:
            continue

        curr_gene_df = disgenet_response_json_to_dataframe(curr_gene_list)

        # 第一个数据写入需要带上表头，后续写入的数据不需要带上表头
        if first is True:
            first = False  # 表明已经有写入数据
            curr_gene_df.to_csv(
                cache_file_buffer,
                header=True,
                index=False,
                sep="\t",  # 必须使用制表符分隔，因为单个项中已经使用了逗号分隔
                encoding="utf-8",
                mode="a",
            )
        else:
            curr_gene_df.to_csv(
                cache_file_buffer,
                header=False,  # 已经不需要表头了
                index=False,
                sep="\t",  # 必须使用制表符分隔，因为单个项中已经使用了逗号分隔
                encoding="utf-8",
                mode="a",
            )

        gene_df_list.append(curr_gene_df)
        cache_file_buffer.flush()  # 把缓存中的内容写入磁盘，防止丢失

    p_bar.close()  # 关闭进度条
    cache_file_buffer.close()  # 关闭持续写入的文件缓冲对象

    # 检查一下有没有列名不同的结果，也只是提醒一下，结果还是要的
    for gene_df_index in range(len(gene_df_list)):
        if gene_df_list == 0:
            continue
        if list(gene_df_list[gene_df_index].columns) != list(
            gene_df_list[gene_df_index - 1].columns
        ):
            print("disgenet_api_gene_symbol_array_search错误：存在列名不同的结果。")
            print(gene_df_list[gene_df_index])
            print(gene_df_list[gene_df_index - 1])
            break

    gene_symbol_array_df = pd.concat(gene_df_list, axis=0)
    gene_symbol_array_df.reset_index(drop=True, inplace=True)

    print("disgenet_api_gene_symbol_array_search完成。")
    return gene_symbol_array_df


def disgenet_api_gene_symbol_array_search_combine(
    file_path_list: list[str],
) -> pd.DataFrame:
    """将多个DisGeNET查询结果文件合并，并剔除相同的冗余。
    本函数结合disgenet_api_gene_symbol_array_search使用，可以将搜索中断而不得不分为多次搜索的结果快速合并起来。

    Args:
        file_path_list (list[str]): 查询结果文件路径，长度不限。

    Returns:
        combined_df (pd.DataFrame): 合并后的结果。
    """
    print("disgenet_api_gene_symbol_array_search_combine开始。")
    for file_path in file_path_list:
        if (os.path.exists(file_path) and os.path.isfile(file_path)) is False:
            print(f"disgenet_api_gene_symbol_array_search_combine错误：文件路径错误：{file_path}")
            return pd.DataFrame([])

    file_num = len(file_path_list)
    if file_num == 1:
        print(f"disgenet_api_gene_symbol_array_search_combine错误：仅有一个文件，不需要合并。")
        return pd.DataFrame([])

    # 开始读取文件
    file_df_list = []
    p_bar = tqdm.tqdm(total=file_num)
    p_bar.set_description("读取文件")
    for file_path in file_path_list:
        p_bar.update(1)
        file_df = pd.read_csv(
            filepath_or_buffer=file_path,
            header=0,
            index_col=None,
            sep="\t",
            na_filter=False,
            encoding="utf-8",
        )
        file_df_list.append(file_df)
    p_bar.close()

    # 合并结果
    combined_df = pd.concat(file_df_list, axis=0, ignore_index=False)
    # 剔除冗余
    combined_df.drop_duplicates(inplace=True, keep="first")
    # 重置索引
    combined_df.reset_index(drop=True, inplace=True)
    print("disgenet_api_gene_symbol_array_search_combine完成。")
    return combined_df


def disgenet_api_response_df_to_tsv(
    disgenet_response_df: pd.DataFrame, tsv_file_path: str
) -> bool:
    """将DisGeNET返回的结果DataFram转换为tsv文件。
    结果包含列名，分隔符为"\t"，不包含索引，文件编码为utf-8。

    Args:
        disgenet_response_df (pandas.DataFrame): DisGeNET REST API的response.json转换得到的pandas.DataFrame。
        tsv_file_path (str): 结果写入的文件路径。

    Returns:
        success (bool): 是否成功。没啥用，写着玩的。
    """
    print(f"disgenet_api_response_df_to_csv开始：写入路径{tsv_file_path}")
    try:
        disgenet_response_df.to_csv(
            path_or_buf=tsv_file_path,
            header=True,
            index=False,
            sep="\t",
            encoding="utf-8",
        )
    except Exception as ex:
        print(f"disgenet_api_response_df_to_tsv错误：{ex}")
        success = False
        return success
    print(f"disgenet_api_response_df_to_csv完成：写入路径{tsv_file_path}")
    return True


def disgenet_tsv_search_keyword(
    disgenet_tsv_file_path: str,
    keyword_list: list[str],
    column_name_list: list[str] = [],
) -> pd.DataFrame:
    """对于DisGeNET的TSV文件，在指定的列中搜索指定的关键词。

    Args:
        disgenet_tsv_file_path (str): DiGeNET的数据文件。
        column_name_list (list[str]): 列名的列表，默认为空，表示在所有列中搜索。
        keyword_list (list[str]): 关键词列表，要求在某一行需要包含所有的关键词，可以在不同的列中。

    Returns:
        search_result_df (pd.DataFrame): 搜索的结果，保持原始格式。
    """
    print("disgenet_tsv_search_keyword: 开始。")
    # 判断文件是否存在
    if (
        os.path.exists(disgenet_tsv_file_path)
        and os.path.isfile(disgenet_tsv_file_path)
    ) is False:
        print(f"disgenet_tsv_search_keyword: 错误的路径: {disgenet_tsv_file_path}。")
        return pd.DataFrame([])

    # 读取DisGeNET数据
    disgenet_df = pd.read_csv(
        filepath_or_buffer=disgenet_tsv_file_path,
        header=0,
        index_col=None,
        sep="\t",
        na_filter=False,
        encoding="utf-8",
        dtype=str,
    )

    # 判断列名是否有错误
    if (set(column_name_list) <= set(disgenet_df.columns)) is False:
        print(f"disgenet_tsv_search_keyword: 错误的列名: {column_name_list}。")
        return pd.DataFrame([])

    # 列名的默认值
    if column_name_list == []:
        column_name_list = list(disgenet_df.columns)

    # 精简数据，搜索用的不必使用全部数据
    disgenet_search_df = disgenet_df.loc[:, column_name_list].copy(deep=True)

    keyword_num = len(keyword_list)

    def disgenet_row_contain_keyword(disgenet_search_row: pd.Series):
        """用于apply()。对于每一行数据，判断是否存在指定的关键词。"""
        keyword_if_found_list = [False] * keyword_num

        for i, curr_keyword in enumerate(keyword_list):
            column_content_list = list(disgenet_search_row)
            curr_keyword_find_list = map(
                lambda x: find_ic(string=x, pattern=curr_keyword), column_content_list
            )
            curr_keyword_find_list = list(curr_keyword_find_list)
            if (set(curr_keyword_find_list) == {-1}) is False:  # 至少在一列中找到了关键词
                keyword_if_found_list[i] = True  # 对应位置的值置为True，说明这个编号的关键词已经找到

        if set(keyword_if_found_list) == {True}:  # 如果所有的关键词都找到了
            return True
        return False

    search_result_df_index_series = disgenet_search_df.swifter.apply(
        disgenet_row_contain_keyword, axis=1
    )
    search_result_df = disgenet_df.loc[search_result_df_index_series, :]

    print("disgenet_tsv_search_keyword: 完成。")
    return search_result_df


def find_ic(string: str, pattern: str) -> int:
    """忽略大小写的find()

    Args:
        string (str): 在此字符串中查找。
        pattern (str): 需要寻找的子字符串。

    Returns:
        index (int): 如果找到，返回下标，否则返回-1。
    """
    search_result = re.search(pattern=pattern, string=string, flags=re.IGNORECASE)
    if search_result is None:
        return -1
    return search_result.start()


if __name__ == "__main__":
    # # 读取GENCODE数据库包含的全部基因名
    # GENCODE_GENE_SYMBOL_FILE_PATH = "/mnt/disk2/liujh/workspaces/data/GENCODE/analysis_results/gencode_v19_promoter_gene_symbol.txt"
    # gencode_gene_symbol_list = pd.read_csv(
    #     GENCODE_GENE_SYMBOL_FILE_PATH,
    #     header=None,
    #     index_col=None,
    #     sep="\t",
    #     na_filter=False,
    #     encoding="utf-8",
    #     dtype=str,
    # )
    # gencode_gene_symbol_list = gencode_gene_symbol_list.iloc[:, 0]
    # gencode_gene_symbol_list = list(gencode_gene_symbol_list)

    # # 根据基因名称查询对应的GDA数据
    # DISGENET_API_CACHE_FILE_PATH = "这里填写查询结果的存放路径"
    # disgenet_api_gene_symbol_array_search(
    #     gene_symbol_array=gencode_gene_symbol_list,  # 基因名称列表
    #     cache_file_path=DISGENET_API_CACHE_FILE_PATH,  # 查询结果的存放目录，用于实时保存，防止网络断开
    #     start_index=0,  # 从下标为0的基因开始查询
    # )
    # # 即使一次性查询成功了，也建议使用disgenet_api_gene_symbol_array_search_combine()来处理一下结果，它不仅可以用来合并不同的结果，也可以用来去重

    # 查询疾病名称包含了"breast"的GDA数据
    # DISGENET_CURATED_GENCODE_TSV_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/analysis_results/disgenet_results/disgenet_gda_curated_gencode.tsv"
    # keyword_list = ["breast"]
    # search_result_df = disgenet_tsv_search_keyword(
    #     disgenet_tsv_file_path=DISGENET_CURATED_GENCODE_TSV_FILE_PATH,
    #     keyword_list=keyword_list,
    #     column_name_list=["disease_name"],
    # )
    # print(search_result_df)
    # search_result_df.to_csv(
    #     "/mnt/disk2/liujh/workspaces/20230221_database/analysis_results/disgenet_results/disgenet_search_result_breast.tsv",
    #     header=True,
    #     index=False,
    #     sep="\t",
    #     encoding="utf-8",
    # )
