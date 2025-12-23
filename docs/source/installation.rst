*************
Installation
*************

The Python Library requires Python 3.11 or above.

The Python package can be installed using pip command.

.. code-block:: console

pip install pod_lca

The package also comes with two extras; search mode, openLCA linking. The search mode allows searching the databases and require additional dependencies for natural language processing. OpenLCA provides a pipeline to connect to the OpenLCA API for pre-processing of LCI data.

.. code-block:: console

    pip install pod_lca[search]

or

.. code-block:: console

    pip install pod_lca[olca]

or 

.. code-block:: console
    
    pip install pod_lca[search, olca]

