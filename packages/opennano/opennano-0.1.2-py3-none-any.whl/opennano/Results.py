from opennano.io import GeoMxProcessor
import anndata as ad
from opennano.qc import CountsQC
import matplotlib.pyplot as plt
import seaborn as sns

# Define file paths
dcc_directory = "/Users/charalamposanagnostakis/git/opennano/NASA_data/dcc_files"  # Replace with the path to your `.dcc` files directory
pkc_file = "/Users/charalamposanagnostakis/git/opennano/NASA_data/Mm_R_NGS_WTA_v1.0.pkc"  # Replace with the path to your `.pkc` file
metadata_file = "/Users/charalamposanagnostakis/git/opennano/NASA_data/GSE239336_family.soft"  # Replace with the path to your metadata file

# Instantiate the processor
processor = GeoMxProcessor(dcc_files=dcc_directory, pkc_file=pkc_file, metadata_file=metadata_file)

# Process the data and create the AnnData object
adata = processor.process()

# Check the resulting AnnData object
if adata is not None:
    print(f"AnnData object created with shape: {adata.shape}")
    print(f"Observations (obs): {adata.obs.head()}")
    print(f"Variables (var): {adata.var.head()}")
else:
    print("No AnnData object was created.")

qc = CountsQC(adata = adata)
# Generate QC plots
qc.plot_qc_results()



