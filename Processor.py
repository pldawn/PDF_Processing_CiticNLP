# coding = utf-8
import os

from Preprocessing.TextFilter import TextFilter
from Processing.AnalyseFunction import AnalyseFunction
from Processing.ArticleTree import ArticleTree


class Processor:
    """
    1、input_path是待解析的PDF文件的保存路径；
    2、model是可选的建立文档结构树的方法，代码中集成了两种，model等于0时，选用不限大纲目录结构的模式，
    model等于1时，选用基于《货币政策执行报告》目录结构的模式。默认使用不限制大纲目录的模式。
    3、调用示例：
    analyse_result = Processor.analyzer(input_path)
    返回 class Analyse_Function
    可以调用Analyse_Function.py中的class Analyse_Function的接口
    """

    @classmethod
    def analyzer(cls, input_path):

        article_structure = None

        try:
            text_file = TextFilter(input_path=input_path)
            text_list = text_file.plain_txt()

            article_structure_object = ArticleTree(text_list)
            article_structure = article_structure_object.tree_construction()

        except IOError:
            print("PDF 解析失败。")
        else:
            print("PDF 已经完成解析。")

        if os.path.exists(input_path[:-4] + '.txt'):
            os.remove(input_path[:-4] + '.txt')
            os.remove(input_path[:-4] + '_result.txt')
        else:
            print('error, txt file does not exist.')

        analyse_result = AnalyseFunction(article_structure)

        return analyse_result
