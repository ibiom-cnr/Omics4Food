How to package data
===================

Data have to be properly packaged to be analysed through our Mesos system.

.. warning::

   Currently the only data format supported is ``tar.gz``. 

Create a directory containing the fasta file to analyse. The directory name is up to you, however we recommend avoiding special characters and spaces.

Put all needed data in the directory, with the primer file, named ``primers.tsv``, and the metadata file, named ``sample_metadata.tsv``.

You can now compress the directory, with the following command:

::

  tar cvzf compressed_output_file.tar.gz directory_to_compress

The resulting ``tar.gz`` file can be uploaded to our analysis system, using the INFN Uploader tool.
