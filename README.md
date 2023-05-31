# README

本目录为疾病相关G-四链体数据库G4-Disease Association Database (GDAD)的目录，本文档说明了GDAD的开发环境以及设计框架等信息。

![GDAD_logo_blue.png](/assets/img/GDAD%E4%B8%BB%E9%A1%B5_%E6%A1%8C%E9%9D%A2%E7%89%88.jpeg)

---
## GDAD介绍

GDAD的核心目的是构建G-四链体与疾病的相关性。G-四链体的数据来自于文献收集，疾病相关数据来自于DisGeNET的Gene-Disease Association（GDA）数据，基因信息来自于[Gencode](https://www.gencodegenes.org/human/release_19.html)数据库。除了可以根据G-四链体、基因、GDA数据本身的属性进行查询，还能彼此查询。
## 软件开发环境

|名称|版本|链接|
|:---:|:---:|:---:|
|[Python](https://github.com/LawrenceLiu023/GDAD#Python)|3.11.2|<https://www.python.org/downloads/release/python-3112/>|
|[Django](https://github.com/LawrenceLiu023/GDAD#Django)|4.1.7|<https://docs.djangoproject.com/zh-hans/4.1/intro/install/>|
|[MySQL](https://github.com/LawrenceLiu023/GDAD#MySQL)|8.0.32|<https://dev.mysql.com/downloads/installer/>|
|[Bootstrap](https://github.com/LawrenceLiu023/GDAD#Bootstrap)|4.6.2|<https://github.com/twbs/bootstrap/releases/tag/v4.6.2>|

### Python {#Python}

版本：3.11.2

原生的MySQL数据库API驱动程序mysqlclient，
安装方法：

```
pip install mysqlclient
```

使用的python包：

- `pylint-django`：让vscode的代码检查能支持django的语法而不会报错。相关教程可以搜索到。
- `django-bootstrap4`：无缝融合django和bootstrap4，非必要。可以选择手动安装Bootstrap样式文件。链接：<https://pypi.org/project/django-bootstrap4/>
- `markdown`：`views.py`中的视图函数利用此包，直接从`/mysite/gdad/template`目录读取markdown文件的内容，并渲染为适合html的文本内容，从而在网页上显示渲染完成的markdown文档。所有需要的markdown文档都在此目录下，与html模板一同存放，都属于前端设计内容。

### Django {#Django}

版本：4.1.7

建议使用 4.1 大版本，为版本较新的稳定版，同时中文文档比较全面。一般来说，Django对于一个Python版本的支持会持续到其第一个发布的Django LTS安全支持停止，而Django LTS版本安全支持停止是跟随对应版本的Python安全支持结束的。例如，Python 3.3 安全支持在 2017 年 9 月结束，然后 Django 1.8 LTS 安全支持在 2018 年 4 月结束。因此 Django 1.8 是支持 Python 3.3 的最后一版。Python3.11的安全更新支持预计会持续到2027年10月。

具体的Django和Python兼容列表可以参考官方文档：<https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>

4.1版本的官方中文文档：<https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial01/>

在`mysite`目录下的`__init.py__`添加如下命令，以使用pymysql操作数据库。

```python
import pymysql
pymysql.install_as_MySQLdb()
```

#### Django文档笔记：[编写你的第一个Django应用，第1部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial01/)

本章节介绍了如何创建一个基本的Django应用。

Django项目中`settings.py`中的一些设置，这里以MySQL的相关配置为例：

```python
# settings.py
# 数据库设置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "xxx",  # 数据库名称
        "USER":"xxx",  # 用户名
        "PASSWORD":"xxx",  # 密码
        "HOST":"localhost",
        "PORT":"3306",
        "CHARSET":"utf8mb3",
        "COLLATION":"utf8mb3_general_ci",
    }
}

# 安全警告！在生产环境中永远不要打开DEBUG
DEBUG = True

# 设置语言
LANGUAGE_CODE = "zh-Hans"

# 时区设置
TIME_ZONE = 'Asia/Shanghai'
```

#### Django文档笔记：[编写你的第一个Django应用，第2部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial02/)

本章节介绍了如何链接数据库、创建模型、交互式API、管理界面。

创建了管理员用户。使用代码是`python manage.py createsuperuser`

改变数据库模型只需要三步：

1. 编辑`models.py`文件，改变模型。
2. 运行`python manage.py makemigrations`为模型的改变生成迁移文件。
3. 运行`python manage.py migrate`来应用数据库迁移。

在模型的代码`polls/models.py`中添加这样的代码，可以给模型增加`__str__()`方法。可以在显示某条数据时用返回值表示这条数据。
给模型增加`__str__`方法是重要的，不仅仅能给命令行使用带来方便，Django自动生成的Admin里面也是用这个方法来表示对象。

```python
fro django.db import models

class Question(models.Model):
    # ...
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    # ...
    def __str__(self):
        return self.Choice_text
```

Django API提供了对数据库的操作接口`py manage.py shell`，可以在命令行模式中直接操作数据库。

#### Django文档笔记：[编写你的第一个Django应用，第3部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial03/)

本章节介绍了编写视图、模板系统、URL系统。

Django使用了`URLconfs`来配置，将URL和视图关联起来，`URLconfs`将URL模式映射到视图。

#### Django文档笔记：[编写你的第一个Django应用，第4部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial04/)

本章节介绍了表单、通用视图，讲解了如何优化视图。

在编写一个Django应用时，应该先评估一下通用视图是否可以解决问题，应该在一开始使用它，而是不是进行到一半的时候重构代码。通用视图更好，可以删除许多代码，仅需以下几步：

1. 转换URLconf。
2. 删除一些旧的、不再需要的视图。
3. 基于Django的通用视图引入新的视图。

每个通用视图需要知道它将作用于哪个模型，这由model属性提供。

`DetailView`期望从URL中捕获名为`pk`的主键值，所以我们为通用视图把`question_id`改为`pk`。

默认情况下，通用视图`DetailView`使用一个叫做`<app name>/<model name>_detail.html`的模板。在我们的例子中，它将使用`polls/question_detail.html`模板。`template_name`属性是用来告诉Django使用一个指定模板的名字，而不是自动生成的默认名字。我们也为`results`列表模板指定了`template_name`——这确保`results`视图和`detail`视图在渲染时具有不同的外观，即使他们在后台都是同一个`DetailView`。

类似地，`ListView`使用一个叫做`<app name>/<model name>_list.html`的默认模板；我们使用`template_name`来告诉`ListView`使用我们创建的已经存在的`polls/index.html`模板。

在之前的教程中，提供模板文件时都带有一个包含`question`和`latest_question_list`变量的context。对于`DetailView`，`question`变量会自动提供——因为我们使用Django的模型`Question`,Django能够为`context`变量决定一个合适的名字。然而对于`ListView`，自动生成的`context`变量是`question_list`。覆盖了这鞥行为，我们提供`context_object_name`属性，表示我们想使用`latest_question_list`。作为一种替换方案，你可以改变你的模板来匹配新的 context 变量 —— 这是一种更便捷的方法，告诉 Django 使用你想使用的变量名。

#### Django文档笔记：[编写你的第一个Django应用，第5部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial05/)

本章主要讲解了自动化测试。

自动化测试是由某个系统自动完成的。当创建好一系列测试后，每次修改应用代码后，就可以自动检查出修改后的代码是否还像曾经预期的那样正常工作。不需要花费大量时间来进行手动测试。

自动化测试的运行过程：

1. `python manage.py test polls`将会寻找`polls`应用里的测试代码。
2. 它找到了`django.test.TestCase`的一个子类。
3. 它创建一个特殊的数据库供测试使用。
4. 它在类中寻找测试方法——以`test`开头的方法。
5. 在`test_was_published_recently_with_future_question`方法中，它创建了一个`pub_date`值为30天后的`Question`实例。
6. 接着使用`assertIs`方法，发现`was_published_recently()`返回了`True`，而我们期望它返回`False`。
7. 测试系统通知我们哪些测试样例失败了，和造成测试失败的代码所在的行号。

测试的建议：

1. 对于每个模型和视图都简历单独的TestClass
2. 每个测试方法只测试一个功能
3. 给每个测试方法起个能描述其功能的名字

#### Django文档笔记：[编写你的第一个Django应用，第6部分](https://docs.djangoproject.com/zh-hans/4.1/intro/tutorial06/)

本章主要讲解了静态文件，可以添加图片等功能。

`django.contrib.staticfiles`存在的意义：将各个应用的静态文件（和一些你指明的目录里的文件）统一收集起来，这样一来，在生产环境中，这些文件就会集中在一个便于分发的地方。

`{% static %}`模板标签在静态文件（例如样式表css）中是不可用的，因为它们不是由Django生成的。你应该始终使用**相对路径**在你的静态文件之间相互引用，因为这样你可以更改`STATIC_URL`（由`static`模板标签使用来生成URL），而无需修改大量的静态文件。

### MySQL {#MySQL}

版本 8.0.32

安装时选择使用传统密码校验，否则 Navicat 等GUI数据库操作软件会连接不上数据库。

默认的存储引擎是InnoDB，这个引擎是完全事务性的，并且支持外键引用。这是推荐的选择。

设置密码：
MySQL Root Password: liujiahuan

推荐字符集设置"utf8mb3"即可，"utf8mb4"完全兼容utf-8，用四个字节存储更多的字符，v主要是支持了emoji表情。
排序规则使用"utf8mb3"默认的"utf8mb3_general_ci"，ci表示大小写不敏感case insensitive。

### Bootstrap {#Bootstrap}

版本：v4.6.2

大版本选用v4，这个较新且稳定，同时文档比较完善。读音是boot strap，而不是boots trap，t会被快速带过。

## 前端设计

设计主题蓝色：RGB：(0,123,255), HEX：#007bff

前端使用的一些图片素材静态文件存放在`/mysite/gdad/static/gdad`。

### 模板继承

使用html模板的继承功能，由于最基础的模板我放在了`mysite/gdad/templates/gdad/base.html`，所以继承时候，需要说明是在哪个应用的模板目录下的，代码范例如下：

```html
{% extends 'gdad/base.html' %}
```

使用静态文件，需要在html模板的头部里面加上`{% load static %}`

## 查询功能

需要以各种方式能方便地查询数据。

查询功能与文档中的`QuerySet`条目相关，可以在官方文档中查找各种查询功能的实现。
`QuerySet`搜索得到的结果，是一个类名为`QuerySet`的对象，基本可以认为是`Set`，它可以转换为列表，可以使用`len()`方法，可以用`[数字]`索引，而且其中的每一个元素是`models.py`中定义的一个类的实例。

## 导出功能

表格可以一键点击选中全部，然后就可以复制到本地了。同时也使用了Bootstrap table的export扩展，加了一个按钮可以直接一键下载文件。

## 数据导入

数通过自动化代码可以实现把原始文件自动转换为适合导入数据库的格式，然后可以导入MySQL数据库。自动化代码存放路径为`/scripts/gdad_data_import.py`.
`/scripts/gdad_chr.tsv`中存储了GDAD允许的全部染色体名称，在`/scripts/gdad_data_import.py`的数据处理过程中会使用到该文件，从而剔除一些冗余的染色体名称。

### DisGeNET介绍

疾病与基因的关系数据库。收集了大量与人类疾病相关的变异和基因。整合了公共数据库、GWAS目录、动物模型和科学文献的数据。提供了一些原始指标，以帮助确定基因型与表型关系的优先级。可以通过web接口、Cytoscape应用程序、RDF SPARQL终端，几种编程语言的脚本和R包访问这些信息。DisGeNET提供了访问数据库的python、R等的API：[DisGeNET REST API](https://www.disgenet.org/api/)。

本数据库主要关注的数据类型是基因和疾病相关的数据Gene-Disease Associations(GDAs)。关于数据来源的描述在这个链接中：<https://www.disgenet.org/dbinfo#section44>。其中描述了一些数据来源数据库。我认为[The Clinical Genome Resource](https://www.clinicalgenome.org/)数据库的内容比较有用，可以直接提供基因gene symbol与哪个疾病相关，但是缺少一些其他的信息。好处是可以直接下载。

Python API代码示例：

```python
'''
Script example to use the DisGeNET REST API with the new authentication system
'''

#For this example we are going to use the python default http library
import requests

#Build a dict with the following format, change the value of the two keys your DisGeNET account credentials, if you don't have an account you can create one here https://www.disgenet.org/signup/
auth_params = {"email":"change@this.email","password":"changethis"}

api_host = "https://www.disgenet.org/api"

api_key = None
s = requests.Session()
try:
    r = s.post(api_host+'/auth/', data=auth_params)
    if(r.status_code == 200):
        #Lets store the api key in a new variable and use it again in new requests
        json_response = r.json()
        api_key = json_response.get("token")
        print(api_key + "This is your user API key.") #Comment this line if you don't want your API key to show up in the terminal
    else:
        print(r.status_code)
        print(r.text)
except requests.exceptions.RequestException as req_ex:
    print(req_ex)
    print("Something went wrong with the request.")

if api_key:
    #Add the api key to the requests headers of the requests Session object in order to use the restricted endpoints.
    s.headers.update({"Authorization": "Bearer %s" % api_key})
    #Lets get all the diseases associated to a gene eg. APP (EntrezID 351) and restricted by a source.
    gda_response = s.get(api_host+'/gda/gene/351', params={'source':'UNIPROT'})
    print(gda_response.json())

if s:
    s.close()
```

R API代码示例：

```r
#安装disgenet2r包
library(devtools)
install_bitbucket("ibi_group/disgenet2r")
library(disgenet2r)

#获取API密钥
library(disgenet2r)
disgenet_api_key <- get_disgenet_api_key(
                  email = "user@gmail.com",
                  password = "myspwd" )
Sys.setenv(DISGENET_API_KEY= disgenet_api_key)
#检索疾病
library(disgenet2r)
dq <- disease2gene(disease = "C0028754",
    database = "ALL",
    score = c(0.3,1))

#检索与基因列表相关的疾病
results <- gene2disease( gene = c( "KCNE1", "KCNE2", "KCNH1", "KCNH2", "KCNG1"), verbose = TRUE)

#检索与疾病列表相关的基因
results2 <- disease2gene( disease = c("C0036341", "C0002395", "C0030567","C0005586"), database = "CURATED", verbose = TRUE )

#检索与变异列表相关的疾病
results3 <- variant2disease( variant= "rs121913279", database = "CURATED")

#检索与疾病列表相关的变体
results4 <- disease2variant(disease = c("C3150943", "C1859062", "C2678485", "C4015695"), database = "CURATED", score = c(0.75, 1))

#疾病富集功能接收一系列基因，并在DisGeNET中对疾病进行富集分析。输入的基因列表应由HGNC符号或Entrez基因标识符识别。词汇表应该使用参数词汇表来指定。默认情况下，vocabulary = "HGNC"。该函数还有另一个可选参数:源数据库(默认情况下，database = CURATED)
#由多次Fisher检验得到的p值，使用benjamin - hochberg方法对错误发现率进行了校正

res_enrich <-disease_enrichment( entities ="KCNE1,KCNE2", vocabulary = "HGNC", database = "CURATED")

#更多用法参见相关链接
```
