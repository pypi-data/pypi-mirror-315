# -*- coding: utf8 -*-


"""
通过中文语料库，生成随机中文
"""
import os.path
import random

data_file = os.path.join(os.path.dirname(__file__), 'global_word.rst')
with open(data_file, 'r', encoding='utf8') as f:
    chinese_words = f.readline()


def raw(size: int):
    """
    生成随机中文，指定中文字数
    :param size:
    :return:
    """
    return_str = ''
    length = len(chinese_words)
    for i in range(size):
        idx = random.randint(0, length - 1)
        word = chinese_words[idx]
        return_str += word
    return return_str


if __name__ == '__main__':
    print(raw(10))
