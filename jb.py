from os import path
import jieba
import jieba.analyse as analyse


def jieba_action(file_name, ip_address):
    ana_text = ''
    with open(file_name, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line_list = line.split(',', 6)
            if line_list[0] == ip_address:
                ana_text += line_list[6]
                ana_text += ','
    the_word = ''
    for key in analyse.extract_tags(ana_text, 20, withWeight=False):
        the_word += key + ','
    return the_word
