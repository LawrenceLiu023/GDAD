from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404
from django.template import loader
from .models import G4, GeneSequence, Gda

import os
import typing
import markdown


# 判断默认输入表单的内容，可能会是各种值，不确定
DEFAULT_FORM_INPUT_SET = {None, "", "None"}


def index(request):
    """主页视图
    """
    # 指定模板的路径
    template_path = "gdad/index.html"

    # 如用django.shortcuts.render的话，不需要下面这行来读取模板
    # template = loader.get_template(template_path)

    # 向模板传递的上下文字典，将模板内的变量映射为python对象
    all_g4_list = G4.objects.all()
    all_g4_list_len = len(all_g4_list)
    all_genesequence_list = GeneSequence.objects.all()
    all_genesequence_list_len = len(all_genesequence_list)
    all_gda_list = Gda.objects.all()
    all_gda_list_len = len(all_gda_list)
    context = {
            "all_g4_list_len": all_g4_list_len,
            "all_genesequence_list_len": all_genesequence_list_len,
            "all_gda_list_len": all_gda_list_len
            }

    # 传统的返回方法
    # return HttpResponse(template.render(context, request))
    # 快捷方式：载入模板，填充上下文，返回由它生成的HttpReponse对象
    return render(request, template_path, context)

def readme(request):
    """网站的介绍视图
    """
    template_path="gdad/readme.html"
    markdown_path= os.path.join(
        os.getcwd(), "mysite", "gdad", "templates", "gdad", "readme.md"
    )  # 没有django支持，需要给出真实相对路径
    with open(markdown_path,"r",encoding="utf-8") as markdown_file:
        markdown_text=markdown_file.read()
        markdown_html=markdown.markdown(markdown_text)
    context={"markdown_html":markdown_html}
    return render(request, template_path, context)


def g4(request):
    """g4相关功能的主页视图"""
    template_path = "gdad/g4.html"
    markdown_path = os.path.join(
        os.getcwd(), "mysite", "gdad", "templates", "gdad", "g4.md"
    )  # 没有django支持，需要给出真实相对路径
    with open(markdown_path, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()
        markdown_html = markdown.markdown(markdown_text)
    context = {"markdown_html": markdown_html}
    return render(request, template_path, context)


def g4_search(request, search_type: str):
    """搜索g4的结果视图

    Args:
        search_type (str): 从模板传递的参数，用来标注是那种搜索方式，取值有："g4","genesequence","gda"
    """
    template_path = "gdad/g4_search.html"

    # 根据查询的类别分别执行查询
    match search_type:
        case "g4":
            input_id = request.GET.get("id")
            input_chr = request.GET.get("chr")
            input_start = request.GET.get("start")
            input_end = request.GET.get("end")
            input_strand = request.GET.get("strand")
            input_cell_line = request.GET.get("cell_line")
            input_doi = request.GET.get("doi")
            g4_queryset = g4_search_by_g4(
                id=input_id,
                chr=input_chr,
                start=input_start,
                end=input_end,
                strand=input_strand,
                cell_line=input_cell_line,
                doi=input_doi,
            )
            context = {
                "search_type": search_type,  # 给出搜索相关的条件，在结果中显示
                "input_id": input_id,
                "input_chr": input_chr,
                "input_start": input_start,
                "input_end": input_end,
                "input_strand": input_strand,
                "input_cell_line": input_cell_line,
                "input_doi": input_doi,
                "g4_queryset": g4_queryset,
            }
        case "genesequence":
            input_genesequence_id = request.GET.get("genesequence_id")
            input_gene_symbol = request.GET.get("gene_symbol")
            g4_queryset = g4_search_by_genesequence(
                genesequence_id=input_genesequence_id, gene_symbol=input_gene_symbol
            )
            context = {
                "search_type": search_type,  # 给出搜索相关的条件，在结果中显示
                "input_genesequence_id": input_genesequence_id,
                "input_gene_symbol": input_gene_symbol,
                "g4_queryset": g4_queryset,
            }
        case "gda":
            input_gda_id = request.GET.get("gda_id")
            input_disease_name = request.GET.get("disease_name")
            g4_queryset = g4_search_by_gda(
                gda_id=input_gda_id, disease_name=input_disease_name
            )
            context = {
                "search_type": search_type,  # 给出搜索相关的条件，在结果中显示
                "input_gda_id": input_gda_id,
                "input_disease_name": input_disease_name,
                "g4_queryset": g4_queryset,
            }
        case _:
            raise Http404("views.g4_search: Invalid search_type.")

    return render(request, template_path, context)


def genesequence(request):
    """genesequence相关功能的主页视图"""
    template_path = "gdad/genesequence.html"
    markdown_path = os.path.join(
        os.getcwd(), "mysite", "gdad", "templates", "gdad", "genesequence.md"
    )  # 没有django支持，需要给出真实相对路径
    with open(markdown_path, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()
        markdown_html = markdown.markdown(markdown_text)
    context = {"markdown_html": markdown_html}
    return render(request, template_path, context)


def genesequence_search(request, search_type: str):
    """搜索genesequence结果视图

    Args:
        search_type (str): 从模板传递的参数，用来标注是那种搜索方式，取值有："g4","genesequence","gda"
    """
    template_path = "gdad/genesequence_search.html"

    # 根据查询的类别分别执行查询
    match search_type:
        case "genesequence":
            input_id = request.GET.get("id")
            input_chr = request.GET.get("chr")
            input_start = request.GET.get("start")
            input_end = request.GET.get("end")
            input_gene_symbol = request.GET.get("gene_symbol")
            genesequence_queryset = genesequence_search_by_genesequence(
                id=input_id,
                chr=input_chr,
                start=input_start,
                end=input_end,
                gene_symbol=input_gene_symbol,
            )
            context = {
                "search_type": search_type,
                "input_id": input_id,
                "input_chr": input_chr,
                "input_start": input_start,
                "input_end": input_end,
                "input_gene_symbol": input_gene_symbol,
                "genesequence_queryset": genesequence_queryset,
            }
        case "g4":
            input_g4_id = request.GET.get("g4_id")
            genesequence_queryset = genesequence_search_by_g4(g4_id=input_g4_id)
            context = {
                "search_type": search_type,
                "input_g4_id": input_g4_id,
                "genesequence_queryset": genesequence_queryset,
            }
        case "gda":
            input_gda_id = request.GET.get("gda_id")
            input_disease_name = request.GET.get("disease_name")
            genesequence_queryset = genesequence_search_by_gda(
                gda_id=input_gda_id, disease_name=input_disease_name
            )
            context = {
                "search_type": search_type,
                "input_gda_id": input_gda_id,
                "input_disease_name": input_disease_name,
                "genesequence_queryset": genesequence_queryset,
            }
        case _:
            raise Http404("views.genesequence_search: Invalid search_type.")
    return render(request, template_path, context)


def gda(request):
    """gda相关功能的主页视图"""
    template_path = "gdad/gda.html"
    markdown_path = os.path.join(
        os.getcwd(), "mysite", "gdad", "templates", "gdad", "gda.md"
    )  # 没有django支持，需要给出真实相对路径
    with open(markdown_path, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()
        markdown_html = markdown.markdown(markdown_text)
    context = {"markdown_html": markdown_html}
    return render(request, template_path, context)


def gda_search(request, search_type: str):
    """搜索gda结果视图

    Args:
        search_type (str): 从模板传递的参数，用来标注是那种搜索方式，取值有："gda","g4"
    """
    template_path = "gdad/gda_search.html"

    match search_type:
        case "gda":
            input_id = request.GET.get("id")
            input_disease_name = request.GET.get("disease_name")
            input_gene_symbol = request.GET.get("gene_symbol")
            gda_queryset = gda_search_by_gda(
                id=input_id,
                disease_name=input_disease_name,
                gene_symbol=input_gene_symbol,
            )
            context = {
                "search_type": search_type,
                "input_id": input_id,
                "input_disease_name": input_disease_name,
                "input_gene_symbol": input_gene_symbol,
                "gda_queryset": gda_queryset,
            }
        case "g4":
            input_g4_id = request.GET.get("g4_id")
            gda_queryset = gda_search_by_g4(g4_id=input_g4_id)
            context = {
                "search_type": search_type,
                "input_g4_id": input_g4_id,
                "gda_queryset": gda_queryset,
            }
        case "genesequence":
            input_genesequence_id = request.GET.get("genesequence_id")
            gda_queryset = gda_search_by_genesequence(
                genesequence_id=input_genesequence_id
            )
            context = {
                "search_type": search_type,
                "input_genesequence_id": input_genesequence_id,
                "gda_queryset": gda_queryset,
            }
        case _:
            raise Http404("views.gda_search: Invalid search_type.")

    return render(request, template_path, context)


# SECTION - 以下均不是视图函数，用于运算之类


def comma_sep_str_to_list(string: str) -> list[str]:
    """把用逗号隔开的字符串进行处理，变成列表。

    Args:
        string (str): 逗号隔开的字符串。

    Returns:
        out_list (list[str]): 处理后的列表，元素为字符串。会剔除每个元素首尾的空格字符。
    """
    string = string.strip()
    out_list = string.split(",")
    out_list = list(map(lambda x: x.strip(), out_list))
    return out_list


def space_sep_str_to_list(string: str) -> list[str]:
    """把用制表符符号分隔的字符串进行处理，变成列表。

    Args:
        string (str): 制表符隔开的字符串。

    Returns:
        out_list (list[str]): 处理后的列表，元素为字符串。会剔除每个元素首尾的空格字符。
    """
    string = string.strip()
    string_list = string.split(r" ")
    out_set = set(map(lambda x: x.strip(), string_list))
    out_set.discard("")
    out_list = list(out_set)
    return out_list


def g4_id_to_position(g4_id: str | int | float) -> list[str]:
    """根据g4的id得到位置的列表

    Args:
        g4_id (str|int|float): 可以转换为int即可。

    Returns:
        position_list (list[str]): 位置的列表，例如["chr1", 1, 2]
    """
    try:
        g4_id = int(g4_id)
    except Exception as exce:
        raise Http404("views.g4_id_to_position: Invalid g4_id.") from exce

    # get()方法如果找不到也会报错，不必检查异常
    g4_object = G4.objects.get(id=g4_id)
    g4_chr = g4_object.chr
    g4_start = g4_object.start
    g4_end = g4_object.end
    position_list = [g4_chr, g4_start, g4_end]
    return position_list


def g4_search_by_g4(id="", chr="", start="", end="", strand="", cell_line="", doi=""):
    """根据G4的字段查找G4

    Args:
        chr: 染色体，逗号分隔。
        start: 起始位点。
        end: 终止位点。
        strand: 正负链。
        cell_line: 细胞系，逗号分隔。
        doi: DOI,逗号分隔。

    Returns:
        out_queryset (QuerySet): 返回值为QuerySet，包含查询到的G4的对象。
    """
    if id in DEFAULT_FORM_INPUT_SET:
        out_queryset = G4.objects.all()
    else:
        id_list = comma_sep_str_to_list(id)
        out_queryset = G4.objects.filter(id__in=id_list)
    if chr not in DEFAULT_FORM_INPUT_SET:
        chr_list = comma_sep_str_to_list(chr)
        out_queryset = G4.objects.filter(chr__in=chr_list)
    if start not in DEFAULT_FORM_INPUT_SET:
        start = int(start)
        out_queryset = out_queryset.filter(start__gte=start)
    if end not in DEFAULT_FORM_INPUT_SET:
        end = int(end)
        out_queryset = out_queryset.filter(end__lte=end)
    if strand not in DEFAULT_FORM_INPUT_SET:
        strand = strand.strip()
        out_queryset = out_queryset.filter(strand=strand)
    if cell_line not in DEFAULT_FORM_INPUT_SET:
        cell_line_list = comma_sep_str_to_list(cell_line)
        out_queryset = out_queryset.filter(cell_line__in=cell_line_list)
    if doi not in DEFAULT_FORM_INPUT_SET:
        doi_list = comma_sep_str_to_list(doi)
        out_queryset = out_queryset.filter(doi__in=doi_list)
    return out_queryset


def g4_search_by_genesequence(genesequence_id="", gene_symbol=""):
    """根据基因序列信息查找G4。

    Args:
        genesequence_id: genesequence数据的id。
        gene_symbol: 基因名，用逗号隔开，可能是"",None。

    Returns:
        out_queryset (QuerySet): 查找结果。
    """
    genesequence_queryset = genesequence_search_by_genesequence(
        id=genesequence_id, gene_symbol=gene_symbol
    )
    # 找到坐标条件
    position_list = []
    for curr_genesequence in genesequence_queryset:
        curr_genesequence_position = [
            curr_genesequence.chr,
            curr_genesequence.start,
            curr_genesequence.end,
        ]
        position_list.append(curr_genesequence_position)

    # 根据基因组位置查找g4
    g4_queryset_list = []
    for curr_position in position_list:
        # 找到与基因有交叠的g4
        curr_position_g4_queryset = G4.objects.filter(
            chr=curr_position[0],
            start__lt=curr_position[2],
            end__gt=curr_position[1],
        )
        g4_queryset_list.append(curr_position_g4_queryset)
    # 将结果取并集
    out_queryset = G4.objects.none()
    for curr_g4_queryset in g4_queryset_list:
        out_queryset = out_queryset | curr_g4_queryset
    return out_queryset


def g4_search_by_gda(gda_id="", disease_name=""):
    """根据疾病名称查找G4。

    Args:
        gda_id: GDA数据的ID。
        disease_name: 疾病名称，空格分隔，可能是"", None。

    Returns:
        out_queryset (QuerySet): 查找结果。
    """
    gda_queryset = gda_search_by_gda(id=gda_id, disease_name=disease_name)

    # 找到所有涉及的基因名
    gene_symbol_set = set()
    for curr_gda in gda_queryset:
        gene_symbol_set.add(curr_gda.gene_symbol)

    # 用gene_symbol组成字符串直接传给g4_search_by_genesequence
    gene_symbol_str = ",".join(gene_symbol_set)
    out_queryset = g4_search_by_genesequence(gene_symbol=gene_symbol_str)
    return out_queryset


def genesequence_search_by_genesequence(
    id="", chr="", start="", end="", gene_symbol=""
):
    """根据genesequence的字段查找genesequence

    Args:
        id: id，逗号分隔。
        chr: 染色体，逗号分隔。
        start: 起始位点。
        end: 终止位点。
        gene_symbol: 基因名，逗号分隔。

    Returns:
        out_queryset (QuerySet): 返回值为QuerySet，包含查询到的GeneSequence的对象。
    """
    if id in DEFAULT_FORM_INPUT_SET:
        out_queryset = GeneSequence.objects.all()
    else:
        id_list = comma_sep_str_to_list(id)
        out_queryset = GeneSequence.objects.filter(id__in=id_list)
    if chr not in DEFAULT_FORM_INPUT_SET:
        chr_list = comma_sep_str_to_list(chr)
        out_queryset = out_queryset.filter(chr__in=chr_list)
    if start not in DEFAULT_FORM_INPUT_SET:
        out_queryset = out_queryset.filter(start__gte=start)
    if end not in DEFAULT_FORM_INPUT_SET:
        end = int(end)
        out_queryset = out_queryset.filter(end__lte=end)
    if gene_symbol not in DEFAULT_FORM_INPUT_SET:
        gene_symbol_list = comma_sep_str_to_list(gene_symbol)
        out_queryset = out_queryset.filter(gene_symbol__in=gene_symbol_list)
    return out_queryset


def genesequence_search_by_g4(g4_id=""):
    """根据g4的信息查找genesequence

    Args:
        g4_id: g4的id，逗号分隔。

    Returns:
        out_queryset (QuerySet): 返回值为QuerySet，包含查询到的GeneSequence的对象。
    """
    if g4_id in DEFAULT_FORM_INPUT_SET:
        out_queryset = GeneSequence.objects.all()
        return out_queryset

    # 找到所有的G4位置列表
    g4_id_list = comma_sep_str_to_list(g4_id)
    position_list = list(map(g4_id_to_position, g4_id_list))

    # 对每个坐标范围进行查找
    genesequence_queryset_list = []
    for curr_position in position_list:
        curr_position_genesequence_queryset = GeneSequence.objects.filter(
            chr=curr_position[0],
            start__lt=curr_position[2],
            end__gt=curr_position[1],
        )
        genesequence_queryset_list.append(curr_position_genesequence_queryset)
    # 将结果取并集
    out_queryset = GeneSequence.objects.none()
    for curr_genesequence_queryset in genesequence_queryset_list:
        out_queryset = out_queryset | curr_genesequence_queryset
    return out_queryset


def genesequence_search_by_gda(gda_id="", disease_name=""):
    """根据疾病名称查找genesequence

    Args:
        gda_id: GDA数据的id。
        disease_name: 疾病名称，空格分隔，可能是"", None。

    Returns:
        out_queryset (QuerySet): 查找结果。
    """
    gda_queryset = gda_search_by_gda(id=gda_id, disease_name=disease_name)

    # 找到所有涉及的基因名
    gene_symbol_set = set()
    for curr_gda in gda_queryset:
        gene_symbol_set.add(curr_gda.gene_symbol)

    # 用gene_symbol组成字符串直接传给genesequence_search_by_genesequence
    gene_symbol_str = ",".join(gene_symbol_set)
    out_queryset = genesequence_search_by_genesequence(gene_symbol=gene_symbol_str)
    return out_queryset


def gda_search_by_gda(id="", disease_name="", gene_symbol=""):
    """根据gda自带的字段搜索gda

    Args:
        id: id，用逗号分隔。
        disease_name: 疾病名称，用空格分隔。
        gene_symbol: 基因名称，用逗号分隔。

    Returns:
        out_queryset (QuerySet): 查找结果。
    """
    if id in DEFAULT_FORM_INPUT_SET:
        out_queryset = Gda.objects.all()
    else:
        id_list = comma_sep_str_to_list(id)
        out_queryset = Gda.objects.filter(id__in=id_list)
    if disease_name not in DEFAULT_FORM_INPUT_SET:
        disease_name_list = space_sep_str_to_list(disease_name)
        for curr_disease_name in disease_name_list:
            out_queryset = out_queryset.filter(
                disease_name__iregex=rf".*{curr_disease_name}.*"
            )
    if gene_symbol not in DEFAULT_FORM_INPUT_SET:
        gene_symbol_list = comma_sep_str_to_list(gene_symbol)
        out_queryset = out_queryset.filter(gene_symbol__in=gene_symbol_list)
    return out_queryset


def gda_search_by_g4(g4_id=""):
    """根据g4的相关信息查找gda

    Args:
        id: id，用逗号分隔

    Returns:
        out_queryset (QuerySet): 查找结果。
    """
    if id in DEFAULT_FORM_INPUT_SET:
        out_queryset = Gda.objects.all()
        return out_queryset
    # 如果有输入ID，根据ID找到所有对应的g4坐标
    g4_id_list = comma_sep_str_to_list(g4_id)
    g4_position_list = list(map(g4_id_to_position, g4_id_list))

    # 根据g4查找结果找到对应的genesequence
    genesequence_queryset_list = []
    for curr_g4_position in g4_position_list:
        curr_g4_position_genesequence_queryset = GeneSequence.objects.filter(
            chr=curr_g4_position[0],
            start__lt=curr_g4_position[2],
            end__gt=curr_g4_position[1],
        )
        genesequence_queryset_list.append(curr_g4_position_genesequence_queryset)
    # 将结果取并集
    genesequence_queryset = GeneSequence.objects.none()
    for curr_genesequence_queryset in genesequence_queryset_list:
        genesequence_queryset = genesequence_queryset | curr_genesequence_queryset
    # 找到所有涉及的gene_symbol，在gda中查找
    gene_symbol_set = set()
    for curr_genesequence in genesequence_queryset:
        gene_symbol_set.add(curr_genesequence.gene_symbol)
    out_queryset = Gda.objects.filter(gene_symbol__in=gene_symbol_set)
    return out_queryset


def gda_search_by_genesequence(genesequence_id=""):
    """根据gene信息查找gda。

    Args:
        genesequence_id: genesequence数据的id

    Returns:
        out_queryset (QuerySet): 查找的结果。
    """
    if genesequence_id in DEFAULT_FORM_INPUT_SET:
        out_queryset = Gda.objects.all()
        return out_queryset
    # 如果有有效输入的话
    genesequence_id_list = comma_sep_str_to_list(genesequence_id)
    genesequence_queryset = GeneSequence.objects.filter(id__in=genesequence_id_list)
    gene_symbol_set = set()
    for curr_genesequence in genesequence_queryset:
        gene_symbol_set.add(curr_genesequence.gene_symbol)
    out_queryset = Gda.objects.filter(gene_symbol__in=gene_symbol_set)
    return out_queryset


#!SECTION 非视图函数内容结束
