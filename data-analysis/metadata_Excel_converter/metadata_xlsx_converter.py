# coding=utf-8
import argparse
import os
import warnings
import unicodedata
import pandas as pd
import argcomplete
import sys
from xlrd import XLRDError
from openpyxl.utils.exceptions import InvalidFileException

# noinspection DuplicatedCode

warnings.filterwarnings("ignore")


def split_options():
    parser = argparse.ArgumentParser(description="convert xls(x) metadata to tsv", prefix_chars="-")
    parser.add_argument("-m", "--metadata", type=str,
                        help="metadata file",
                        action="store", required=True)
    parser.add_argument("-o", "--outdir", type=str,
                        help="directory where output date will be stored",
                        action="store", required=True)
    argcomplete.autocomplete(parser)
    return parser.parse_args()


def check_file(file_path, _out_file):
    _answer = 0
    if not os.path.exists(file_path):
        _answer = 1
    elif file_path.endswith("xls"):
        try:
            df = pd.DataFrame(pd.read_excel(file_path, engine="xlrd"))
            df.to_csv(_out_file, sep="\t", header=True, index=None)
        except XLRDError:
            _answer = 2
    elif file_path.endswith("xlsx"):
        try:
            df = pd.DataFrame(pd.read_excel(file_path, engine='openpyxl'))
            df.to_csv(_out_file, sep="\t", header=True, index=None)
        except InvalidFileException:
            _answer = 2
    else:
        try:
            df = pd.DataFrame(pd.read_excel(file_path, engine='openpyxl'))
            df.to_csv(_out_file, sep="\t", header=True, index=None)
        except InvalidFileException:
            _answer = 2
    return _answer

if __name__ == "__main__":
    opt = split_options()
    excel_file, outdir = opt.metadata, opt.outdir
    out_file = os.path.join(outdir, "{}.tsv".format("".join(excel_file.split(".")[:-1])))
    a = check_file(excel_file, out_file)
    if a == 0:
        print("Conversion completed: {} generated".format(out_file))
    elif a == 1:
        print("The {} file doesn't exists!!!".format(excel_file))
    elif a == 2:
        print("The {} is not in an expected format".format(excel_file))