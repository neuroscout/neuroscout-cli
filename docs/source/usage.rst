Usage
=====

**Neuroscout-CLI** executes models built using Neuroscout by acting as a lightway layer that fetches 
the data required for the model, and runs it using `FitLins <https://github.com/poldracklab/fitlins>`_.
After the model is run, the results are outputs as BIDS Derivatives, and uploaded to NeuroVault (by default).

Containerized execution
-----------------------
Note that depending on your :doc:`installation` method, the exact command will differ.

For **Docker**, you must prepend the command with ``docker run -it`` and map relevant
local directories from the host to the container using ``-v``. Instead of ```euroscout``, the command 
will be ``neuroscout/neuroscout-cli`` to reference a specific image. For example::

   docker run -it -v LOCAL_DIR:OUT_DIR neuroscout/neuroscout-cli run ANALYSIS_ID OUT_DIR

For **Singularity**, you must prepend the command with ``singularity run --cleanenv`` and refer to
a specific pre-downloaded image::

   singularity run --cleanenv neuroscout-cli-<version>.simg ANALYSIS_ID OUT_DIR

For a complete guide, see :doc:`neuroscout:cli/docker` and :doc:`neuroscout:cli/singularity` in the offical `Neuroscout Docs <https://neuroscout.org/docs>`_.

Command-Line Arguments
-----------------------
.. click:: neuroscout_cli.cli:main
   :prog: neuroscout
   :nested: full

Optional FitLins arguments
--------------------------

Under the hood Neuroscout-CLI uses `FitLins <https://github.com/poldracklab/fitlins>`_ to execute the model.
As such, Neuroscout-CLI will forward any arguments passed as `[FITLINS_OPTIONS]` to __FitLins__. 

For details on valid FitLins arguments, please see :doc:`fitlins:usage`.