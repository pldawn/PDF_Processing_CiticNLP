# coding=utf-8
from conf import ReModule as Re
import conf
from collections import defaultdict


class IndexNode:
    def __init__(self):
        self.title = ""
        self.paragraphs = []
        self.children_node = []
        self.parent = "root"


class ArticleTree:
    def __init__(self, text_list):
        self.text_list = text_list
        self.x0_dict = defaultdict(int)
        self.plain_text = []
        self.start_position = 0
        self.end_position = 0

    def tree_construction(self):
        self.catalogue_region()
        self.plain_text_generation()
        result = self.convert_to_tree()
        return result

    def catalogue_region(self):
        text_list = self.text_list
        for line_index in range(self.end_position, len(text_list)):
            check = Re(text_list[line_index][2])
            if check.catalogue_search():
                self.start_position = line_index
            if check.chapters_search() and text_list[line_index][0] > 150:
                self.end_position = line_index
                break

    def plain_text_generation(self):
        most_x0 = 0
        for (x0, height, content) in self.text_list:
            self.x0_dict[x0] += 1
        for key, value in self.x0_dict.items():
            if value == max(self.x0_dict.values()):
                most_x0 = key
        for index in range(len(self.text_list)):
            (x0, height, content) = self.text_list[index]
            if index >= self.end_position or index < self.start_position:
                if abs(x0 - most_x0) >= 5:
                    self.plain_text.append(content)
                else:
                    self.plain_text[-1] += content

        return self.plain_text

    def article_name_extract(self):
        text_list = self.text_list
        article_name = text_list[0][-1] + text_list[1][-1]
        return article_name

    def convert_to_tree(self):
        plain_text = self.plain_text
        root_node = IndexNode()
        root_node.title = self.article_name_extract()
        parent_stack = [('root', root_node)]

        for content in plain_text:
            if not content:
                continue
            index_token = conf.get_index_token(content)
            if index_token is not None:
                if len(content) < 50:
                    new_node = IndexNode()
                    new_node.title = [content]
                else:
                    parent_stack[-1][1].paragraphs.append([content])
                    continue
                is_added = False

                # 与上一标题行平级
                for i in range(len(parent_stack), 0, -1):
                    ind = i - 1
                    if parent_stack[ind][0] == index_token:
                        while len(parent_stack) > ind:
                            parent_stack.pop()
                        parent_stack[-1][1].children_node.append(new_node)
                        new_node.parent = parent_stack[-1][1]
                        parent_stack.append((index_token, new_node))
                        is_added = True
                        break

                if not is_added:
                    parent_stack[-1][1].children_node.append(new_node)
                    new_node.parent = parent_stack[-1][1]
                    parent_stack.append((index_token, new_node))

            else:
                parent_stack[-1][1].paragraphs.append([content])

        return root_node
