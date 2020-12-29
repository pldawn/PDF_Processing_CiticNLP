# PDF解析

中信银行信息技术管理部金融产品IT创新实验室的PDF解析库，提供了一种基于pdfminer.six、pdfplumber和PyMuPDF的pdf解析方法。目前，该库已经封装了常见的PDF解析方法：

0、能够读取PDF文件、跳过其中的图、表以及专栏（专栏此处可以理解为具有特殊颜色的文本区域）并将其转化为TXT文本；

1、能够将PDF文件转化成文本树数据结构，该数据结构是一棵自定义的树数据结构，每个节点包含标题、段落、次级节点以及其母节点信息；

2、能够提取出文章所有的标题，返回由标题构成的列表；

3、能够提取出文章所有的文本块，返回由文本块（文本块是由标题、段落构成的文本列表）构成的二维列表；

4、能够按照给定路径路径查找文本块或者句子；

5、能够按照给定路径查找其上下文；

上述方法的调用方法请参考文档Usage中的内容。目前PDF解析模块能够很好的对单栏PDF文本进行解析，较为复杂的PDF文档解析，如双栏四区域的PDF文件解析模块正在开展研发工作，预计于2020年3月左右开发完毕。

## Requirements

> python : 3.6 | 3.7
> pdfminer.six：20200517
> pdfplumber：0.5.24
> PyMuPDF：1.18.4

## Usage

这里给出用法示例：

首先，需要给出PDF文件的路径，例如：

```python
input_path = './Resources/2018Q3.pdf'
```

然后需要创建一个Processor()对象：

```python
agent = Processor()
```

调用``analyzer()``方法：

```python
analyse_result = agent.analyzer(input_path)
```

这样就可以调用`analyzer`对象中的方法：

> 1、获得文本块列表：
>
> ```python
> content_list = analyse_result.article_list_extract()
> ```

>2、获得标题列表：
>
>```python
>structure_list = analyse_result.article_structure_extract()
>```

>3、依据路径查找相应段落：
>
>```python
>find_sentence_result = analyse_result.find_content([['c3'], ['c1'], ['p2s2']])
>```

>4、依据段落查找目标段落：
>
>```python
>target_result_01 = analyse_result.next_paragraph(step=1, paragraph=find_result[0][0])
>target_result_02 = analyse_result.next_paragraph(step=1, path=[['c3'], ['c1'], ['p2']])
>```

## Project Introduce

PDF解析模块共分为8个主程序文件，分别是与预处理模块：``PDF_Preprocessing.py``，信息提取与页码检索模块``Page_Search.py``， 文本正则匹配模块：``Re_Module.py``， 文本过滤模块：``Text_Filter.py``，文本结构输出模块：``Output_Paragraph.py``，文本结构输出模块：``Article_Tree.py``，解析功能接口模块：``Analyse_Function.py``， 封装模块：``Processor.py``。下面逐一介绍：

### 1、预处理模块``PDF_Preprocessing.py``

该模块定义了一个类：

```python
class Pdf_Preprocessing
```

定义了方法：

```python
def table_coordinate_detect(self):
```

通过调用该方法，可以返回一个含有表格坐标信息的有序字典。

输入：PDF文件路径（string）

输出：一个有序字典，key值是表格的页码，value值是PDF文件表格竖线的首尾纵坐标的数组，是一个二维列表。

### 2、信息提取与页码检索模块``Page_Search.py``

该模块定义了一个类：

```python
class Pages_Search
```

输入：

PDF_Path：PDF文件路径（string）

TXT_Path：PDF转成TXT文本之后，该TXT文本的保存路径（string）

Search_Token：是一个检索词组成的一维列表，可以通过该类的方法搜索该词语出现的页码。

定义了如下方法：

```python
def parsePDFtoTXT(self)
```

返回PDF生成的TXT文本，该文本用于检索分页功能，保存位置为TXT_Path。

```python
def get_word_page(self)
```

返回一个二维列表，将Search_Token每一个元素出现的页码位置保存在一个列表中返回。

```python
def get_page_of_sentence(self, sentence):
```

sentence：字符串

返回sentence首次出现的位置（int），默认为-1。

```python
def divide_to_pages(self)
```

返回一个字典：key为页码，value为该页的内容

```python
def get_pdf_name(self):
```

返回pdf文件的文件名（string）

```python
def get_most_height(cls, pages_dict):
```

得到出现频率最高的行高（float）

```python
def get_most_x0(cls, pages_dict):
```

得到出现频率最高的缩进（float）

### 3、文本正则匹配模块：``Re_Module.py``

该模块定义了用于文本正则匹配，用于匹配特定的内容。定义了一个类：

```python
class Re_Module
```

输入：待匹配字符串（string）

定义了如下方法：

```python
def table_title_search(self)
```

匹配表头，如果匹配成功，返回True。

```python
def figure_title_search(self)
```

匹配图注，如果匹配成功，返回True。

```python
def annotation_search(self)
```

匹配数据来源，如果匹配成功，返回True。

```python
def chapters_search(self)
```

匹配章标题，如果匹配成功，返回True。

```python
def lower_title_search(self)
```

匹配二级标题，如果匹配成功，返回True。

```python
def subtitle_search(self)
```

匹配三级标题，如果匹配成功，返回True。

```python
def unit_search(self)
```

匹配‘单位’，如果匹配成功，返回True。

```python
def image_search(self)
```

匹配图信息，如果匹配成功，返回True。

```python
def roman_numerals(self)
```

匹配罗马数字，如果匹配成功，返回True。

```python
def home_page_search(self)
```

匹配首页，如果匹配成功，返回True。

```python
def abstract_search(self)
```

匹配摘要，如果匹配成功，返回True。

```python
def catalogue_search(self)
```

匹配目录，如果匹配成功，返回True。

### 4、文本过滤模块``Text_Filter.py``

该模块将会使用上述模块将pdf文件转成一个带有缩进信息、行高度信息的txt文本，并将其按行保存为一个list数据结构。定义了类：

```python
class Text_Filter
```

输入：pdf文件路径，（string）

输出：在该路径下保存一个带有缩进信息、行高度信息的txt文本，文件名为pdf文件名+result，返回一个相同内容的list。

定义了方法```def plain_txt(self)```用于执行该功能。

### 5、文本结构输出模块：``Output_Paragraph.py``

按照文件节点——>章节点——>一级标题——>二级标题——>段落生成文本树数据结构，调用方法：

```python
class Output_Paragraph.article_tree(self)
```

调用示例如下：

```python
article_structure_object = Output_Paragraph(text_list: class Text_Filter.plain_txt(self))
article_structure = article_structure_object.article_tree()
```

### 6、文本结构输出模块：``Article_Tree.py``

本模块定义了一棵树结构，文本树结构与``Output_Paragraph.py``完全相同，但是泛化性更好，可以用于多级标题的文本树生成，调用方法如下：

```python
class article_tree.tree_construction(self)
```

调用示例如下：

```python
article_structure_object = article_tree(text_list: class Text_Filter.plain_txt(self))
article_structure =
article_structure_object.tree_construction()
```

### 7、解析功能接口模块：``Analyse_Function.py``

提供了一些辅助功能。定义了类：

```python
class Analyse_Function
```

输入：

1、text_tree：文本树数据结构

（1）通过调用：

```python
structure_list = Analyse_Function.article_structure_extract()
```

> 可以按顺序抽取文本的所有标题，会返回一个list，列表中是文本所有的标题。

（2）通过调用：

```python
structure_list = Analyse_Function.article_list_extract()
```

> 可以按顺序抽取文章中所有的文本块（文本块包括：标题和正文段落）。

（3）通过调用：

```python
structure_list = Analyse_Function.next_paragraph()
```

> 可以用于段落查找，依据给定的文本块或者路径进行查找。
>
> 1、step是步长，基于当前文本块，默认为1， 即就是查找下一个文本块的内容
> 2、path是路径，示例写法
> 用法示例：```path = [[c1], [c2], [t], [p1s1s2, p2]]```， c1为下一级第一个部分， t为当年目录下的标题，p1为第一段，s1为第一句话。
> 3、返回值为一个只有一个元素的list。

（4）通过调用：

```python
structure_list = Analyse_Function.find_content(path = [[c1], [c2], [p1s1s2, p2]])
```

可以用于依据路径查找文本块，返回一个单一元素的列表。

### 8、封装模块：``Processor.py``

``Processor.py``对上述代码进行了封装，便于调用。该模块定义了一个类：

```python
class Processor
```

该类下定义了一个方法：

```python
def analyzer(cls, input_path, model: Optional[int] = 0):
```

>1、input_path是待解析的PDF文件的保存路径；
>2、model是可选的建立文档结构树的方法，代码中集成了两种，model等于0时，选用不限大纲目录结构的模式，model等于1时，选用基于《货币政策执行报告》目录结构的模式。默认使用不限制大纲目录的模式。
>3、调用示例：
>
>```python
>analyse_result = Processor.analyzer(input_path)
>```
>
>``analyse_result = Processor.analyzer(input_path)``返回`` class Analyse_Function``
>可以调用``Analyse_Function.py``中的``class Analyse_Function``的接口