# coding=utf-8
import re
from collections import OrderedDict
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBoxHorizontal
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfparser import PDFParser


class PagesSearch:
    # Search_Token is a list for words you want to get page index
    # TXT_Path is a txt file copying from pdf
    # PDF_Path is your pdf file's path
    def __init__(self):
        # input data
        self.pdf_path = None
        # parse result
        self.result = []
        self.pages_dict = OrderedDict()
        self.title_max_length = 30
        self.pdf_name = None
        self.most_x0 = 0
        self.most_height = 0

    # this function can change pdf file to a list by line
    # each element of this list is a line of pdf
    def parse_pdf_to_txt(self, pdf_path):
        with open(pdf_path, 'rb') as fp:
            self.pdf_path = pdf_path
            parser = PDFParser(fp)
            document = PDFDocument(parser=parser)
            parser.set_document(document)
            rsrcmgr = PDFResourceManager()
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(document):
                interpreter.process_page(page)
                layout = device.get_result()
                # output form: <LTPage(1) 0.000,0.000,595.320,841.920 rotate=0>
                output = str(layout)
                # layout信息与文本分行
                output += '\n'
                for page_line in layout:

                    if isinstance(page_line, LTTextBoxHorizontal):

                        # 分页文本
                        text = page_line.get_text()
                        output += text
                        content = page_line.get_text().strip()
                        content = content.replace('\n', '|')

                        # 过滤掉只有换行符的内容
                        if content == '':
                            continue
                        self.result.append((page_line.x0, page_line.height, content))
                with open(pdf_path[:-4] + '_result.txt', 'a', encoding='utf-8') as f:
                    f.write(output)
        return self.result

    # this function can search page index by self.search_token = Search_Token
    # self.search_token = Search_Token is a list object
    # ***
    def get_word_page(self):
        with open(self.pdf_path[:-4] + '_result.txt', encoding='utf-8') as file_read:
            text_list = file_read.read().split('<LTPage')
            n = len(text_list)
            page_list = []
            for i in range(1, n):
                if re.search(r'\.{5,}[\s\S]\d+', text_list[i]) is not None:
                    page_list.append(i)
            return page_list

    # sentence is line in a report
    # return -1 means sentence is not in this report
    def get_page_of_sentence(self, sentence):
        result = -1
        with open(self.pdf_path[:-4] + '_result.txt', 'r', encoding='utf-8') as f:
            # 以'<LTPage'为标志符分割txt文档为一个list
            text_list = f.read().split('<LTPage')
            # total pages - 1
            n = len(text_list)
            for i in range(1, n):
                if sentence in text_list[i]:
                    result = i
                    break
        return result

    # this function can change pdf to OrderDict()[page_index] = page content
    def divide_to_pages(self):
        pool = []
        # 当前页数
        page_present = 1
        # 上一次循环检索的页数
        last_page = 1
        # 报告总行数
        total_lines = len(self.result)
        # line is equal to line_page + 1
        for line in range(total_lines):
            # (x.x0, x.height, content)
            line_tuple = self.result[line]
            sentence = line_tuple[-1]
            line_page = self.get_page_of_sentence(sentence=sentence)
            # improve search page results
            # pdf搜索定页解析存在极少量的内容定页出现异常，目前采用如下方法解决问题
            # 解析会将异常内容的页码定位为上一轮搜索定页的结果
            if line_page == last_page or line_page == last_page + 1:
                line_page = line_page
            else:
                line_page = last_page
            last_page = line_page
            # 添加字典元素
            if line_page == page_present:
                pool.append(line_tuple)
            else:
                page = line_page - 1
                self.pages_dict[page] = pool
                page_present = line_page
                pool = [line_tuple]
            # 将末页内容添加入OrderDict()
            self.pages_dict[line_page] = pool
        return self.pages_dict

    # 返回pages_dict中出现频率最高的文本高度
    @classmethod
    def __get_most_height(cls, pages_dict):
        contents = []
        for value in pages_dict.values():
            contents += value
        # item is x.height in (x.x0, x.height, content)
        # heights is height of each line.
        # form of heights is [38.69999999999993, 23.607000000000028, 19.349999999999994...]
        heights = [item[1] for item in contents]
        freq_dict = {}

        for height in heights:
            # dict.setdefault(key, default=None)
            # key -- 查找的键值。
            # default -- 键不存在时，设置的默认键值。
            # 如果字典中包含有给定键，则返回该键对应的值，否则返回为该键设置的值。
            # 统计heights中元素出现的次数，记为字典值
            freq_dict[height] = freq_dict.setdefault(height, 0) + 1
        # k is height, v is frequency
        heights_pairs = [(k, v) for k, v in freq_dict.items()]
        # sort by frequency
        heights_pairs.sort(key=lambda x: x[1])
        # most height is the most frequency height
        most_height = heights_pairs[-1][0]
        print(most_height)
        return most_height

    # 返回pages_dict中出现频率最高的文本缩进，原理同上
    # 用来指定一个类的方法为类方法，没有此参数指定的类的方法为实例方法
    @classmethod
    # 第一个参数是cls， 表示调用当前的类名
    def __get_most_x0(cls, pages_dict):
        contents = []
        for value in pages_dict.values():
            contents += value
        x0s = [item[0] for item in contents]
        freq_dict = {}
        for x0 in x0s:
            freq_dict[x0] = freq_dict.setdefault(x0, 0) + 1
        x0s = [(k, v) for k, v in freq_dict.items()]
        x0s.sort(key=lambda x: x[1])
        most_x0 = x0s[-1][0]
        return most_x0
