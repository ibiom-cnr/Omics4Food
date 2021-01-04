Qiime 2 Paired End (demultiplexed data): Denoising
==================================================

The `Qiime2 <https://docs.qiime2.org/2020.6/tutorials/>`_ Denoising step for Paired End demultiplexed data is made by 12 steps.

.. note::

   Please referes to `Qiime 2 official documentation <https://docs.qiime2.org/2020.6/tutorials/moving-pictures/>`_ for additional information.

``Data download``
-----------------

:Description: This step download data from the ReCaS Swift storage to the MESOS Cluster, for the analysis.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/data_download.json>`_.

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

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_import_demultiplexed.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. warning::

   For demultiplexed data, the **demultiplexing step** is, of course, skipped and the import command is slightly different with respect to the one used in the :doc:`qiime2_se_denoising` section.


``Qiime2: Demux Summarize``
---------------------------

:Description: Run Qiime 2 demux summarize.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.3.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Dada2``
-----------------

:Description: run qiime dada2.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.4.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

	``{{ trunc_len_f }}``: Position at which forward read sequences should be truncated.

	Default value: 150

        Mandatory: YES

        .. warning::

           This value has to be configurable on the LIMS.

        ``{{ trunc_len_r }}``:  Position at which forward read sequences should be truncated.

        Default value: 150

        Mandatory: YES

        .. warning::

           This value has to be configurable on the LIMS.

        ``{{ trim_left_f }}``: Position at which forward read sequences should be trimmed.

	Default value: 13

        Mandatory: YES

	.. warning::

	   This value has to be configurable on the LIMS.

        ``{{ trim_left_r }}``: Position at which reverse read sequences should be trimmed.

        Default value: 13

        Mandatory: YES

        .. warning::

           This value has to be configurable on the LIMS.

``Qiime2: Feature table summary``
---------------------------------

:Description: Run qiime future table summarize.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.5.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Feature table tabulate sequences``
--------------------------------------------

:Description: Run qiime future table tabulate seqs.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.6.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Metadata tabulate``
-----------------------------

:Description: Run qiime to tabulate metadata.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.7.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Create phylogenetic tree``
------------------------------------

:Description: Run qiime to generate a tree for phylogenetic diversity analyses.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.8.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Export outputs``
--------------------------

:Description: Run qiime to export data.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.9.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Biom``
--------

:Description: Run biom to create summary table.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/qiime2_denoising.10.json>`_.

:Input parameters:
        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

   Please note that Biom requires more resources. Currently set to 2 CPUs and 1 GB of memory.


``Prepare data for the upload``
-------------------------------

:Description: Prepare data for the upload on ReCaS Swift. Currently compress outputs to a single tar.gz file.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/prepare_data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

   The output tarball is named: ``qiime2_pe_denoising.tar.gz``

.. note::

   The input ``sample_metadata.tsv`` is included in the output tarball, since it is needed in the next step :doc:`qiime2_pe_diversity`

``Data upload``
---------------

:Description: Upload data on ReCaS Swift.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_pe_denoising/data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

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

   The output file ``qiime2_pe_denoising.tar.gz`` name is specified at the line:

   ::

     { "name": "OUTPUT_FILENAMES", "value": "output_{{ job_run_id }}/qiime2_pe_denoising.tar.gz" },

   and should match the output file name specified in the previous step.

.. note::

   <30 Dec 2020>  - A test version of the same json file, with the possibility to call a test API, which will be replaced with the one provided by the LIMS, is available.

The update version is located in a brach of the GitHub repository, `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/lims-api-call/data-analysis/templates/qiime2_pe_denoising/data_upload_with_lims_call.json>`_.

Three new enviroment variables that need to be added are:

::

  JOB_RUN_ID: "{{ job_run_id }}"
  RECAS_URL_PREFIX: "http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
  LIMS_API_METHOD: "POST"
  LIMS_API_URL: "http://90.147.75.142:5000/lims_api_mock/v1.0/update-output-url"

.. warning::

   ``RECAS_URL_PREFIX`` is mandatory and can't be modified.

.. warning::

   ``LIMS_API_METHOD`` is a LIMS API specific method, currently set to ``POST``.

.. warning::

   ``LIMS_API_URL`` is the LIMS API URL, currently set to the test API URL.
