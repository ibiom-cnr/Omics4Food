Qiime 2 Single End: Diversity
=============================

The `Qiime2 <https://docs.qiime2.org/2020.6/tutorials/>`_ Diversity step for Single End multiplexed data is made by 6 steps.

The input data of this step is the output of the :doc:`qiime2_se_denoising` section.

.. note::

   Please referes to `Qiime 2 official documentation <https://docs.qiime2.org/2020.6/tutorials/moving-pictures/>`_ for additional information.

.. warning::

   This step require the ``sample-metadata.tsv`` original input to be included in denoising outputs. It is one of the inputs of this workflow step.


``Data download``
-----------------

:Description: This step downloads the output of Denoising step from the ReCaS Swift storage to the MESOS Cluster, for the analysis.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/data_download.json>`_.

:Input parameters:

	``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster.

	Mandatory: YES

	.. warning::

           The ``{{ job_run_id }}`` is the same for all the analysis step, in this case the whole *Qiime 2 Diversity* steps.

	``{{ DATA_URL }}``: URL associated to the output of the Denoising step on (ReCaS) Swift.

	Mandatory: YES

	Data URL `example <http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/4AFD40C4DF01B75F35CB90ECFE789D91/81EE76C6F5210A26CE981AD81155B17E/output_977691e6-292d-4910-b150-6fdc719ebcd3/qiime2_se_denoising.tar.gz>`_.

``Qiime2: Create core-metrics-phylogenetic``
--------------------------------------------

:Description: Create core-metrics-phylogenetic.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/qiime2_diversity.1.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Qiime2: Feature classifier with vsearch``
-------------------------------------------

:Description: Feature classifcation with vsearch.

.. warning::

   This step requires more resources. Current default is set to 4 CPU and 6 GB of memory. Please check the resources available on Mesos worker nodes to properly setup this threshold.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/qiime2_diversity.2.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

.. note::

   The following parameters are mandatory for vsearch. The reference reads and the taxonomy are automatically downloaded at run time.

    ::

      REFERENCE_READS: silva-138-99-seqs.qza
      REFERENCE_READS_URL: http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/qiime2-reference-data/silva-138-99-seqs.qza
      REFERENCE_TAXONOMY", "value": "silva-138-99-tax.qza
      REFERENCE_TAXONOMY_URL: http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/qiime2-reference-data/silva-138-99-tax.qza
      P_THREADS: 5

``Qiime2: Metadata tabulate``
--------------------------------------------

:Description: Run qiime to tabulate metadata.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/qiime2_diversity.3.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES

``Prepare data for the upload``
-------------------------------

:Description: Prepare data for the upload on ReCaS Swift. Currently compress outputs to a single tar.gz file.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/prepare_data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previ
ous step.

        Mandatory: YES

.. note::

   The output tarball is named: ``qiime2_se_diversity.tar.gz``

``Data upload``
---------------

:Description: Upload data on ReCaS Swift.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/qiime2_se_diversity/data_upload.json>`_.

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

   The output file ``qiime2_se_diversity.tar.gz`` name is specified at the line:

   ::

     { "name": "OUTPUT_FILENAMES", "value": "output_{{ job_run_id }}/qiime2_se_diversity.tar.gz" },

   and should match the output file name specified in the previous step.
