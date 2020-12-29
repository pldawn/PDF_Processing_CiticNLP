# coding = utf-8
import re


# 该类用来确定文本块标题的文本格式，用来构建文本树，'A'，'B'...为文本标题的大纲级别
def get_index_token(text):
    pattern_a = re.compile('第[一二三四五六七八九十]{1,2}部分')
    pattern_b = re.compile('内容摘要')
    result = re.match(pattern_a, text) or re.match(pattern_b, text)
    if result:
        return 'A'

    pattern = re.compile('([一二三四五六七八九十]{1,2})([.、])')
    result = re.match(pattern, text)
    if result:
        return 'B'

    pattern = re.compile('[（(][一二三四五六七八九十0-9]{1,2}[)）]')
    result = re.match(pattern, text)
    if result:
        return 'C'

    pattern = re.compile(r'[0-9]\.[^ 0-9]')
    result = re.match(pattern, text)
    if result:
        return 'D'

    return None


# 该类用来决定是否保留该种类的文本内容，该部分中可以被正则匹配的PDF内容均不会被写入文本树
class ReModule:
    def __init__(self, string):
        self.string = string

    def table_title_search(self):
        if re.search(r'表 +\d', self.string) is not None:
            return True

    def figure_title_search(self):
        if re.search(r'图 +\d', self.string) is not None:
            return True

    def annotation_search(self):
        if re.search(r'数据来源', self.string) is not None:
            return True

    def chapters_search(self):
        if re.search(r'第.部分', self.string) is not None:
            return True

    def lower_title_search(self):
        if re.match(r'[一二三四五六七八九十]、', self.string) is not None:
            return True

    def unit_search(self):
        if re.search(r'单位：', self.string) is not None:
            return True

    def image_search(self):
        if re.search(r'<image:', self.string) is not None:
            return True

    def roman_numerals(self):
        if re.search(r'[IVX]', self.string) is not None:
            return True

    def abstract_search(self):
        if re.search(r'内容摘要', self.string) is not None:
            return True

    def catalogue_search(self):
        if re.search(r'目 +录', self.string) is not None:
            return True

    def subtitle_search(self):
        if re.match(r'（[一二三四五六七八九十]）', self.string) is not None:
            return True

    def mini_title_search(self):
        if re.match(r'[0-9]\.[^ 0-9]', self.string):
            return True
