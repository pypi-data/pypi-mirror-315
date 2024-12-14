=======
History
=======


0.1.20 (2024-12-13)
-------------------

- Bump docker version


0.1.19 (2024-03-19)
-------------------

- Try again to release.


0.1.18 (2024-03-19)
-------------------

- Try PyPi release with adjusted GA workflow.


0.1.17 (2024-03-19)
-------------------

- Retry release.


0.1.16 (2024-03-19)
-------------------

- Try to release to PyPi


0.1.15 (2024-03-19)
-------------------

- Filter Kubernetes job: need to start with "simulation-"


0.1.14 (2023-08-29)
-------------------

- Added option for getting job status in Kubernetes backend.


0.1.13 (2023-07-10)
-------------------

- Kubernetes job should only run once.

- Allow size limit on `EmptyDirVolumeSource`.


0.1.12 (2023-03-06)
-------------------

- Secret mount options was incorrect.


0.1.11 (2023-03-03)
-------------------

- Allow more Kubernetes mounts options.


0.1.10 (2023-03-01)
-------------------

- Enable `annotations` and `resources` (limits/requests).


0.1.9 (2023-02-13)
------------------

- Added shared `EmptyDirVolumeSource` with name "shared-data" between simulation and scheduler container.


0.1.8 (2023-02-10)
------------------

- Drop `scheduler-worker` container in Kubernetes.


0.1.7 (2022-12-07)
------------------

- Need to use V1DeleteOptions from openapi


0.1.6 (2022-09-19)
------------------

- Automically remove pod under job.

- Add the option of opening a debug port for the docker backend.


0.1.5 (2022-06-24)
------------------

- Added `imagePullSecrets`, `NodeAffinity` and `Resources` options for Kubernetes simulation `Job`.


0.1.4 (2022-06-17)
------------------

- Kubernetes backend `container_list()` needs to return simulation-id's only.


0.1.3 (2022-06-15)
------------------

- Changes in Kubernetes backend after testing.


0.1.2 (2022-05-09)
------------------

- Added kubernetes support.


0.1.1 (2022-04-15)
------------------

- Major refactor: carriers now are available via backend modules.


0.0.19 (2022-04-13)
-------------------

- Don't pick SENTRY settings up from simple-settings. Should be given via `up` function `envs` parameter.


0.0.18 (2021-12-21)
-------------------

- Updated pypi token.


0.0.17 (2021-12-21)
-------------------

- Dynamically set container "LOG_LEVEL" via env parameter.


0.0.16 (2021-09-03)
-------------------

- Disable model mount when `gridadmin_download_url` and `tables_download_url` parameters
  are both given.


0.0.15 (2021-07-27)
-------------------

- Added options for passing `gridadmin_download_url` and `tables_download_url` parameters
  to the `up()` function


0.0.14 (2021-06-09)
-------------------

- Removed threedi-api-client as requirement.

- Added a pypi release pipeline to github action workflow.


0.0.13 (2020-10-13)
-------------------

- Added the 'clean_up_files' arg to 'up()' function.


0.0.12 (2020-08-11)
-------------------

- Bumped docker version

0.0.11 (2020-05-15)
-------------------

- Added the 'max_rate' arg to `up()` function.


0.0.10 (2020-04-20)
-------------------

- All MarathonApp args must be strings.


0.0.9 (2020-04-20)
------------------

- Session memory argument `mem` must be string for marathon strange enough.


0.0.8 (2020-04-16)
------------------

- Added the `pause_timeout` arg to the `up()` function.


0.0.7 (2020-02-19)
------------------

- Strip the 'simulation-' prefix when querying for the docker container_list to
  ensure uniformity between all carriers.


0.0.6 (2020-01-27)
------------------

- Use a generic `envs` arg that will set the container env variables.

- Added args `sim_uid, sim_ref_datetime, end_time, duration and start_mode` to
  container CMD.


0.0.5 (2020-01-17)
------------------

- Use generic marathon constraints settings.


0.0.4 (2019-12-19)
------------------

- Added support for host and ip lookups.


0.0.3 (2019-12-19)
------------------

- Catch also `ImportErrors` for simple settings.


0.0.2 (2019-12-19)
------------------

- Rename env var only_initialize to scheduler_action.


0.0.1 (2019-12-19)
------------------

* First release on PyPI.
