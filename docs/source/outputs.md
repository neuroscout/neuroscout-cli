# Outputs

 __Neuroscout-CLI__ creates an output directory, with the name `neuroscout-ANALYSIS_ID` which contains both the inputs to the analysis (`sourcedata`), as well as the outputs of execution (`fitlins`).

Below is an example output directory.

```
  /home/user/out/neuroscout-ANALYSIS_ID
    └───sourcedata
    │   │
    │   └───DATASET
    │       └───fmriprep
    │   └───bundle
    │       └───events
    │       │   model.json
    │       │   ...
    └───fitlins
        └───sub-01
        └───reports
        |   dataset_description.json
        |   ...
    └─── options.json
```

## sourcedata directory

In the `sourcedata` folder, there are two folders: one contaning the preprocessed fMRI inputs (the name of the folder is the name of the Dataset), and `bundle` which contains the contents of the analysis bundle for your `ANALYSIS_ID`.

.. note::

   If specified `--download-dir` at run time (reccomended; to cache the input directory in a common directory), you will not find the input
   data directory here. 

Within the `bundle` directory you will find the event files and BIDS Stats Model (`model.json`) that are used to generate the design matrix for your analysis. 

.. note::

   For more information about __BIDS Stats Models__, take a look at the [official documentation](https://bids-standard.github.io/stats-models/).

## fitlins directory

Within the `fitlins` directory, you will find the BIDS Derivatives compliant outputs from [FitLins](https://github.com/poldracklab/fitlins) 
execution. 

Within the `reports` folder, you can view interactive HTML reports, including a summary of your model, design matrices, and quality control visualizations.

## Uploading to NeuroVault

By default, NeuroScout will upload all group and subject level results to NeuroVault, and update the NeuroScout API with the corresponding meta-data. You are free to opt out by specifiying ` --no-upload` at runtime.