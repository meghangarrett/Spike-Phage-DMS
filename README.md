# Spike Phage DMS Repo

This repository contains all necessary code for analysis described in <>
The repository contains the code for a [Nextflow](https://www.nextflow.io/docs/latest/getstarted.html) pipeline,
dubbed [phip-flow](https://github.com/matsengrp/phip-flow), along with all analysis and plotting code.

### Abstract

TODO

### Analysis environment

The library design script and analysis notebooks contain all code needed to run analysis 
for the manuscript using custom code from 
[phippery](https://github.com/matsengrp/phippery) along with a few other popular python packages.

We suggest using [conda](https://www.anaconda.com/) to create the environment like so:
```
conda env create -f environment.yml && conda activate pan-cov-manuscript
mkdir -p _ignore && cd _ignore
git clone git@github.com:matsengrp/phippery.git
cd phippery && python setup.py install --user && cd ../../
```

### Running the alignment pipeline

All raw fastq files for the samples can be obtained upon request and will be provided in a tarball, `NGS.tar`.
Place this file in the `alignment-pipeline/` directory and run `tar -xvf NGS.tar` to produce the `NGS` Directory.

The pipeline can be run anywhere with `Nextflow` and `Docker` (or `Singularity`) installed. 
The scripts inside the directory provide an example of how to run the pipeline on our local Fred Hutch cluster, gizmo.
To run on you're own compute system: 
(1) Create a config file similar to `nextflow.gizmo.config` that describes the job submission parameters and partitions you would like to use.
(2) Create a run script using `run_gizmo_cat.sh` as a template with your own paths for temporary directories and modules you might need to load.
More instruction on creating config files can be found [here](https://www.nextflow.io/docs/latest/config.html#configuration-file)

After the pipeline finishes merging all counts from the alignments,
the output of the pipeline is a file, `phip_data/pan-cov-ds.phip`
containing sample and peptide metadata tied to the raw counts matrix like so:

<p align="center">
  <img src="figures/Xarray.png" width="350">
</p>

With the colored columns representing coordinate dimensions and the grey squares representing data arrays
organized by respective shared dimensions.
