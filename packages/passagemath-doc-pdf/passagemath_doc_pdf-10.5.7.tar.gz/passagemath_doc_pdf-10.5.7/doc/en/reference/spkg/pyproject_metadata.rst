.. _spkg_pyproject_metadata:

pyproject_metadata: PEP 621 metadata parsing
======================================================

Description
-----------

PEP 621 metadata parsing

License
-------

MIT

Upstream Contact
----------------

https://pypi.org/project/pyproject-metadata/


Type
----

standard


Dependencies
------------

- $(PYTHON)
- :ref:`spkg_packaging`
- :ref:`spkg_pip`

Version Information
-------------------

package-version.txt::

    0.8.0

version_requirements.txt::

    pyproject-metadata


Equivalent System Packages
--------------------------

.. tab:: Fedora/Redhat/CentOS

   .. CODE-BLOCK:: bash

       $ sudo yum install python3-pyproject-metadata 


.. tab:: Gentoo Linux

   .. CODE-BLOCK:: bash

       $ sudo emerge dev-python/pyproject-metadata 



If the system package is installed and if the (experimental) option
``--enable-system-site-packages`` is passed to ``./configure``, then ``./configure``
will check if the system package can be used.

