Data quality asssurance
=======================

The quality assurance workflow is based on `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ and is made by 4 steps.

``Data download``
-----------------

:Description: This step download data from the ReCaS Swift storage to the MESOS Cluster, for the analysis.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/data_download.json>`_.

:Input parameters:

	``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster.

	Mandatory: YES

	.. warning::

           The ``{{ job_run_id }}`` is the same for all the analysis step, in this case the whole *Quality assurance* step.

	``{{ DATA_URL }}``: URL associated to the data uploaded on (ReCaS) Swift.

	Mandatory: YES

	Data URL `example <http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/4AFD40C4DF01B75F35CB90ECFE789D91/81EE76C6F5210A26CE981AD81155B17E/test-data.tar.gz>`_


``Fastqc``
----------

:Description: Quality assurance step based on `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/fastqc.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES


``Prepare data for the upload``
-------------------------------

:Description: Prepare data for the upload on ReCaS Swift. Currently compress outputs to a single tar.gz file.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/prepare_data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previ
ous step.

        Mandatory: YES

``Data upload``
---------------

:Description: Upload data on ReCaS Swift.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/data_upload.json>`_.

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

   <30 Dec 2020>  - A test version of the same json file, with the possibility to call a test API, which will be replaced with the one provided by the LIMS, is available.

The update version is located in a brach of the GitHub repository, `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/lims-api-call/data-analysis/templates/fastqc/data_upload_with_lims_call.json>`

Three new enviroment variables need to be added:

::

  RECAS_URL_PREFIX: "http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
  LIMS_API_METHOD: "POST"
  LIMS_API_URL: "http://90.147.75.142:5000/lims_api_mock/v1.0/update-output-url"

.. warning::

   ``RECAS_URL_PREFIX`` is mandatory and can't be modified.

.. warning::

   ``LIMS_API_METHOD`` is a LIMS API specific method, currently set to ``POST``.

.. warning::

   ``LIMS_API_URL`` is the LIMS API URL, currently set to the test API URL.


Paired End version
------------------

.. note::

   For FastQC paired end and single end workflows are the same. 

Only two variable has to be changed:

::

  { "name": "DATA_DIR", "value": "emp-paired-end-sequences" },

and, of course, the data URL.

The Json files for Paired End analysis can be found `here <https://github.com/ibiom-cnr/Omics4Food/tree/master/data-analysis/templates/fastqc/fastqc_pe>`_ as reference.

