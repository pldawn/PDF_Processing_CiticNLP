# coding=utf-8
import re
from typing import Optional, List


class StructureTreeNode:

    def __init__(self, title='', children_node=None):
        if children_node is None:
            children_node = []
        self.title = title
        self.children_node = children_node

    def add_child_node(self, child_node):
        self.children_node.append(child_node)


class AnalyseFunction:
    # text list is result of TextFilter.py and is a line list
    # (horizontal[0], height, line content)
    def __init__(self, text_tree):
        self.text_tree = text_tree
        self.structure_list = []
        self.article_list = []
        self.article_list_dict = {}

    # this Module is used to get article structure.
    """
    1、该方法用于提取文章中所有的标题，基于N叉树前序遍历
    2、self.text_tree是生成的文章结构树，该方法会对所有的节点的标题按照先后顺序进行提取
    3、返回由所有标题组成的一维列表
    4、用法示例：
    structure_list = Analyse_Function.article_structure_extract()
    """
    def article_structure_extract(self):
        if self.text_tree is None:
            return []
        stack, output = [self.text_tree, ], self.structure_list
        while stack:
            root = stack.pop()
            if root.title:
                output.append(root.title)
            stack.extend(root.children_node[::-1])
        return self.structure_list

    # this Module is used to get article structure.
    """
    1、该方法用于提取文章中所有的文本块，基于N叉树前序遍历
    注释：文本块包括：标题和正文段落
    2、self.text_tree是生成的文章结构树，该方法会对所有的节点的标题、段落按先后顺序进行提取
    3、返回由所有文本块组成的一维列表
    4、用法示例：
    structure_list = Analyse_Function.article_list_extract()
    """
    def article_list_extract(self):
        if self.text_tree is None:
            return []
        stack, output = [self.text_tree, ], self.article_list
        while stack:
            root = stack.pop()
            if root.title:
                output.append(root.title)
            if root.paragraphs:
                for item in root.paragraphs:
                    output.append(item)
            stack.extend(root.children_node[::-1])
        for i in range(len(self.article_list)):
            self.article_list_dict[str(self.article_list[i])] = i
        return self.article_list

    # forward/step
    # path, 替换item_index
    """
    该方法用于段落查找，依据给定的文本块或者路径进行查找
    1、step是步长，基于当前文本块，默认为1， 即就是查找下一个文本块的内容
    2、path是路径，示例写法
    用法示例：path = [[c1], [c2], [t], [p1s1s2, p2]]， c1为下一级第一个部分， t为当年目录下的标题，拍
    p1为第一段，s1为第一句话。
    3、返回值为一个只有一个元素的list，用法示例：
    structure_list = Analyse_Function.next_paragraph()
    """
    def next_paragraph(self, step: int = 1, paragraph: Optional[str] = None,
                       path: List[List[str]] = None):
        if self.text_tree is None:
            return None
        if paragraph:
            base_value = self.article_list_dict.get(str([paragraph]), None)
            if base_value is not None:
                if len(self.article_list) > base_value + step > -1:
                    return self.article_list[base_value+step]
                else:
                    print('list out of index.')
                    return None
            else:
                print('content not exists.')
                return None
        if path:
            content = self.find_content(path)
            base_value = self.article_list.index(content[0]) + step
            if len(self.article_list) > base_value > -1:
                return self.article_list[base_value]
            else:
                print('list out of range.')
                return None

    """
    1、该方法用于依据路径查找文本块，返回一个单一元素的列表。
    2、用法示例：
    structure_list = Analyse_Function.find_content(path = [[c1], [c2], [p1s1s2, p2]])
    """
    def find_content(self, path):
        # path = [[c1], [c2], [t], [p1s1s2, p2]]
        if self.text_tree is None:
            return None
        path = path.copy()
        result = [self.text_tree]
        cache = []

        while path:
            route = path.pop(0)
            for ind in range(len(result)):
                # 文章树
                tree = result[ind]

                for r in route:
                    if r.startswith("c"):
                        # 索引
                        index = int(r[1:]) - 1
                        try:
                            position = tree.children_node[index]
                            cache.append(position)
                        except IndexError:
                            pass
                    elif r.startswith("t"):
                        try:
                            position = tree.title
                            head = position[:4]
                            if "、" in head:
                                start = head.index("、") + 1
                            elif "）" in head:
                                start = head.index("）") + 1
                            elif "." in head:
                                start = head.index(".") + 1
                            else:
                                start = 0
                            position = position[start:]
                            cache.append(position + "。")
                        except IndexError:
                            pass
                    elif r.startswith("p"):
                        if "s" in r:
                            first_s = r.index("s")
                            index = int(r[1:first_s]) - 1
                            try:
                                sents = r[first_s + 1:].split("s")
                                paragraphs = re.split("[。？！]", tree.paragraphs[index][0])
                                for s in sents:
                                    try:
                                        position = paragraphs[int(s) - 1]
                                        head = position[:3]
                                        if "是" in head:
                                            start = position.index("是") + 1
                                        else:
                                            start = 0
                                        position = position[start:]
                                        cache.append(position + "。")
                                    except IndexError:
                                        pass
                            except IndexError:
                                pass
                        else:
                            index = int(r[1:]) - 1
                            try:
                                position = tree.paragraphs[index]
                                head = position[:3]
                                if "是" in head:
                                    start = position.index("是") + 1
                                else:
                                    start = 0
                                position = position[start:]
                                cache.append(position)
                            except IndexError:
                                pass
                    else:
                        # 报错调整
                        raise ValueError("路径错误，重新输入路径。")

            result = cache
            cache = []

        return result
