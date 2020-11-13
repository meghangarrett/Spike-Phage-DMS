#Spike Phage-DMS library design

##Contents of this directory
This directory contains the sequences and scripts used to generate the Spike Phage-DMS library used in this study. 

##Generating Spike Phage-DMS peptide sequences
To computationally design the oligonucleotide sequences used to generate the Spike Phage-DMS library, I performed the following two steps:

**1. Optimize sequences**
First, I took fasta files containing the sequences of the proteins I would like to generate oligos. I took the entire sequence of S1 and S2 from the Wuhan Hu-1 strain of SARS-CoV-2. I additionally generated sequences in the background of the D614G mutation, and called this S1alt. These files are located within the `sequences` directory:

*`SARSCoV2_S1_seq.fasta`
*`SARSCoV2_S2_seq.fasta`
*`SARSCoV2_S1alt_seq.fasta`

These sequences served as the input for the `DNAChisel_spike_optimization.py` script within the `optimization` directory. This script was modified from the [DnaChisel](https://github.com/Edinburgh-Genome-Foundry/DnaChisel) library. The optimized sequence outputs were made into new .fasta files, also within the `sequences` directory:

* `SARSCoV2_S1_dna_opt.fasta`
* `SARSCoV2_S2_dna_opt.fasta`
* `SARSCoV2_S1alt_dna_opt.fasta`

**2. Generate oligos**
Phage-DMS libraries consist of oligos encoding overlapping peptides spanning the protein of interest where the middle residue for each oligo has been randomized to encode any of the 20 amino acids. A complete library thereby consists of 20 oligos per site in the protein of interest. Additionally, the oligos are 93 nucleotides long and each oligo advances by 3 nucleotides (1 amino acid) compared to the previous oligo.

The optimized DNA sequences generated above serve as the input for the script named `spike_oligos_040420.py`. This code was originally written by Katharine H.D. Crawford in the Bloom lab, and was modified for use with the spike library.

The script first checks to see that the input nucleotide sequence matches the original protein sequence. These protein .fasta files can be found within the `sequences` directory:

* `SARSCoV2_S1_prot.fasta`
* `SARSCoV2_S2_prot.fasta`
* `SARSCoV2_S1alt_prot.fasta`

The parameters `oligo_length` and `tile` variables defined in the beginning of each script specify the desired length of the oligos (ex: 20) and the length of tiling (ex: 3). These scripts also add on the necessary adaptor sequences for cloning these oligos into the [T7 Select phage system](https://www.emdmillipore.com/US/en/product/T7Select10-3-Cloning-Kit,EMD_BIO-70550#anchor_USP).
Additionally, user-specified linker sequences are added to the first and last oligos ordered to ensure the first and last sites to be mutated are in the middle of those oligos. 

The scripts also use synonymous substitution to remove any sequences matching the restriction sites used for cloning. For the T7 Select system, those restriction sites are `GAATTC` and `AAGCTT` matching the motifs for the EcoRI and HindIII restriction enzymes, respectively.The sequences to remove from the designed oligos are referred to as `avoid_motifs` and can be specified in the beginning of the scripts.

Finally, since most peptides are identical between S1 and S1alt (except for those spanning site 614), the script removes all duplicate sequences, so each oligo ordered is unique.

The output for each script is a `.txt` file with the columns `Virus`, `Rand_Loc`, `Rand_AA`, and `Oligo`. 
The `Virus` column specifies the virus strain for which the oligos are designed; `Rand_Loc` specifies what residue is in the middle of the oligo and, thus, being randomized; `Rand_AA` specifies what amino acid is encoded in this middle position; and `Oligo` is the final oligo sequence including necessary adaptors.
These `.txt` files are output to an `oligos` directory:

* `SARSCoV2_Spike_master_oligos.txt`

To run these scripts and re-make the oligos we designed, clone this repo and run each script from the command line (for example, use the command: `spike_oligos_040420.py` to re-make the spike oligos).
These scripts require Python version 3.6 and pandas.
To facilitate running these scripts, we have also included an `envrionment.yml` file.
This can be used to create a conda environment compatible with running these scripts for library design using the command: `conda env create -f environment.yml`.
