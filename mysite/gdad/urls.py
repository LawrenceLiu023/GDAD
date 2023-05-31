from django.urls import path

from . import views

# 为URL名称添加命名空间
app_name = "gdad"

urlpatterns = [
    # 主页视图：/gdad/
    path(route="", view=views.index, name="index"),
    # 网站介绍视图：/gdad/readme/
    path(route="readme/",view=views.readme,name="readme"),
    # g4相关主页：/gdad/g4/
    path(route="g4/", view=views.g4, name="g4"),
    # g4_search:/gdad/g4/search/<str:search_type>/
    # search_type用来标识是那种查询类别，取值可以有"g4","genesequence","gda"
    path(route="g4/search/<str:search_type>/", view=views.g4_search, name="g4_search"),
    # genesequence相关主页：/gdad/genesequence/
    path(route="genesequence/", view=views.genesequence, name="genesequence"),
    # genesequence_search:/gdad/genesequence/<search_type>/
    # search_type用来标识是那种查询类别，取值可以有"g4","genesequence","gda"
    path(
        route="genesequence/<str:search_type>/",
        view=views.genesequence_search,
        name="genesequence_search",
    ),
    # gda相关主页：/gdad/gda/
    path(route="gda/", view=views.gda, name="gda"),
    # gda_search:/gdad/gda/<search_type>/
    # search_type用来标识是那种查询类别，取值可以有"g4","genesequence","gda"
    path(route="gda/<str:search_type>/", view=views.gda_search, name="gda_search"),
]
