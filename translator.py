
import PyPDF2
import nltk
from nltk.corpus import words
from tqdm import tqdm
from fpdf import FPDF
import pickle
import os
import json

from utils import *
from baidu_api import baidu_translate
from baidu_account import app_limit
from build_pdf import PDF


def detector(path, filename, vocab=words.words()):

    obj = open(path, "rb")
    reader = PyPDF2.PdfFileReader(obj)
    # print(reader.numPages)
    # print(reader.)
    # count = 0
    dic = dict()
    # dic[14] = []
    # last_full_stop_flag = False
    word_count = 0
    length = 0
    for page_id in tqdm(range(reader.numPages)):

        page = reader.getPage(page_id)
        raw_text = page.extractText()
        word_count += len(raw_text.split())
        length += len(raw_text)
        # print(raw_text)
        raw_text_lines = raw_text.split("\n")
        text_lines = list_cut_starting_ending_spaces(raw_text_lines)
        text_lines_combined = list_word_combination(text_lines, vocab, page_id)
        # print("[{0:03d}] text_lines_combined: {1}".format(page_id, text_lines_combined))

        if page_id > 0 and len(text_lines_combined) > 0:
            if text_lines_combined[0][0].isupper() or text_lines_combined[0][0].isdigit() or len(dic[page_id - 1]) == 0:
                pass
            else:
                if ". " in text_lines_combined[0]:
                    split_parts = text_lines_combined[0].split(". ")
                    last_part = split_parts[0] + "."
                    next_part = ". ".join(split_parts[1:])
                    if len(dic[page_id - 1]) == 0:
                        dic[page_id - 1] = [last_part]
                    else:
                        dic[page_id - 1][-1] = dic[page_id - 1][-1] + " " + last_part
                    text_lines_combined[0] = next_part
                else:
                    if len(dic[page_id - 1]) == 0:
                        dic[page_id - 1] = [text_lines_combined[0]]
                    else:
                        dic[page_id - 1][-1] = dic[page_id - 1][-1] + " " + text_lines_combined[0]
                    text_lines_combined = text_lines_combined[1:]


        # print(text_lines)
        # print(list_word_combination(text_lines, vocab))
        # page_no_enter = raw_text.replace("\n", " ")
        # count += len(page_no_enter)
        dic[page_id] = text_lines_combined
        # print("{}: {}".format(i, len(page_no_enter)))
        # word_list = page_no_enter.split()
    # for one_key in dic:
    #     print("{}: {}".format(one_key, dic[one_key]))
    save_path = "saves/{}_detected.pkl".format(filename)
    with open(save_path, "wb") as f:
        pickle.dump(dic, f)
    res_dic = {
        "file_name": filename,
        "file_path": path,
        "page": reader.numPages,
        "save_detected_path": save_path,
        "word_count": word_count,
        "length": length
    }
    print(json.dumps(res_dic, indent=4, ensure_ascii=False))
    return res_dic


def translate_step():
    pass


def translator(dic_path, translated_output_path):
    with open(dic_path, "rb") as f:
        dic = pickle.load(f)
    # print(dic.keys())  # 0 -391
    translated_dic = dict()
    # f_log = open("logs.txt", "a")
    for one_key in tqdm(dic.keys()):
        # print(dic[one_key])
        sentence_list = dic[one_key]
        result_list = []
        tmp_list = []
        tmp_count = 0
        for i, sentence in enumerate(sentence_list):
            if tmp_count + len(sentence) > app_limit:
                # f_log.write("[over limit] length = {} (next {} > {})\n".format(tmp_count, tmp_count + len(sentence), app_limit))
                long_sentence = "\n".join(tmp_list)
                translate_result = baidu_translate(long_sentence)
                result_list += translate_result
                tmp_list = []
                tmp_count = 0
            tmp_list.append(sentence)
            tmp_count += len(sentence)
            if i == len(sentence_list) - 1:
                # f_log.write("[page last] length = {}\n".format(tmp_count))
                long_sentence = "\n".join(tmp_list)
                translate_result = baidu_translate(long_sentence)
                result_list += translate_result
                tmp_list = []
                tmp_count = 0
        translated_dic[one_key] = result_list
        # f_log.write("page {}: start with {} sentences - finally get {} sentences\n\n".format(one_key, len(sentence_list), len(result_list)))
    with open(translated_output_path, "wb") as f:
        pickle.dump(translated_dic, f)
    res_dic = {
        "save_detected_path": dic_path,
        "save_translated_path": translated_output_path
    }
    print(json.dumps(res_dic, indent=4, ensure_ascii=False))
    return res_dic
    # f_log.close()


def create_pdf_pages(translated_dic_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    with open(translated_dic_path, "rb") as f:
        dic = pickle.load(f)
    for one_key in tqdm(list(dic.keys())):
        sentence_list = dic[one_key]
        sentence_src = "\n".join([item["src"] for item in sentence_list])
        sentence_dst = "\n".join([item["dst"] for item in sentence_list])
        with open("{}/page_{}.txt".format(output_path, one_key), "w") as f:
            f.write(sentence_src + "\n\n")
            f.write(sentence_dst + "\n")
    res_dic = {
        "save_translated_path": translated_dic_path,
        "save_all_pages_directory": output_path,
        "page": len(list(dic.keys()))
    }
    print(json.dumps(res_dic, indent=4, ensure_ascii=False))
    return res_dic


def build_pdf(filename, page_directory, page_num):
    pdf = PDF()
    for i in tqdm(range(page_num)):
        pdf.print_chapter(i + 1, "", "{}/page_{}.txt".format(page_directory, i))
        # print("pages/RM/page_{}.txt".format(i))
    pdf_path = "files/{}_translated.pdf".format(filename)
    pdf.output(pdf_path, "F")
    res_dic = {
        "filename": filename,
        "save_all_pages_directory": page_directory,
        "page": page_num,
        "pdf_path": pdf_path
    }
    print(json.dumps(res_dic, indent=4, ensure_ascii=False))
    return res_dic


if __name__ == '__main__':
    # translator("saves.pkl")

    create_pdf_pages("saves_translated.pkl", "pages/RM")


    # vocabulary = words.words()
    # # print([item for item in vocabulary if len(item) == 1])
    # for bad_word in ["thee", "ds", "es"]:
    #     if bad_word in vocabulary:
    #         print("removed \"{}\" from vocabulary".format(bad_word))
    #         vocabulary.remove(bad_word)
    # for good_word in []:
    #     if good_word not in vocabulary:
    #         print("added \"{}\" to vocabulary".format(good_word))
    #         vocabulary.append(good_word)
    # detector("files/Restall, Matthew - Seven Myths of the Spanish Conquest-Oxford University Press (2004_2003) (1).pdf", vocabulary)


    # for item in ["conquistadores", "conquistador", "es"]:
    #     print("\"{}\": {}".format(item, word_in_vocab("Adam", vocabulary)))
    #
    # # print("were" in vocabulary)
    #
    # # print([item for item in vocabulary if item[:3] == "jew"])  # sacrifice
    # # print(len(vocab))
    # # nltk.download('words')
    # for item in ["conquistadores"]:
    #     print("\"{}\": {}".format(item, item in vocabulary))
    pass
