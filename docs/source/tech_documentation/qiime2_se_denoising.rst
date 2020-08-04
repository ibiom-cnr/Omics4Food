Qiime 2 Single End: Denoising
=============================

The `Qiime2 <https://docs.qiime2.org/2020.6/tutorials/>`_ Denoising step for Single End multiplexed data is made by 13 steps.

.. note::

   Please referes to `Qiime 2 official documentation <https://docs.qiime2.org/2020.6/tutorials/moving-pictures/>`_ for additional information.

``Data download``
-----------------

:Description: This step download data from the ReCaS Swift storage to the MESOS Cluster, for the analysis.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/data_download.json>`_.

:Input parameters:

	``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster.

	Mandatory: YES

	.. warning::

           The ``{{ job_run_id }}`` is the same for all the analysis step, in this case the whole *Qiime 2 Denoising* steps.

	``{{ DATA_URL }}``: URL associated to the data uploaded on (ReCaS) Swift.

	Mandatory: YES

	Data URL `example <http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/4AFD40C4DF01B75F35CB90ECFE789D91/81EE76C6F5210A26CE981AD81155B17E/test-data.tar.gz>`_


``Qiime2: Import``
------------------

:Description: Import tool.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.1.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES


``Qiime2: Demux``
-----------------

:Description: Run qiime 2 demultiplexing step.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.2.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Demux Summarize``
---------------------------

:Description: Run Qiime 2 demux summarize.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.3.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Dada2``
-----------------

:Description: run qiime dada2

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.4.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

	``{{ trunc_len }}``: truncate each sequence at specified position.

	Default value: 120

        Mandatory: YES

        .. warning::

           This value has to be configurable on the LIMS.

        ``{{ trim_len }}``: trimm off the first specified number of bases of each sequence.

	Default value: 0

        Mandatory: YES

	.. warning::

	   This value has to be configurable on the LIMS.


``Qiime2: Feature table summary``
---------------------------------

:Description: Run qiime future table summarize.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.5.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Feature table tabulate sequences``
--------------------------------------------

:Description: Run qiime future table tabulate seqs.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.6.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Metadata tabulate``
-----------------------------

:Description: Run qiime to tabulate metadata.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.7.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Create phylogenetic tree``
------------------------------------

:Description: Run qiime to generate a tree for phylogenetic diversity analyses.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.8.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Export outputs``
--------------------------

:Description: Run qiime to export data.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.9.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Biom``
--------

:Description: Run biom to create summary table.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/qiime2_denoising.10.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

   Please note that Biom requires more resources. Currently set to 2 CPUs and 1 GB of memory.


``Prepare data for the upload``
-------------------------------

:Description: Prepare data for the upload on ReCaS Swift. Currently compress outputs to a single tar.gz file.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/prepare_data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

   The output tarball is named: ``qiime2_se_denoising.tar.gz``

.. note::

   The input ``sample_metadata.tsv`` is included in the output tarball, since it is needed in the next step :doc:`qiime2_se_diversity`

``Data upload``
---------------

:Description: Upload data on ReCaS Swift.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_denoising/data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

        .. warning::

           The following parameters are mandatory for each step requiring data Upload on ReCaS Swift and should not be changed.

	``USERNAME`` and ``PROJECT_ID``: Username and project-ID to identify the ReCaS Swift directory and upload the data, making them available to download.

        ::

          OUTPUT_PROTOCOL: swift+keystone
          OUTPUT_ENDPOINT: https://cloud.recas.ba.infn.it:5000/v3
          OS_IDENTITY_API_VERSION: 3
          OS_PROJECT_DOMAIN_ID: default
          OUTPUT_REGION: recas-cloud
          OUTPUT_TENANT: *****
          OUTPUT_USERNAME: *****
          OUTPUT_PASSWORD: *****

.. note::

   The output file ``qiime2_se_denoising.tar.gz`` name is specified at the line:

   ::

     { "name": "OUTPUT_FILENAMES", "value": "output_{{ job_run_id }}/qiime2_se_denoising.tar.gz" },

   and should match the output file name specified in the previous step.
