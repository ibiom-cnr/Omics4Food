# coding=utf-8
import argparse
import os
import warnings
from shutil import copyfileobj, copytree, copy, make_archive, move, rmtree
from zipfile import ZipFile
import unicodedata
import pandas as pd
import argcomplete
from Bio import SeqIO
import sys
import numpy
from biom import load_table
from datetime import datetime
from plotnine import *
import pdfkit

# noinspection DuplicatedCode

warnings.filterwarnings("ignore")


def split_options():
    parser = argparse.ArgumentParser(description="prepare data for ProBio report", prefix_chars="-")
    parser.add_argument("-d", "--denoising_stats_qza", type=str,
                        help="qiime2 qza artifacts containing the denoising statics [denoising-stats.qza]",
                        action="store", required=True)
    parser.add_argument("-m", "--metadata", type=str,
                        help="metadata file",
                        action="store", required=True)
    parser.add_argument("-a", "--asv_qza", type=str,
                        help="inferred ASVs qza file [rep-seqs.qza]",
                        action="store", required=True)
    parser.add_argument("-T", "--asv_table_qza", type=str,
                        help="inferred ASV table qza file [table.qza]",
                        action="store", required=True)
    parser.add_argument("-t", "--tax_barplot", type=str,
                        help="taxonomy bar plot [taxa-bar-plots.qzv]",
                        action="store", required=True)
    parser.add_argument("-b", "--base_report", type=str,
                        help="base report html",
                        action="store", required=False,
                        default="/Users/brunofosso/Documents/IBIOM/Progetti/INNONETWORK/PDF_generation/base_report/report_static.html")
    parser.add_argument("-o", "--outdir", type=str,
                        help="directory where output date will be stored",
                        action="store", required=True)
    argcomplete.autocomplete(parser)
    return parser.parse_args()


def check_file(file_name):
    """
    This function verifies the indicated file exists and it is not empty
    :param file_name: file name
    :type file_name: str
    """
    if not os.path.exists(file_name):
        sys.exit("{} doesn't exists!!! Have you indicated the right file name?")
    if os.stat(file_name)[6] == 0:
        sys.exit("{} is empty!!! PLEASE CHECK IT!!! Have you indicated the right file name?")


def sample2feaures(metadata_file):
    """

    :param metadata_file:
    :param metadata_file: str
    :return sample2meta: dictionary containing a list of metadata and associated values for each sample.
    """
    df = pd.read_csv(metadata_file, sep="\t", header=0)
    _meta = list(df.columns)
    sample2meta = {}
    for _sample in [i for i in df[_meta[0]] if not i.startswith("#")]:
        # print(sample)
        d = df[df[_meta[0]] == _sample]
        _l = []
        for _ in _meta[1:]:
            _l.append([_, list(d[_])[0]])
        sample2meta[_sample] = _l
    return sample2meta, _meta[1:]


def sample2denosing_statisitcs(denoising_qza, _sample2metadata):
    with ZipFile(denoising_qza, "r") as zipObj:
        for filename in zipObj.namelist():
            if filename.endswith("stats.tsv"):
                df = pd.read_csv(zipObj.open(filename), sep="\t", header=0)
                break
    _sample_name_c = list(df.columns)[0]
    sample2denoising_info = {}
    for _sample in _sample2metadata:
        _ = df[df[_sample_name_c] == _sample]
        print(_)
        sample2denoising_info[_sample] = {"input": float(list(_["input"])[0]),
                                          "filtered": float(list(_["filtered"])[0]),
                                          "non-chimeric": float(list(_["non-chimeric"])[0])}
    return sample2denoising_info


def sample2sequence_profile(ASV_rep_seq_, ASV_table):
    asv2len = {}
    with ZipFile(ASV_rep_seq_, "r") as zipObj:
        for filename in zipObj.namelist():
            if filename.endswith("dna-sequences.fasta"):
                source = zipObj.open(filename)
                target = open("dna-sequences.fasta", "wb")
                with source, target:
                    copyfileobj(source, target)
                break
        with open("dna-sequences.fasta") as a:
            for record in SeqIO.parse(a, "fasta"):
                asv2len[record.id] = len(str(record.seq))
    asv_df = pd.DataFrame({"ASV": list(asv2len.keys()), "LEN": list(asv2len.values())})
    with ZipFile(ASV_table, "r") as zipObj:
        for filename in zipObj.namelist():
            if filename.endswith("feature-table.biom"):
                source = zipObj.open(filename)
                target = open("feature-table.biom", "wb")
                with source, target:
                    copyfileobj(source, target)
                table_df = load_table("feature-table.biom").to_dataframe()
                break
    for name in ["dna-sequences.fasta", "feature-table.biom"]:
        try:
            os.remove(name)
        except OSError as e:
            print("Error: %s : %s" % (name, e.strerror))
    return asv_df, table_df


def import_taxonomy(taxonomy_qzv, meta_list):
    rank2df = {}
    level2rank = {"1": "kingdom", "2": "phylum", "3": "class", "4": "order", "5": "family", "6": "genus",
                  "7": "species"}
    # level2rank = {"2": "phylum"}
    with ZipFile(taxonomy_qzv, "r") as zipObj:
        listofnames = zipObj.namelist()
        for rank, rname in level2rank.items():
            for filename in listofnames:
                if filename.endswith("level-%s.csv" % rank):
                    df = pd.read_csv(zipObj.open(filename), sep=",", header=0)
                    _col = [i for i in df.columns if i not in meta_list]
                    df = df[_col]
                    df = df.set_index("index").T
                    rank2df[rname] = df
    return rank2df


def relative_counts(df, _sample):
    """
    This function generates the relative counts for the analysed taxa tabal
    :param df: pandas dataframe generated from import_taxonomy function
    :type df: pd.DataFrame
    :param _sample: sample nale
    :type _sample: str
    :return sample_d: pandas dataframe containing the relative counts
    """
    sample_d = pd.DataFrame(df[_sample])
    _s = float(sample_d.sum(0))
    sample_d["relative"] = sample_d[_sample] / _s
    sample_d = sample_d[sample_d["relative"] > 0]
    sample_d = sample_d.sort_values(by="relative", ascending=False)
    return sample_d.head(10)


def generate_metadata_string(_sample, lista, input_sequence):
    stringa = "<p>ID del campione: <b>{}</b></p>\n".format(_sample)
    for i in lista:
        stringa += "<p>{}: <b>{}</b></p>\n".format(i[0], i[1])
    stringa += "<p>Sequenze prodotte: <b>{}</b></p>\n".format(input_sequence)
    return stringa


def generate_denoising_table(_sample, denoising_data):
    d = denoising_data[_sample]
    print
    if float(d["input"]) > 0:
        stringa = "<tr>\n<td>{0}</td>\n<td>{1}</td>\n<td>{2:.2f}</td>\n<td>{3}</td>\n<td>{4:.2f}</td>\n</tr>\n". \
            format(d["input"], d["filtered"], (d["filtered"] / d["input"]) * 100, d["non-chimeric"],
                   (d["non-chimeric"] / d["input"]) * 100)
    else:
        stringa = False
    return stringa


def generate_len_plot(_sample, asv_table, asv2len, folder):
    _name = list(asv_table[asv_table[_sample] > 0].index)
    d = asv2len[asv2len["ASV"].isin(_name)]
    plot_name = os.path.join(folder, "images", "len_dist.png")
    p = (ggplot(d, aes(x='LEN')) +
         geom_density(alpha=0.1, fill="red") +
         labs(title="Distribuzione della lunghezza delle ASV", x="lunghezza in nt", y="abbondanza relativa") +
         theme(axis_text_x=element_text(size=14),
               panel_grid_major_y=element_blank(),
               panel_grid_minor_y=element_blank(),
               axis_title_x=element_text(size=16, face="bold"),
               axis_title_y=element_text(size=16, face="bold"),
               axis_text_y=element_text(size=14),
               plot_title=element_text(size=18, face="bold", hjust=0.5)))
    p.save(filename=plot_name, dpi=300, format="png",
           width=10,
           height=10, units="in")
    stringa = "<tr>\n<td>{0:.2f}</td>\n<td>{0:.2f}</td>\n<td>{0:.2f}</td>\n<td>{0:.2f}</td>\n</tr>\n".format(
        d["LEN"].min(),
        d["LEN"].mean(),
        d["LEN"].median(),
        d["LEN"].max())
    return stringa


def prepare_taxa_tables(tax_dict, _sample, lista_aggiunte):
    """

    :param tax_dict:
    :param _sample:
    :param lista_aggiunte:
    :type lista_aggiunte: list
    :return:
    """
    for rank in ["kingdom", "phylum", "class", "order", "family", "genus", "species"]:
        df = relative_counts(tax_dict[rank], _sample)
        stringa = "<tr>\n"
        for taxa in list(df.index):
            stringa += "<td>{0}</td>\n<td>{1:.3f}%</td>\n".format(taxa, float(df.loc[taxa]["relative"]) * 100)
            stringa += "</tr>\n"
        lista_aggiunte.append(stringa)
    return lista_aggiunte


def generate_report(_sample, _basic_report, sample2meta, denoising_data, asv2len, asv_table, taxa_dict, _outdir):
    print(_sample)
    denoising_table = generate_denoising_table(_sample, denoising_data)
    if denoising_table:
        dTo = datetime.now()
        folder = os.path.join(_outdir,
                              "{}_report_{}_{}_{}_{}_{}_{}".format(_sample, dTo.year, dTo.month, dTo.day, dTo.hour,
                                                                   dTo.minute,
                                                                   dTo.second))
        if not os.path.exists(folder):
            os.mkdir(folder)
        base_folder_images = os.path.join(os.path.split(_basic_report)[0], "images")
        copytree(base_folder_images, os.path.join(os.getcwd(), folder, "images"))
        copy(os.path.join(base_folder_images, "style.css"), os.path.join(os.getcwd(), folder, "style.css"))
        metadata_table = generate_metadata_string(_sample, sample2meta[_sample], denoising_data[_sample]["input"])

        asv_len_table = generate_len_plot(_sample, asv_table, asv2len, folder)
        # generiamo la lista con le porzioni di codice html da aggiungere al report base
        # nota bene che è fondamentale l'ordine
        adding_list = [metadata_table, denoising_table, asv_len_table]
        adding_list = prepare_taxa_tables(taxa_dict, _sample, adding_list)
        with open(_basic_report) as html:
            lines = list(map(str.strip, html.readlines()))
        for a, b in zip(
                ["METADATA_DA_INSERIRE", "TABELLA_DENOISING", "TABELLA_ASV", "TABELLA_KINGDOM", "TABELLA_PHYLUM",
                 "TABELLA_CLASS", "TABELLA_ORDER", "TABELLA_FAMILY", "TABELLA_GENUS", "TABELLA_SPECIES"],
                adding_list):
            lines[lines.index(a)] = b
        open(os.path.join(folder, "report.html"), "w").write("\n".join(lines))
        wd = os.getcwd()
        os.chdir(folder)
        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '0.5in',
            'footer-font-name': 'Times-Italic',
            'footer-font-size': "10",
            'footer-right': '[page]',
            'encoding': "UTF-8",
            'enable-local-file-access': None
        }
        # css = os.path.join(os.getcwd(), "style.css")
        pdfkit.from_file('report.html', '%s.pdf' % _sample, options=options)
        os.chdir(wd)
        move(os.path.join(folder, '%s.pdf' % _sample), wd)
        make_archive("{}_data".format(folder), 'zip', folder)
        rmtree(folder)
    else:
        print("No sequences were available for {}".format(sample))


if __name__ == "__main__":
    opt = split_options()
    basic_report, metadata, den_stat_qza, rep_seq, asv_tab, barplot, outdir = \
        opt.base_report, opt.metadata, opt.denoising_stats_qza, opt.asv_qza, opt.asv_table_qza, opt.tax_barplot, opt.outdir
    # inserire qui il check dei file
    sample2metadata, metadata_list = sample2feaures(metadata)
    denoising_info = sample2denosing_statisitcs(den_stat_qza, sample2metadata)
    asv_len_df, asv_table_df = sample2sequence_profile(rep_seq, asv_tab)
    tax_rank2df = import_taxonomy(barplot, metadata_list)
    for sample in sample2metadata:
        generate_report(sample, basic_report, sample2metadata, denoising_info, asv_len_df, asv_table_df, tax_rank2df,
                        outdir)
