===================================================================
practice-package : a repo containing practice problems and examples
===================================================================

The repo contains a variety of software examples, questions, and solutions (implemented in python).

.. badges

.. list-table::
    :stub-columns: 1
    :widths: 10 90

    * - docs
      - |docs|
    * - tests
      - |build| |coverage|
    * - package
      - |version| |platform| |downloads|

.. |docs| image:: https://readthedocs.org/projects/practice-package/badge/?version=latest
    :target: `Read the Docs`_
    :alt: Docs

.. |build| image:: https://img.shields.io/azure-devops/build/pyt3r/practice/4
    :alt: Build
    :target: `Azure Pipeline`_

.. |coverage| image:: https://img.shields.io/azure-devops/coverage/pyt3r/practice/4
    :alt: Coverage
    :target: `Azure Pipeline`_

.. |version| image:: https://img.shields.io/conda/v/pyt3r/practice
    :alt: Version
    :target: `Anaconda Cloud`_

.. |platform| image:: https://img.shields.io/conda/pn/pyt3r/practice
    :alt: Platform
    :target: `Anaconda Cloud`_

.. |downloads| image:: https://img.shields.io/conda/dn/pyt3r/practice
    :alt: Platform
    :target: `Anaconda Cloud`_

.. end badges

.. links

.. _conda-build: https://docs.conda.io/projects/conda-build/en/latest/
.. _Azure Pipeline: https://dev.azure.com/pyt3r/practice/_build
.. _Anaconda Cloud: https://anaconda.org/pyt3r/practice
.. _Read the Docs: https://practice-package.readthedocs.io

.. _(mini)conda: https://docs.conda.io/en/latest/miniconda.html
.. _conda-recipe/meta.yaml: conda-recipe/meta.yaml
.. _azure-pipelines.yml: azure-pipelines.yml
.. _https://dev.azure.com/pyt3r/practice/_build: https://dev.azure.com/pyt3r/practice/_build
.. _https://anaconda.org/pyt3r/practice: https://anaconda.org/pyt3r/practice
.. _.readthedocs.yml: .readthedocs.yml
.. _https://practice-package.readthedocs.io: https://practice-package.readthedocs.io
.. _MIT License: LICENSE

.. end links

.. contents:: :local:

Features
##################
Review and practice an array of problems; many of which have been excerpted from the following sources:

* Leet Code
* Cracking the Coding Interview
* ...

The problems cut across the following domains:

* Data Structures
* Dynamic Programming
* Multi Processing
* Design Patterns
* ...


Read the Docs
##################

View and download the complete list of problem statements and solutions from the following Read the Docs page:

`https://practice-package.readthedocs.io`_

Repo Invocation
##################

To invoke a problem from the repo, please use the following instructions.

1. Clone the repo

2. Navigate to the working directory::

    $ cd practice-package

3. Create and activate the practice conda environment::

    $ conda env create --name test-env --file ci/test-env-requirements.yml python=3.7
    $ conda activate test-env

4. View a list of all available problems and examples::

    (test-env) $ python -m ...this is a placeholder...

5. Select an available problem or example and invoke its solution::

    (test-env) $ python -m ...this is a placeholder...

Package Invocation
##################
To invoke a problem from the package, please use the following instructions.

1. Install the package::

    $ conda install practice -c pyt3r

2. View a list of all available problems and examples::

    $ pyt3r-practice list

3. Select an available problem or example and invoke its solution::

    $ pyt3r-practice run <name>

Author
##################

* ``pyt3r``

License
##################

* `MIT License`_
