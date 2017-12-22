Welcome to CS410-Project: Address Tagging and Matching's documentation!
=======================================================================

Project Goal
------------
Address data in CRM (customer relationship management) tools are typically of poor quality.  The poor quality makes it challenging and time consuming to report on a customer base, conduct customer segmentation analyses, etc.  Due to this poor quality and lack of controls, databases typically contain tons of duplicate records/addresses, incomplete addresses, and incorrect addresses/information.  Data stewards/analysts are often tasked with manually fixing the poor quality data, an efficient and time-consuming process.

Our project focused on creating a suite of tools to parse, tag, standardize, and compare lists of addresses as an alternative to expensive Master Data Management and similar systems.  The goal is to be able to use our tools to find duplicates within a single list of addresses as well as across 2 separate address lists.  In essence, our tools are designed to help master the address data so that a database doesn't have duplicates/triplicates, etc.


Project Location
----------------
The actual code files are saved in GitHub_

.. _GitHub: https://github.com/aberk104/CS410-Project


Pre-Requisites
--------------
The various methods within the address_compare project have been built using Python 3.x.  In addition, the following Python packages will need to be installed in order to run the various methods:

- python-crfsuite

::

    pip install python-crfsuite

- editdistance

::

   pip install editdistance


Additional Python Packages
--------------------------
In addition to the pre-requisites listed above, the various code files also utilize the following python packages. These should be part of a default python build using Anaconda; if not using Anaconda, these may need to be installed as well:

- collections

- itertools

- json

- pandas

- pickle

- pkg_resources

- random

- re

- scikit-learn

- scipy

- sklearn.metrics (should be part of scikit-learn)


Guide
-----

.. toctree::
   :maxdepth: 3

   address_compare


* Example_: The master_file.ipynb is a pre-built parameterized "program" that can be used to access the aggregate_functions.py file to parse, tag, and match addresses.

.. _Example: https://github.com/aberk104/CS410-Project/blob/master/master_file.ipynb


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
