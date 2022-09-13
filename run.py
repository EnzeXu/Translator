import os
import warnings
import argparse

from translator import detector, translator, create_pdf_pages, build_pdf

warnings.filterwarnings("ignore")


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", type=str, default="files/test.pdf", help="file path")
    parser.add_argument("-y", "--yes", action='store_true')
    opt = parser.parse_args()
    path = opt.path
    if not os.path.exists(path):
        path = "{}/{}".format("files", path)
        if not os.path.exists(path):
            print("File does not exists! Please check the file path.")
            return

    filename = path.split("/")[-1].replace(".pdf", "").replace(".PDF", "")
    detected_path = "saves/{}_detected.pkl".format(filename)
    if os.path.exists(detected_path):
        print("File {} exists. Skip detecting".format(detected_path))
    else:
        detected_dict = detector(path, filename)

    translated_path = "saves/{}_translated.pkl".format(filename)
    if os.path.exists(translated_path):
        print("File {} exists. Skip translating".format(translated_path))
    else:
        if not opt.yes:
            answer = input("Continue translating? [Y/N]")
            if answer not in ["Y", "y"]:
                print("Exit.")
                return
        else:
            translator(detected_path, translated_path)

    all_pages_directory = "pages/{}/".format(filename)
    pages_dic = create_pdf_pages(translated_path, all_pages_directory)
    build_pdf(filename, all_pages_directory, pages_dic["page"])


if __name__ == "__main__":
    run()
