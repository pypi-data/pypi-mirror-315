from opennano.qc import CountsQC

dcc_directory = "/Users/niamhcallinankeenan/Downloads/dcc_files/"
pkc_file = "/Users/niamhcallinankeenan/Downloads/Mm_R_NGS_WTA_v1.0.pkc"
metadata_file = "/Users/niamhcallinankeenan/Downloads/GSE239336_family.soft"

# Initialize the CountsQC object
qc = CountsQC(
    dcc_directory=dcc_directory,
    pkc_file=pkc_file,
    metadata_file=metadata_file
)

# Run QC checks and get filtered data
filtered_adata, negative_probes_adata = qc.run_all_checks(return_negative_probes=True)

# Print details of filtered data
print("\nFiltered AnnData Object:")
print(filtered_adata)

# Print details of negative probes data
print("\nNegative Probes AnnData Object:")
print(negative_probes_adata)

# Save filtered data to files (optional)
filtered_adata.write("filtered_adata.h5ad")
negative_probes_adata.write("negative_probes_adata.h5ad")

print("\nFiltered AnnData and negative probes AnnData saved as H5AD files.")
