Omics4Food: data analysis
=========================

Mesos CURL
----------

The parent job (the first analysis step, is always the data download).

```
curl -k -L -H 'Content-Type: application/json' -X POST -d '@parent.json' https://90.147.75.16:4443/v1/scheduler/iso8601 -u admin:******
```

The dependent jobs, i.e. all the following analysis steps, are called with:

```
curl -k -L -H 'Content-Type: application/json' -X POST -d '@child.json' https://90.147.75.16:4443/v1/scheduler/dependency -u admin:******
```

To allow these steps to be run on MESOS, the parent job MUST always be correctly submitted and run on MESOS. This has to be checked. Please, check if the parent job return 200 status code. If the parent is not submitted all children will FAIL.
