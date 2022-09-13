import os
import warnings

from translator import detector, translator, create_pdf_pages, build_pdf

warnings.filterwarnings("ignore")


def run(path):
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
    run("files/Manuscript_V4.pdf")
