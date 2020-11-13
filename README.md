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

### library design

The pan-human CoV was created using a script that can also be found 
[here](https://github.com/jbloomlab/phipseq_oligodesign) 
and was written by Kate H.D Crawford in the Bloom lab.
The fasta files needed to create the library are located in the library-design
directory. simply run

```
cd library-design
tar -xvf prot_files.tar
```

Next, to create the library, make sure your environment is activated then

```
python phip_seq_oligodesign.py prot_files out_dir protein
```
