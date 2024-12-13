# iimi: identifying infection with machine intelligence

`iimi` is a Python package designed for plant virus diagnostics using high-throughput genome sequencing data. It provides tools for converting BAM files into coverage profiles, processing viral genomic data, and predicting viral infections in plant samples.

## Installation

```bash
pip install iimi
```


## Usage

```python
import iimi
```

## Data Preprocessing

```python
# convert BAM files to coverage profiles
bam_files = ["path/to/sample1.sorted.bam", "path/to/sample2.sorted.bam"]
example_cov = iimi.convert_bam_to_rle(bam_files)

# convert coverage profiles to a feature-extracted DataFrame
rle_data = {
    "sample1": {"seg1": [1, 2, 3, 0, 0, 4], "seg2": [0, 0, 0, 1, 1, 2]},
    "sample2": {"seg3": [2, 3, 4, 5, 0, 1]},
}

additional_info = pd.DataFrame({
    "virus_name": ["Virus4"],
    "iso_id": ["Iso4"],
    "seg_id": ["seg4"],
    "A_percent": [40],
    "C_percent": [20],
    "T_percent": [20],
    "GC_percent": [20],
    "seg_len": [800],
})

df = iimi.convert_rle_to_df(example_cov, additional_nucleotide_info=additional_info)
```

## Unreliable Regions

### High Nucleotide Content Regions

```python
virus_info = {
    "seg1": "ATGCGATCGATCGATCGTACGATCGATCGATCGATCGTACGATCG",
    "seg2": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
}

# identify regions with high GC content
high_gc = create_high_nucleotide_content(
    gc=0.4, a=0.0, window=10, virus_info=virus_info
)
# identify regions with high A content
high_a = create_high_nucleotide_content(
    gc=0.0, a=0.8, window=10, virus_info=virus_info
)
```

### Mappability Profile

```python
# generate mappability profile from host or virus BAM files
result = create_mappability_profile(
    path_to_bam_files="path/to/bam/files",
    virus_info=virus_info,
    window=10
)
```

## Visualizing Coverage Profiles

```python
covs = {
    "sample1": {
        "seg1": [20, 30, 50, 60, 80],
        "seg2": [15, 25, 45, 55, 75],
    }
}
virus_info = {
    "seg1": "ACGT" * 250,
    "seg2": "TGCA" * 250,
}

# plot coverage of segments without unreliable regions
plot_cov(
    covs,
    legend_status=True,
    nucleotide_status=True,
    virus_info=virus_info,
    unreliable_regions=None,
)
```

## Predicting Plant Sample(s)

### Using Pre-trained Models

```python
# Predict using pre-trained XGBoost model
predictions = iimi.predict_iimi(newdata=df, method='xgb')
```

### Training a Custom Model

```python
# Split data into training and testing sets
train_x = df[df['sample_id'].isin(train_names)]
test_x = df[~df['sample_id'].isin(train_names)]

# Prepare labels
train_y = [example_diag.loc[row['seg_id'], row['sample_id']] for _, row in train_x.iterrows()]

# Train custom model
custom_model = iimi.train_iimi(train_x=train_x, train_y=train_y)

# Predict using custom model
custom_predictions = iimi.predict_iimi(newdata=test_x, trained_model=custom_model)
```

## References

- H. Ning, I. Boyes, Ibrahim Numanagić, M. Rott, L. Xing, and X. Zhang, “Diagnostics of viral infections using high-throughput genome sequencing data,” Briefings in Bioinformatics, vol. 25, no. 6, Sep. 2024, doi: https://doi.org/10.1093/bib/bbae501.
- Grigorii Sukhorukov, M. Khalili, Olivier Gascuel, Thierry Candresse, Armelle Marais-Colombel, and Macha Nikolski, “VirHunter: A Deep Learning-Based Method for Detection of Novel RNA Viruses in Plant Sequencing Data,” Frontiers in bioinformatics, vol. 2, May 2022, doi: https://doi.org/10.3389/fbinf.2022.867111.
