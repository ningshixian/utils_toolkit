import numpy as np
import re
import string
import codecs


def cut_and_padding(seq, max_len, pad=0):
    """
    cut or pad the sequence to fixed size
    Args:
        seq:     sequence
        max_len:    the fixed size specified
        pad:    symbol to pad
    Returns:
        fixed size sequence
    """
    if len(seq) >= max_len:
        return seq[:max_len]
    else:
        return seq + [pad] * (max_len - len(seq))


def to_categorical(y, nb_classes=None):
    """Convert class vector (integers from 0 to nb_classes)
    to binary class matrix, for use with categorical_crossentropy.
    """
    if not nb_classes:
        nb_classes = np.max(y) + 1
    Y = np.zeros((len(y), nb_classes))
    for i in range(len(y)):
        Y[i, y[i]] = 1.0
    return Y


def base_filter():
    import string

    f = string.punctuation
    f = f.replace("'", "")
    f += "\t\n"
    return f


def create_dico(item_list):
    """
    Create a dictionary of items from a list of list of items.
    """
    assert type(item_list) is list
    dico = {}
    for items in item_list:
        for item in items:
            if item not in dico:
                dico[item] = 1
            else:
                dico[item] += 1
    return dico


def create_mapping(dico):
    """
    Create a mapping (item to ID / ID to item) from a dictionary.
    Items are ordered by decreasing frequency.
    """
    sorted_items = sorted(dico.items(), key=lambda x: (-x[1], x[0]))
    id_to_item = {i: v[0] for i, v in enumerate(sorted_items)}
    item_to_id = {v: k for k, v in id_to_item.items()}
    return item_to_id, id_to_item


def wordNormalize(word):
    """
    对单词进行清洗,特殊符号归一化
    :param word:
    :return:
    """
    word = word.strip().lower()
    word = re.sub(u"\s+", "", word, flags=re.U)  # 匹配任何空白字符
    word = word.replace("--", "-")
    word = re.sub('"+', '"', word)

    if word.isdigit():
        word = "1"
    else:
        temp = word
        for char in word:
            if char not in string.printable:
                temp = temp.replace(char, "*")
        word = temp
    return word


def get_stopword(file_path):
    # 从文件导入停用词表
    with codecs.open(file_path, "r", "utf-8") as f:
        stpwrd_content = f.read()
        stpwrdlst = stpwrd_content.splitlines()
    return stpwrdlst


def is_number(s):
    '''
    判断字符串是否为数字
    '''
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def number_filter(word_list):
    """去除数字"""
    words_list = [word for word in word_list if not is_number(word)]
    return words_list


def stopword_filter(word_list, stpwrdlst):
    """去除停用词
    word_list: 文本分词后的词列表
    stpwrdlst: 停用词列表
    Return: 去除停用词后的词列表
    """
    word_list = list(filter(lambda x: x not in stpwrdlst, word_list))
    return word_list


def clean(text):
    # 去掉标点符号
    text = re.sub("[’!\"#$%&'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+", " ", text)
    # 去除不可见字符
    text = re.sub(
        "[\001\002\003\004\005\006\007\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a]+",
        "",
        text,
    )
    return text


# 打乱数据顺序
def shuffle_in_unison(x, y):
    assert len(x) == len(y)
    shuffled_x = [0] * len(x)
    shuffled_y = [0] * len(y)
    permutation = np.random.permutation(len(x))
    for old_index, new_index in enumerate(permutation):
        shuffled_x[new_index] = x[old_index]
        shuffled_y[new_index] = y[old_index]
    return shuffled_x, shuffled_y
