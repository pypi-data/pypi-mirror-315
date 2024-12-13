import pandas as pd
import numpy as np
import pysam
from collections import defaultdict
from .globals import nucleotide_info, unreliable_regions


def convert_bam_to_rle(bam_files, paired=False):
    """
    convert_bam_to_rle(bam_files, paired=False)

    Converts one or more BAM files into a run-length encoded (RLE) list.

    Parameters:
        bam_files (list): List of paths to BAM files.
        paired (bool): Whether the sequencing data is paired-end.

    Returns:
        dict: A dictionary where keys are sample names, and values are coverage profiles (RLE format).
    """
    coverage_profiles = {}

    for bam_file in bam_files:
        bam = pysam.AlignmentFile(bam_file, "rb")
        sample_name = bam_file.split("/")[-1].replace(".sorted.bam", "")

        coverage = defaultdict(int)

        for read in bam:
            # make sure read has valid alignment positions
            if read.reference_start is not None and read.reference_end is not None:
                if not paired or (paired and read.is_paired):
                    start = read.reference_start
                    end = read.reference_end

                    # incr coverage for all positions in the read range
                    for position in range(start, end):
                        coverage[position] += 1

        rle = []
        prev_value = None
        run_length = 0

        for position in sorted(coverage.keys()):
            value = coverage[position]

            if value == prev_value:
                run_length += 1
            else:
                if prev_value is not None:
                    rle.append((prev_value, run_length))
                prev_value = value
                run_length = 1

        if prev_value is not None:
            rle.append((prev_value, run_length))

        coverage_profiles[sample_name] = rle

    return coverage_profiles


def convert_rle_to_df(covs, unreliable_region_version="1_4_0",
                      unreliable_region_enabled=False, additional_nucleotide_info=pd.DataFrame()):
    """
    convert_rle_to_df(covs, unreliable_region_version="1_4_0",
                      unreliable_region_enabled=False, additional_nucleotide_info=pd.DataFrame())

    Converts RLE coverage profiles into a DataFrame with feature extraction.

    Parameters:
        covs (dict): Coverage profiles in RLE format.
        unreliable_regions (pd.DataFrame): DataFrame of unreliable regions.
        unreliable_region_version (str): Version of unreliable regions (default "1_4_0").
        additional_nucleotide_info (pd.DataFrame): Additional nucleotide info (default empty).

    Returns:
        pd.DataFrame: Feature-rich DataFrame.
    """
    # combine nucleotide info with additional data if given
    combined_nucleotide_info = pd.concat(
        [nucleotide_info, additional_nucleotide_info], ignore_index=True)

    # handle unreliable regions if enabled
    if unreliable_region_enabled:
        if unreliable_region_version == "1_4_0":
            unreliable_region_df = unreliable_regions[unreliable_regions["1_4_0"] == True]
        elif unreliable_region_version == "1_5_0":
            unreliable_region_df = unreliable_regions[unreliable_regions["1_5_0"] == True]
        else:
            raise ValueError(
                "Unsupported unreliable_region_version:", unreliable_region_version)

        for sample, segments in covs.items():
            for seg, coverage in segments.items():
                unreliable_regions_seg = unreliable_region_df[unreliable_region_df["Virus segment"] == seg]
                for _, row in unreliable_regions_seg.iterrows():
                    start, end = row["Start"], row["End"]
                    for pos in range(start, end + 1):
                        if pos < len(coverage):
                            coverage[pos] = 0

    # data frame structure
    column_names = [
        "seg_id", "iso_id", "virus_name", "sample_id",
        "A_percent", "C_percent", "T_percent", "GC_percent",
        "avg_cov", "max_cov", "seg_len",
        "cov_2_percent", "cov_3_percent", "cov_4_percent", "cov_5_percent",
        "cov_6_percent", "cov_7_percent", "cov_8_percent", "cov_9_percent",
        "cov_10_percent"
    ]
    model_data = pd.DataFrame(columns=column_names)

    # process each sample and segment
    for sample, segments in covs.items():
        for seg, coverage in segments.items():
            seg_info = combined_nucleotide_info[combined_nucleotide_info["seg_id"] == seg]
            if seg_info.empty:
                continue

            isolate_id = seg_info["iso_id"].iloc[0]
            virus_name = seg_info["virus_name"].iloc[0]
            seg_length = seg_info["seg_len"].iloc[0]
            a_content = seg_info["A_percent"].iloc[0]
            c_content = seg_info["C_percent"].iloc[0]
            t_content = seg_info["T_percent"].iloc[0]
            gc_content = seg_info["GC_percent"].iloc[0]

            max_cov = max(coverage)
            avg_cov = np.mean(coverage)

            coverage_values = np.array(coverage)
            total_length = len(coverage)

            cov_percentages = {
                f"cov_{i}_percent": sum(coverage_values > i) / total_length for i in range(2, 11)
            }

            new_row = {
                "seg_id": seg,
                "iso_id": isolate_id,
                "virus_name": virus_name,
                "sample_id": sample,
                "A_percent": a_content,
                "C_percent": c_content,
                "T_percent": t_content,
                "GC_percent": gc_content,
                "avg_cov": avg_cov,
                "max_cov": max_cov,
                "seg_len": seg_length,
                **cov_percentages
            }

            model_data = pd.concat(
                [model_data, pd.DataFrame([new_row])], ignore_index=True)

    for col in column_names[4:]:
        model_data[col] = pd.to_numeric(model_data[col], errors='coerce')

    return model_data
