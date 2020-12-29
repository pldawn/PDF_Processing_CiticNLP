# coding=utf-8
from Processor import Processor


def main():
    # 封装
    input_path = './Resources/2018Q3.pdf'
    agent = Processor()
    analyse_result = agent.analyzer(input_path)

    # title and paragraph
    content_list = analyse_result.article_list_extract()

    # functions
    find_result = analyse_result.find_content([['c3'], ['c1'], ['p2']])
    find_sentence_result = analyse_result.find_content([['c3'], ['c1'], ['p2s2']])
    target_result_01 = analyse_result.next_paragraph(step=1, paragraph=find_result[0][0])
    target_result_02 = analyse_result.next_paragraph(step=1, path=[['c3'], ['c1'], ['p2']])
    structure_list = analyse_result.article_structure_extract()
    return structure_list


if __name__ == '__main__':
    main()
