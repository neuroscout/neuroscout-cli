Welcome to Neuroscout-CLI's documentation!
==========================================

.. image:: neuroscout-logo.svg
  :width: 400
  :alt: Neuroscout Logo

The Neuroscout Command Line Interface (Neuroscout-CLI) allows you to easily execute analyses created on neuroscout.org. 
Neuroscout-CLI automatically fetches analysis dependencies (including data, and analysis specifications), 
fits a GLM model to the BIDS dataset, and produces shareable reports of the results.

Neuroscout-CLI uses `FitLins <https://github.com/poldracklab/fitlins>`_ to estimate linear models using the BIDS model specification.

Check out the :doc:`usage` section for further information, including
how to :ref:`installation` the project.

.. note::

   If you are new to the Neuroscout project, visit the `Neuroscout <https://neuroscout.org>`_ website and 
   the official `Neuroscout Docs <https://neuroscout.org/docs>`_ for a general introduction.

Contents
--------

.. toctree::
   
   installation
   usage
   outputs