
def dictree_by_esm():
    import esm
    # pip install esmre

    print('获取字典树trie')
    word_list = ['apple', 'alien', 'app']
    dic = esm.Index()
    for i in range(len(word_list)):
        word = word_list[i].lower()
        dic.enter(word)
    dic.fix()

    sentence = 'i like apple and app'
    result = dic.query(sentence.lower())
    result = list(set(result))
    print(result)


def dictree_by_ahocorasick():
    import ahocorasick
    # > pip install pyahocorasick

    A = ahocorasick.Automaton()
    words = "he hers his she hi him man he"
    for i,w in enumerate(words.split()):
        A.add_word(w, (i, w))

    # convert the trie to an Aho-Corasick automaton to enable Aho-Corasick search
    A.make_automaton()

    """
    import cPickle
    >>> pickled = cPickle.dumps(A)
    >>> B = cPickle.loads(pickled)
    """

    s = "he rshershidamanza "
    print([x[1][1] for x in A.iter(s)])

    for end_index, (insert_order, original_value) in A.iter(s, 2, 8):
        start_index = end_index - len(original_value) + 1
        print((start_index, end_index, (insert_order, original_value)))
        assert s[start_index:start_index + len(original_value)] == original_value

    print("====")

    def callback(index, item):
        print(index, item)

    A.find_all(s, callback, 2, 11)


def dictree_by_flashtext():
    from flashtext.keyword import KeywordProcessor

    keyword_processor = KeywordProcessor(case_sensitive=False)
    words = "he hers his she hi him man he"
    keyword_processor.add_keywords_from_list(words.split())

    s = "he rshershidamanza "
    keywords_found = keyword_processor.extract_keywords(s, span_info=True)
    print(keywords_found)
