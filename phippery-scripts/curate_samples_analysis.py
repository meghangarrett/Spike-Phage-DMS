import phippery
from phippery.normalize import enrichment, differential_selection
from phippery.utils import *
import phippery.tidy
import xarray as xr
import numpy as np
import pandas as pd
import pickle
from plotnine import *

path_to_phip_dataset = "../Meghan-Spike-Phage-DMS-Analysis/pipeline-run-10-29-20/phip_data/10-23-20-spike.phip"
xpds = pickle.load(open(path_to_phip_dataset,"rb"))
print(xpds)

participants_chu = [str(par_id) for par_id in range(1,19)]
replicates_chu = set(sample_id_coordinate_subset(xpds, where="participant_ID", is_in=participants_chu))
library_controls = set(sample_id_coordinate_subset(xpds, where="control_status", is_equal_to="library"))
chu_samples = xpds.loc[dict(sample_id=list(replicates_chu.union(library_controls)))]

# compute enrichment seperately for each batch
zero_peptides_batch = {}
enriched_ds = []
for batch, batch_ds in iter_sample_groups(chu_samples, "library_batch"):

    batch_lib_controls =sample_id_coordinate_subset(batch_ds, where="control_status", is_equal_to="library")
    lib_ds = batch_ds.loc[dict(sample_id=batch_lib_controls)]
    lib_cc_df = lib_ds.counts.to_pandas().corr()
    batch_lib_controls = [
        sid for sid, cc in lib_cc_df.iterrows() if (sum(cc)-1)/(len(lib_cc_df)-1) >= 0.5
    ]

    zero_pep = {}
    lib_counts = lib_ds.counts.to_pandas()
    for batch_lib_control in batch_lib_controls:
        batch_lib_counts = lib_counts.loc[:,batch_lib_control]
        zero_pep[batch_lib_control] = set(batch_lib_counts[batch_lib_counts == 0].index.values)
    zero_peptides_batch[batch] = set.intersection(*zero_pep.values())
    print(f"there are {len(zero_peptides_batch[batch])} peptides *NOT* observed across all {batch} library input sequencing samples")

    batch_enriched = enrichment(batch_ds, ds_lib_control_indices=batch_lib_controls, inplace=False)
    enriched_ds.append(batch_enriched)
    
merged_ds = enriched_ds[0].merge(enriched_ds[1])
    
# find all conv patients samples yo keep
conv_replicates_to_keep = []
conv = sample_id_coordinate_subset(
    merged_ds, where="patient_status", is_in=['conv outpatient 30d', 'conv outpatient 60d']
)
conv_ds = merged_ds.loc[dict(sample_id=conv)]
for par_id, par_ds in iter_sample_groups(conv_ds, "participant_ID"):
    print(f"\nAll cross-library replicate correlations for {par_id}")
    at_least_one = False
    replicate_candidates = []
    num_pat_stat = len(get_all_sample_metadata_factors(par_ds, "patient_status"))
    if num_pat_stat < 2: continue
    for pat_st, pat_st_ds in iter_sample_groups(par_ds, "patient_status"):
        print(f"  {pat_st}")
        best_two_correlates = None
        best_corr = 0
        spike1 = sample_id_coordinate_subset(pat_st_ds, where="library_batch", is_equal_to="SPIKE1")
        spike2 = sample_id_coordinate_subset(pat_st_ds, where="library_batch", is_equal_to="SPIKE2")
        pat_st_counts = pat_st_ds["enrichment"].to_pandas()
        for s1_sam in spike1:
            for s2_sam in spike2:
                corr = round(pat_st_counts.loc[:,[s1_sam,s2_sam]].corr().values[0][1],2)
                print(f"    s1: {s1_sam}, s2: {s2_sam} corr: {corr}")
                if corr > best_corr:
                    best_corr = corr
                    best_two_correlates = [s1_sam, s2_sam]
        replicate_candidates.extend(best_two_correlates)
        if best_corr >= 0.5: at_least_one = True
    if at_least_one:
        conv_replicates_to_keep.extend(replicate_candidates)
        print(f"Valid: keeping repicates: {replicate_candidates}")
    else:
        print(f"Not valid set of correlates: Throwing out")

curated_ds = merged_ds.loc[
    dict(
        sample_id = conv_replicates_to_keep #+ healthy_replicates_to_keep
    )
]

print()
print(f"There are {len(conv_replicates_to_keep)//4} conv participants with 2 time points each ")

batch_tidy = []
for batch, batch_ds in iter_sample_groups(curated_ds, "library_batch"):
 
    differential_selection(batch_ds, scaled_by_wt=True, new_table_name="scaled_diff_sel", inplace=True)
    tidy = phippery.tidy.tidy_ds(batch_ds)
    zero_pep_index = tidy[tidy["peptide_id"].isin(zero_peptides_batch[batch])].index.values
    tidy.loc[zero_pep_index, ["counts", "enrichment", "scaled_diff_sel"]] = np.nan
    
    batch_tidy.append(tidy)

both_batch_tidy = pd.concat(batch_tidy)

avg_bio_reps = both_batch_tidy.groupby(
    ["sample_ID", "peptide_id", 
    'sample_type','participant_ID','patient_status',
    'Virus', 'Protein', 'Loc', 'aa_sub', 'is_wt']
).mean().reset_index()

avg_bio_reps.to_csv("Curated_Samples_Phage_DMS_Analysis.csv", index=False, na_rep="NA")
