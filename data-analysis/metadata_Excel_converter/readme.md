Environment Configuration
===========
This script converts Excel files to tsv by using *_pandas_*, *_xlrd_* and *_openpyxl_*.  


1. Install the required packages:
   ```
   conda install xlrd
   conda install openpyxl
   ```    
   
   
Usage
=====
```
python ../metadata_xlsx_converter.py \
    -m metadata.tsv \
    -o /PATH/TO/outdir
```
