Environment Configuration
===========
This scripts generate a summary report of the metabarcoding analysis performed by using *QIIME2*.  
It has been developed to be exectued in the same conda environment in which QIIME2 is executed.  
The scripts requires a folder containing all the stuffs needed to create an html file who will be converted in PDF by using `wkhtmltopdf`.  

1. Activate the appropriate *Conda* environment:  
    `conda activate qiime2-2019.9`  
2. Install the required packages:
   ```
   pip install pdfkit
   sudo apt-get install `wkhtmltopdf`
   conda install biopython
   conda install argcomplete
   conda install -c conda-forge plotnine
   ```  
3. Download the the repository contenc on your machine:  
   
   
Usage
=====
```
python ../generate_PDF_report.py \
    -m metadata.tsv \
    -d denoising-stats_16S.qza \
    -a rep-seqs_16S.qza \
    -T table_16S.qza \
    -t taxa-bar-plots_16S_SKLEARN.qzv \
    -b /PATH/TO/base_report/report_static.html 
```