#########
MADCUBApy
#########

|PyPI Status| |Documentation Status|

*NOTE: This package is in its first test versions and should not be used in its
current state.*

``madcubapy`` is a package developed to work with MADCUBA products to quickly
access their data in python. 

`MADCUBA <https://cab.inta-csic.es/madcuba/>`_ is a software developed in the
spanish Center of Astrobiology (CSIC-INTA) to analyze astronomical datacubes,
and is built using the ImageJ infrastructure. This tool will not work with any
other ImageJ program.

Instead of writing history into new fits cards in the header of the file,
MADCUBA creates a history file named *_hist.csv*. With ``madcubapy`` we can
read fits files with this external history information into a single object in
python.


Installation
============

Install from PyPI with:

.. code-block:: bash

    pip install madcubapy


.. |PyPI Status| image:: https://img.shields.io/pypi/v/madcubapy
    :target: https://pypi.org/project/madcubapy
    :alt: PyPI Status

.. |Documentation Status| image:: https://img.shields.io/readthedocs/madcubapy/latest.svg?logo=read%20the%20docs&logoColor=white&label=Docs
    :target: https://madcubapy.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status