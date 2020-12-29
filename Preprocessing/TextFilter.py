# coding=utf-8
import fitz
from Tools.Utensil import Utensil
from Preprocessing.PageSearch import PagesSearch
import conf


class TextFilter:
    # input_path is your pdf path
    # coordinate_dict is a dict from Pdf_Preprocessing(input_path=input_path).table_coordinate_detect()
    # association is a page search module from Pages_Search()
    # search_token is a method to divide article，please do not change it.
    def __init__(self, input_path):
        self.input_path = input_path
        self.text_list = []

    def plain_txt(self):
        coordinate = Utensil()
        coordinate_dict = coordinate.table_coordinate_detect(input_path=self.input_path)

        association = PagesSearch()
        association.parse_pdf_to_txt(pdf_path=self.input_path)

        boundary = association.get_word_page()[-1]
        doc = fitz.Document(self.input_path)
        page_count = doc.pageCount
        with open(self.input_path[:-3] + 'txt', 'a') as txt_file:

            for i in range(page_count):
                page = doc.loadPage(i)
                blocks = page.getText("blocks")
                blocks_length = len(blocks)
                coordinate_page_dict = coordinate_dict[i]

                for block_index in range(blocks_length):
                    # (x0, y0, x1, y1, "lines in block", block_type, block_no)
                    block = blocks[block_index]
                    vertical = [block[1], block[3]]
                    horizontal = [block[0], block[2]]
                    height = vertical[1] - vertical[0]
                    content = block[4].strip()
                    if content.strip() == '':
                        continue
                    content = content.replace('\n', ' ')
                    # 检查这一文段是否在图表范围，默认False
                    in_table = False

                    if coordinate_page_dict:
                        for sequence in coordinate_page_dict:
                            if vertical[0] > page.rect.height - float(sequence[1]) \
                                    and vertical[1] < page.rect.height - float(sequence[0]):
                                in_table = True

                    if not in_table:
                        check = conf.ReModule(string=content)
                        # check = ReModule(string=content)

                        if i < boundary - 1 and not check.roman_numerals():
                            txt_file.write(str(horizontal[0]) + '\t' + str(vertical[1]
                                                                           - vertical[0]) + '\t' + content + '\n')
                            self.text_list.append([horizontal[0], height, content])
                            continue

                        if check.chapters_search() or check.lower_title_search():
                            txt_file.write(str(horizontal[0]) + '\t' + str(vertical[1]
                                                                           - vertical[0]) + '\t' + content + '\n')
                            self.text_list.append([horizontal[0], height, content])
                            continue

                        if check.image_search():
                            continue

                        if not check.figure_title_search() \
                                and not check.table_title_search() \
                                and not check.annotation_search() \
                                and not check.unit_search():
                            if horizontal[0] < 120 and 24.5 > height > 13.9:
                                if horizontal[0] > 114.1 or horizontal[0] < 113.9:
                                    txt_file.write(str(horizontal[0]) + '\t' + str(vertical[1]
                                                                                   - vertical[
                                                                                       0]) + '\t' + content + '\n')
                                    self.text_list.append([horizontal[0], height, content])

        return self.text_list
