from PorterStemmer import PorterStemmer

symbols = [",", ".", "?", "-", "!", "—", "\"", "\'", "“", "”", " "]
pairs = [["ﬁ", "fi"], ["ﬂ", "fl"], ["ﬀ", "ff"], ["ﬄ", "ffl"], ["ﬃ", "ffi"], ["—", " — "]]
bad_word_list = []
p = PorterStemmer()


def word_purify(word):
    for item in symbols:
        word = word.replace(item, "")
    for one_pair in pairs:
        word = word.replace(one_pair[0], one_pair[1])
    return word


def word_stem(word):
    return p.stem(word, 0, len(word) - 1)


def word_in_vocab(word, vocab):
    word = word_purify(word)
    if len(word) == 0:
        return False
    if len(word) == 1 and word not in ["a", "A", "I", "i"]:
        return False
    if word in vocab:
        return True
    word = word.lower()
    if word in vocab:
        return True
    if len(word) >= 3 and word[-1] == "s" and word[:-1] in vocab:
        return True
    if word[-1] == "e":
        return False
    if word in bad_word_list:
        return False
    if word_stem(word) in vocab:
        return True


def list_word_combination(raw_list, vocab, page=-1):
    new_list = []
    # tmp_list = []
    for i, item in enumerate(raw_list):
        words = item.split()
        # print("[rule 1]")
        for j, one_word in enumerate(words):
            if 1 <= len(one_word) and one_word not in symbols:
                if j - 1 >= 0 and words[j - 1] not in symbols and len(words[j - 1]) >= 1 and not word_in_vocab(words[j - 1], vocab) and not word_in_vocab(words[j], vocab) and word_in_vocab(words[j - 1] + words[j], vocab):
                    # print("{} + {} = {}".format(words[j - 1], words[j], words[j - 1] + words[j]))
                    words[j] = words[j - 1] + words[j]
                    words[j - 1] = ""
                elif j + 1 <= len(words) - 1 and words[j + 1] not in symbols and len(words[j + 1]) >= 1 and not word_in_vocab(words[j + 1], vocab) and not word_in_vocab(words[j], vocab) and word_in_vocab(words[j] + words[j + 1], vocab):
                    # print("{} + {} = {}".format(words[j], words[j + 1], words[j] + words[j + 1]))
                    words[j] = words[j] + words[j + 1]
                    words[j + 1] = ""
        words = [item for item in words if len(item) > 0]
        # print("[rule 2]")
        for j, one_word in enumerate(words):
            if 1 <= len(one_word) and one_word not in symbols:
                if j - 1 >= 0 and words[j - 1] not in symbols and len(words[j - 1]) >= 1 and not word_in_vocab(words[j - 1], vocab) and word_in_vocab(words[j - 1] + words[j], vocab):
                    # print("{} + {} = {}".format(words[j - 1], words[j], words[j - 1] + words[j]))
                    words[j] = words[j - 1] + words[j]
                    words[j - 1] = ""
                elif j + 1 <= len(words) - 1 and words[j + 1] not in symbols and len(words[j + 1]) >= 1 and not word_in_vocab(words[j + 1], vocab) and word_in_vocab(words[j] + words[j + 1], vocab):
                    # print("{} + {} = {}".format(words[j], words[j + 1], words[j] + words[j + 1]))
                    words[j] = words[j] + words[j + 1]
                    words[j + 1] = ""
        words = [item for item in words if len(item) > 0]
        # print("[rule 3]")
        for j, one_word in enumerate(words):
            if j + 1 <= len(words) - 1 and words[j + 1] not in symbols and (
                        j + 1 == len(words) - 1 or word_in_vocab(words[j + 2], vocab)) and (
                             j == 0 or word_in_vocab(words[j - 1], vocab)) and not word_in_vocab(words[j],
                                                                                                 vocab) and not word_in_vocab(
                words[j + 1], vocab) and len(words[j + 1]) >= 1 and words[j][-1] not in symbols and words[j + 1][
                     0] not in symbols and not words[j + 1][0].isupper():
                # print("{} + {} = {}".format(words[j], words[j + 1], words[j] + words[j + 1]))
                words[j] = words[j] + words[j + 1]
                words[j + 1] = ""
        words = [item for item in words if len(item) > 0]
        tmp = ""
        for j, one_word in enumerate(words):
            if not word_in_vocab(one_word, vocab):
                with open("saves/mis_matches.txt", "a") as f:
                    f.write("[Page {0:03d}] word \"{1}\" in \"{2}\"\n".format(page, one_word, item))
            if j != 0 and one_word[0] != "-":
                tmp += " "
            tmp += one_word
        new_list.append(tmp)
    return new_list


def list_cut_starting_ending_spaces(raw_list):
    new_list = []
    tmp = ""
    for i, item in enumerate(raw_list):
        if len(item) == 0:
            continue
        drop_flag = False
        while item[0] == " ":
            if len(item) == 1:
                drop_flag = True
                break
            item = item[1:]
        while item[-1] == " ":
            if len(item) == 1:
                drop_flag = True
                break
            item = item[:-1]
        if not drop_flag:
            tmp += " " if len(tmp) > 0 and item[0] != "-" else ""
            tmp += item
            if item[-1] in [".", "!", "?"] or i == len(raw_list) - 1:
                for one_pair in pairs:
                    tmp = tmp.replace(one_pair[0], one_pair[1])
                new_list.append(tmp)
                tmp = ""
    return new_list


if __name__ == "__main__":
    print(list_cut_starting_ending_spaces(["", " ", "  ", " sdsds  sdssd sd s ds    ", "a  ", "  b"]))
    pass





