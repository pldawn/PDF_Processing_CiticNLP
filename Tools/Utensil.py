# coding=utf-8
import pdfplumber as plumber
from collections import OrderedDict


class Utensil:
    def __init__(self):
        self.tables_dict = OrderedDict()

    # input path
    # 能够识别表格区域、专栏区域
    def table_coordinate_detect(self, input_path):
        with plumber.open(input_path) as pdf:
            for page_number in range(len(pdf.pages)):
                result = []
                page = pdf.pages[page_number]
                vertical_edges = page.debug_tablefinder(table_settings={}).edges
                for i in range(len(vertical_edges)):
                    pairs = []
                    # 字典键 orientation 表示这条直线的朝向，如果其值为v，代表竖向，如果其值为h，代表横向
                    if vertical_edges[i]['orientation'] == 'v':
                        # a A4 page's y0 is usually smaller than 0.05 and y1 bigger than 841
                        if vertical_edges[i]['y0'] < 0.05 and vertical_edges[i]['y1'] > 841:
                            continue
                        y0 = vertical_edges[i]['y0']
                        y1 = vertical_edges[i]['y1']
                        # print(vertical_edges[i])
                        pairs.append(y0)
                        pairs.append(y1)
                # 如果该页面存在目标对象，那么y0和y1非空
                    if pairs:
                        result.append(pairs)
                self.tables_dict[page_number] = result
        return self.tables_dict
