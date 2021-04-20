How to package data
===================

Data have to be properly packaged to be analysed through our Mesos system.

.. warning::

   Currently the only data format supported is ``tar.gz``. 

Create a directory containing the fasta file to analyse. The directory name is up to you, however we recommend avoiding special characters and spaces.

Put all needed data in the directory, with the primer file, named ``primers.tsv`` and the metadata file ``sample_metadata.tsv``.

you can now compress the directory, with the following command:

::

  tar cvzf name_compressed_file.tar.gz directory_to_compress

The resulting ``tar.gz`` will be uploaded to our analysis system, using the Uploader tool.
