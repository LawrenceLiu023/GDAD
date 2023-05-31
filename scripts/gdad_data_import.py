"""
本文件用于格式化原始数据，用于直接导入gdad数据库。
"""

import os
import numpy as np
import pandas as pd
import tqdm
import swifter

# g4数据表的字段名称列表
G4_TABLE_FIELD_LIST = [
    "chr",
    "start",
    "end",
    "strand",
    "cell_line",
    "technology",
    "doi",
]
# gene_sequence数据表的字段名称列表
GENESEQUENCE_TABLE_FIELD_LIST = ["chr", "start", "end", "gene_symbol"]

# gda数据表的字段名称列表
GDA_TABLE_FIELD_LIST = [
    "gene_id",
    "gene_symbol",
    "uniprot_id",
    "gene_dsi",
    "gene_dpi",
    "gene_pli",
    "protein_class",
    "protein_class_name",
    "disease_id",
    "disease_name",
    "disease_class",
    "disease_class_name",
    "disease_type",
    "disease_semantic_type",
    "gda_score",
    "ei",
    "el",
    "year_initial",
    "year_final",
]


# 设置允许的染色体编号名称
def read_gdad_chr_tsv(gdad_chr_tsv_file_path: str) -> set:
    """从TSV文件中读取GDAD允许的染色体名称。

    Args:
        gdad_chr_tsv_file_path (str): 保存了GDAD允许的染色体名称的文件，其中每个染色体编号独立成行，注释行开头为"#"

    Returns:
        chr_set (set): 允许的全部染色体名称的元组。
    """
    print("read_gdad_chr_tsv: 开始。")
    gdad_chr_df = pd.read_csv(
        filepath_or_buffer=gdad_chr_tsv_file_path,
        header=None,
        index_col=None,
        comment="#",
        sep="\t",
        na_filter=False,
        dtype=str,
        encoding="utf-8",
    )
    chr_set = set(gdad_chr_df.iloc[:, 0].unique())
    print("read_gdad_chr_tsv: 完成。")
    return chr_set


# 读取统一目录下的gdad_chr.tsv文件，从而确定允许的染色体名称
GDAD_CHR_TSV_FILE_PATH = "./gdad_chr.tsv"
GDAD_CHR_SET = read_gdad_chr_tsv(gdad_chr_tsv_file_path=GDAD_CHR_TSV_FILE_PATH)


def formatted_df_to_tsv(formated_df: pd.DataFrame, tsv_path: str) -> str:
    """将格式化的数据写入TSV文件。
    选择TSV文件是因为有些字段中含有逗号，如果使用CSV文件会造成歧义。

    Args:
        formatted_df (pd.DataFrame): 输入的DataFrame。可以不带列名。
        tsv_path (str): 写入的TSV结果路径。包含列名。

    Returns:
        tsv_path (str): 写入的TSV结果路径。包含列名。
    """
    print(f"formatted_df_to_csv: 开始，写入路径: {tsv_path}")
    formated_df.to_csv(tsv_path, header=True, index=False, sep="\t", encoding="utf-8")
    print(f"formatted_df_to_csv: 完成，写入路径: {tsv_path}")
    return tsv_path


def g4_table_format(
    g4_bed_file_path: str, cell_line: str = "", technology="", doi: str = ""
) -> pd.DataFrame:
    """格式化g4的bed文件。用于数据表g4。

    Args:
        g4_bed_file_path (str): G4的BED文件路径。
        cell_line (str): 细胞系名称。
        technology (str): 测序技术名称。
        doi (str): DOI文献号。

    Returns:
        g4_table_df (pd.DataFrame): 输出的结果。
    """
    print("g4_table_format: 开始。")
    print(f"g4_table_format: 路径：{g4_bed_file_path}")
    print(f"g4_table_format: 细胞系：{cell_line}")
    print(f"g4_table_format: 测序技术：{technology}")
    print(f"g4_table_format: DOI：{doi}")
    g4_bed_df = pd.read_csv(
        filepath_or_buffer=g4_bed_file_path,
        header=None,
        index_col=None,
        sep="\t",
        encoding="utf-8",
        na_filter=False,
        dtype=str,
    )

    # 过滤染色体编号名称
    print("g4_table_format: 处理chr信息。")

    def row_chr_in_gdad_chr_set(df_row: pd.Series) -> bool:
        """用于判断DataFrame的一行中，第一个元素染色体是否在允许的元组中"""
        if str(df_row.iloc[0]) in GDAD_CHR_SET:
            return True
        return False

    g4_bed_df_chr_filter_series = g4_bed_df.apply(row_chr_in_gdad_chr_set, axis=1)
    g4_bed_df = g4_bed_df.loc[g4_bed_df_chr_filter_series, :]
    g4_bed_df.reset_index(drop=True, inplace=True)

    # 剔除不需要的行以后再确定行列数
    g4_bed_df_column_num = g4_bed_df.shape[1]
    g4_bed_df_row_num = g4_bed_df.shape[0]

    # 判断是否分双链位置
    if (
        g4_bed_df_column_num >= 5 and len(set(g4_bed_df.iloc[:, 4].unique())) > 1
    ):  # 包含strand列且不会全是“.”
        if_double_strands = True
    else:
        if_double_strands = False

    def get_strand_field(row_series: pd.Series) -> str:
        """得到strand字段的Series。用于apply()。除了正负号都是""。"""
        curr_row_strand_str = row_series.iloc[4]
        if curr_row_strand_str in {"+", "-"}:
            return curr_row_strand_str
        return ""

    # 确定strand字段的值
    print("g4_table_format: 处理strand信息。")
    if if_double_strands:
        g4_table_df_strand_field_series = g4_bed_df.swifter.apply(
            get_strand_field, axis=1
        )
    else:
        g4_table_df_strand_field_series = pd.Series([""] * g4_bed_df_row_num)

    # cell_line字段
    g4_table_df_cell_line_field_series = pd.Series([cell_line] * g4_bed_df_row_num)

    # technology字段
    g4_table_df_technology_field_series = pd.Series([technology] * g4_bed_df_row_num)

    # doi字段
    g4_table_df_doi_field_series = pd.Series([doi] * g4_bed_df_row_num)

    # 合并结果
    g4_table_df_list = [
        g4_bed_df.iloc[:, :3],
        g4_table_df_strand_field_series,
        g4_table_df_cell_line_field_series,
        g4_table_df_technology_field_series,
        g4_table_df_doi_field_series,
    ]
    g4_table_df = pd.concat(g4_table_df_list, axis=1, ignore_index=True)

    # 重置列名，利用全局变量
    g4_table_df.columns = G4_TABLE_FIELD_LIST

    print("g4_table_format: 完成。")
    return g4_table_df


def genesequence_table_format(gencode_gtf_file_path: str) -> pd.DataFrame:
    """使用Gencode的GTF文件获取适用于genesequence数据表的格式。

    Args:
        gencode_gtf_file_path (str): Gencode的基因组注释GTF文件。

    Returns:
        genesequence_table_df (pd.DataFrame): 结果数据。
    """

    print("genesequence_table_format: 开始。")
    print(f"genesequence_table_format: {gencode_gtf_file_path}")
    gencode_gtf_df = pd.read_csv(
        filepath_or_buffer=gencode_gtf_file_path,
        header=None,
        index_col=None,
        sep="\t",
        comment="#",
        na_filter=False,
        encoding="utf-8",
        dtype=str,
    )

    # 过滤染色体编号名称
    gencode_gtf_df = gencode_gtf_df.loc[gencode_gtf_df.iloc[:, 0] in GDAD_CHR_SET, :]

    # 选取为基因信息的行
    gencode_gtf_df = gencode_gtf_df.loc[gencode_gtf_df.iloc[:, 2] == "gene", :]

    def row_format(row_series: pd.Series) -> pd.Series:
        """根据一行的内容整理出需要的格式。
        1. 提取gene symbol，剔除版本号。
        2. 1-based坐标转换为0-based。

        Args:
            gencode_gtf_df_row (pd.Series): Gencode的GTF文件读取出的一行的数据。

        Returns:
            formatted_row_series (pd.Series): 格式化的行Series。
        """
        # 处理gene symbol
        row_info = row_series.iloc[8]
        gene_name_prefix = 'gene_name "'  # 基因名称的前缀
        gene_name_prefix_index = row_info.find(gene_name_prefix)
        gene_name_start_index = gene_name_prefix_index + len(gene_name_prefix)
        gene_name_end_index = row_info.find('"', gene_name_start_index)  # 找到引号的位置
        row_gene_name = row_info[gene_name_start_index:gene_name_end_index]
        row_gene_name = row_gene_name.split(".")[0]  # 去除版本号
        formatted_row_series = pd.concat(
            [row_series.iloc[[0, 3, 4]], pd.Series(row_gene_name)], ignore_index=True
        )  # Series连接仍然是Series。Series.iloc[list[int]]可能报错，不管它，pandas认为没错。

        # 1-based坐标转换0-based
        formatted_row_series.iloc[1] = int(formatted_row_series[1]) - 1
        formatted_row_series.iloc[1] = str(formatted_row_series.iloc[1])

        return formatted_row_series

    # 格式化每一行
    genesquence_table_df = gencode_gtf_df.swifter.apply(row_format, axis=1)
    # 命名每一列
    genesquence_table_df.columns = GENESEQUENCE_TABLE_FIELD_LIST

    print("genesequence_table_format: 完成。")
    return genesquence_table_df


def gda_table_format(disgenet_gda_tsv_file_path: str) -> pd.DataFrame:
    """格式化从DisGeNET的爬取的GDA数据，用于gda数据表。

    Args:
        disgenet_gda_tsv_file_path (str): DisGeNET GDA数据路径。TSV格式。

    Returns:
        gda_table_df (pd.DataFrame): 用于gda数据表的DataFrame。
    """
    print("gda_table_format: 开始。")
    print(f"gda_table_format: {disgenet_gda_tsv_file_path}")
    disgenet_gda_df = pd.read_csv(
        filepath_or_buffer=disgenet_gda_tsv_file_path,
        header=0,
        index_col=None,
        sep="\t",
        comment="#",
        na_filter=False,
        encoding="utf-8",
        dtype=str,
    )

    def row_format(row_series: pd.Series) -> pd.Series:
        """格式化每一行的格式
        1. 剔除最后一列的source的结果。
        2. disease_class_name中";"分隔开，单独一项中含有","，";"前后会有空格，需要剔除。

        Args:
            row_series (pd.Series): 读取得到的DisGeNET GDA数据的每一行的结果。

        Returns:
            formatted_row_series (pd.Seires): 格式化以后的结果。
        """
        # 剔除最后一列的source信息
        formatted_row_series = row_series.iloc[:-1]
        # 读取原始的disease_class_name
        original_disease_class_name = row_series["disease_class_name"]
        # 获取原始的disease_class_name列表
        original_disease_class_name_list = original_disease_class_name.split(";")
        # 剔除每一项之间的多余空格
        formatted_disease_class_name_list = map(
            lambda x: x.strip(), original_disease_class_name_list
        )
        # 转换为列表
        formatted_disease_class_name_list = list(formatted_disease_class_name_list)
        # 列表合并为字符串
        formatted_disease_class_name = ";".join(formatted_disease_class_name_list)
        formatted_row_series["disease_class_name"] = formatted_disease_class_name
        return formatted_row_series

    gda_table_df = disgenet_gda_df.swifter.apply(row_format, axis=1)
    gda_table_df.columns = GDA_TABLE_FIELD_LIST

    print("gda_table_format: 完成。")
    return gda_table_df


if __name__ == "__main__":
    # 结果写入的路径
    ALL_TABLE_FILE_DIR = (
        "/mnt/disk2/liujh/workspaces/20230221_database/analysis_results/tables"
    )
    G4_TABLE_PATH = os.path.join(ALL_TABLE_FILE_DIR, "g4_table.tsv")
    GENESEQUENCE_TABLE_PATH = os.path.join(ALL_TABLE_FILE_DIR, "genesequence_table.tsv")
    GDA_TABLE_PATH = os.path.join(ALL_TABLE_FILE_DIR, "gda_table.tsv")

    # 格式化g4数据表
    # K-562,G4 ChIP-seq数据
    K562_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/data/G4/GSE145090/GSE145090_20180108_K562_async_rep1-3.mult.5of8.bed"
    k562_g4_table_df = g4_table_format(
        g4_bed_file_path=K562_G4_BED_FILE_PATH,
        cell_line="K-562",
        technology="G4 ChIP-seq",
        doi="10.1186/s13059-021-02324-z",
    )
    # Hep G2,G4 ChIP-seq数据
    HEPG2_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/data/G4/GSE145090/GSE145090_HepG2_async_rep1-3.mult.6of9.bed"
    hepg2_g4_table_df = g4_table_format(
        g4_bed_file_path=HEPG2_G4_BED_FILE_PATH,
        cell_line="Hep G2",
        technology="G4 ChIP-seq",
        doi="10.1186/s13059-021-02324-z",
    )

    # MCF7,CUT&Tag,10.1038/s41598-021-02943-3
    MCF7_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE181373/GSE181373_MCF7_50k_bg4_1000.bio2.bed"
    mcf7_g4_table_df = g4_table_format(
        g4_bed_file_path=MCF7_G4_BED_FILE_PATH,
        cell_line="MCF7",
        technology="CUT&Tag",
        doi="10.1038/s41598-021-02943-3",
    )

    # U-2 OS,CUT&Tag,10.1038/s41598-021-02943-3
    U2OS_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE181373/GSE181373_U2OS_100k_bg4_bulk_1000.bio.bed"
    u2os_g4_table_df = g4_table_format(
        g4_bed_file_path=U2OS_G4_BED_FILE_PATH,
        cell_line="U-2 OS",
        technology="CUT&Tag",
        doi="10.1038/s41598-021-02943-3",
    )

    # A549,G4P ChIP-seq,10.1093/nar/gkaa841
    A549_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE133379/GSE133379_A549-G4P-hg19-rep1.narrowPeak"
    a549_g4_bed_df = g4_table_format(
        g4_bed_file_path=A549_G4_BED_FILE_PATH,
        cell_line="A549",
        technology="G4P ChIP-seq",
        doi="10.1093/nar/gkaa841",
    )

    # NCI-H1975,G4P ChIP-seq,10.1093/nar/gkaa841
    NCI_H1975_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE133379/GSE133379_H1975-G4P-hg19-rep1.narrowPeak"
    nci_h1975_g4_bed_df = g4_table_format(
        g4_bed_file_path=NCI_H1975_G4_BED_FILE_PATH,
        cell_line="NCI-H1975",
        technology="G4P ChIP-seq",
        doi="10.1093/nar/gkaa841",
    )

    # HeLa-S3,G4P ChIP-seq,10.1093/nar/gkaa841
    HELA_S3_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE133379/GSE133379_HeLa-S3-G4P-hg19-rep1.narrowPeak"
    hela_s3_g4_bed_df = g4_table_format(
        g4_bed_file_path=HELA_S3_G4_BED_FILE_PATH,
        cell_line="HeLa-S3",
        technology="G4P ChIP-seq",
        doi="10.1093/nar/gkaa841",
    )

    # 293T,G4P ChIP-seq,10.1093/nar/gkaa841
    PREFIX_293T_G4_BED_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/data/G4_raw_bed/GSE133379/GSE133379_293T-G4P-hg19-rep1.narrowPeak"
    prefix_293t_g4_bed_df = g4_table_format(
        g4_bed_file_path=PREFIX_293T_G4_BED_FILE_PATH,
        cell_line="293T",
        technology="G4P ChIP-seq",
        doi="10.1093/nar/gkaa841",
    )

    # 合并所有的G4格式化结果
    g4_table_df = pd.concat(
        [
            k562_g4_table_df,
            hepg2_g4_table_df,
            mcf7_g4_table_df,
            u2os_g4_table_df,
            a549_g4_bed_df,
            nci_h1975_g4_bed_df,
            hela_s3_g4_bed_df,
            prefix_293t_g4_bed_df,
        ],
        axis=0,
    )
    formatted_df_to_tsv(formated_df=g4_table_df, tsv_path=G4_TABLE_PATH)
    del g4_table_df

    # 格式化genesequence数据表
    # 输入GTF格式的基因组文件
    # GENCODE_GTF_FILE_PATH = (
    #     "/mnt/disk2/liujh/workspaces/data/GENCODE/gencode.v19.annotation.gtf"
    # )
    # genesequence_table_df = genesequence_table_format(
    #     gencode_gtf_file_path=GENCODE_GTF_FILE_PATH
    # )
    # formatted_df_to_tsv(
    #     formated_df=genesequence_table_df, tsv_path=GENESEQUENCE_TABLE_PATH
    # )
    # del genesequence_table_df

    # 格式化gda数据表
    # 输入从DisGeNET得到的GDA数据
    # DISGENET_GDA_TSV_FILE_PATH = "/mnt/disk2/liujh/workspaces/20230221_database/analysis_results/disgenet_results/disgenet_gda_curated_gencode.tsv"
    # gda_table_df = gda_table_format(
    #     disgenet_gda_tsv_file_path=DISGENET_GDA_TSV_FILE_PATH
    # )
    # formatted_df_to_tsv(formated_df=gda_table_df, tsv_path=GDA_TABLE_PATH)
    # del gda_table_df
