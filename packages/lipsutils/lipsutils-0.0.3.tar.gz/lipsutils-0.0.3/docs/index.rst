PrincetonLIPS Computing 
=======================

This site contains a number of useful resources for using Princeton research computing systems, our internal 
lab hosts (LIPS Private Compute or LPC), and generic Python utilities that seem to be re-implemented across many 
research projects. 
In addition, we provide a number of tutorials that cover common challenges in research. 

To use our Python utilities, simply install the package with: 

.. code-block:: console 

   $ pip install lipsutils

.. toctree::
   :maxdepth: 1
   :caption: Princeton Research Clusters

   cluster-utils/ionic
   cluster-utils/shared_storage
   cluster-utils/apptainer
   cluster-utils/slurm

.. toctree:: 
   :maxdepth: 1
   :caption: LIPS Private Compute (LPC)

   lpc/connecting_via_ssh
   lpc/containers
   lpc/gpu
   lpc/nfs
   lpc/admin
   lpc/faq

.. toctree:: 
   :maxdepth: 1
   :caption: Python Utilities 

   python-utils/profiling
   python-utils/string_formatting
   python-utils/api

.. toctree:: 
   :maxdepth: 1
   :caption: Tutorials

   tutorials/docker
   tutorials/gpu_profiling

Support 
-------

.. note:: 

   This is an internally managed project with minimal maintenance. 
