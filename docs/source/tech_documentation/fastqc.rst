Data quality asssurance
=======================

The quality assurance workflow is based on `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_ and is made by 4 steps.

``Data download``
-----------------

:Description: This step download data from the ReCaS Swift storage to the MESOS Cluster, for the analysis.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/fastqc_pe/data_download.json>`_.

:Input parameters:

	``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster.

	Mandatory: YES

	.. warning::

           The ``{{ job_run_id }}`` is the same for all the analysis step, in this case the whole *Quality assurance* step.

	``{{ DATA_URL }}``: URL associated to the data uploaded on (ReCaS) Swift.

	Mandatory: YES

	Data URL `example <http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20/4AFD40C4DF01B75F35CB90ECFE789D91/81EE76C6F5210A26CE981AD81155B17E/qiime_pe.tar.gz>`_


``Fastqc``
----------

:Description: Quality assurance step based on `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`_.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/fastqc_pe/fastqc.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES


``Prepare data for the upload``
-------------------------------

:Description: Prepare data for the upload on ReCaS Swift. Currently compress outputs to a single tar.gz file.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/fastqc_pe/prepare_data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previ
ous step.

        Mandatory: YES

``Data upload``
---------------

:Description: Upload data on ReCaS Swift.

:Json file: The json file is located `here <https://raw.githubusercontent.com/ibiom-cnr/Omics4Food/master/data-analysis/templates/fastqc/fastqc_pe/data_upload.json>`_.

:Input parameters:

        ``{{ job_run_id }}``: Unique identifier of the run on MESOS: It is used to identfy the parent and dependent jobs and to create the working directory on MESOS cluster. Must be the same of the previous step.

        Mandatory: YES


The following parameters are mandatory for each step requiring data Upload to contact the LIMS API.

``LIMS_USERNAME`` and ``LIMS_PROJECT_ID``: Username and project-ID to identify the ReCaS Swift directory and upload the data, making them available to download.

The other parameters are needed to contact the LIMS API.

::

  LIMS_IDTENANT: "00000000-0000-0000-0000-000000000000
  LIMS_PASSWORD: "*****"
  LIMS_NOMESERVER: "*****"
  LIMS_API_METHOD: "POST"
  LIMS_API_URL: "*****"

.. warning::

  ``LIMS_API_METHOD`` is a LIMS API specific method, currently set to ``POST`` and should not be changed.

The following parameters are mandatory for each step requiring data Upload on ReCaS Swift and should not be changed.

::

  RECAS_URL_PREFIX: "http://cloud.recas.ba.infn.it:8080/v1/AUTH_cf2db2690546474f889e300445b3bf20"
  OUTPUT_PROTOCOL: swift+keystone
  OUTPUT_ENDPOINT: https://cloud.recas.ba.infn.it:5000/v3
  OS_IDENTITY_API_VERSION: 3
  OS_PROJECT_DOMAIN_ID: default
  OUTPUT_REGION: recas-cloud
  OUTPUT_TENANT: *****
  OUTPUT_USERNAME: *****
  OUTPUT_PASSWORD: *****

.. warning::

   ``RECAS_URL_PREFIX`` is mandatory and can't be modified.
