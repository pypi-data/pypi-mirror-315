import numpy as np
from param import output

from opennano.qc import CountsQC
import os
import anndata as ad
import pandas as pd
import tempfile
import scipy.sparse as sp

def test_qc_checks():
    # Example paths
    dcc_directory = "/Users/charalamposanagnostakis/git/opennano/NASA_data/dcc_files/"
    pkc_file = "/Users/charalamposanagnostakis/git/opennano/NASA_data/Mm_R_NGS_WTA_v1.0.pkc"
    metadata_file = "/Users/charalamposanagnostakis/git/opennano/NASA_data/GSE239336_family.soft"

    # Initialize QC
    qc = CountsQC(
        dcc_directory=dcc_directory,
        pkc_file=pkc_file,
        metadata_file=metadata_file
    )
    
    # Ensure the AnnData object is created
    assert qc.adata is not None, "AnnData object was not created"
    print("AnnData shape:", qc.adata.shape)
    print("AnnData var head:\n", qc.adata.var.head())
    print("AnnData obs head:\n", qc.adata.obs.head())
    
    # Run all checks
    try:
        qc.run_all_checks()
    except Exception as e:
        assert False, f"QC checks failed with error: {e}"

def test_write_function():
    """
    A Unit test for "write" function in the CountQC class.
    Ensures the path is valid, directories exist, and overwriting works correctly.
    """
    # Create a temporary directory and file for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = os.path.join(temp_dir, "test_output.h5ad")
        non_existing_folder = os.path.join(temp_dir, "non_existing_folder")
        invalid_path_file = os.path.join(non_existing_folder, "test_invalid.h5ad")

        # Create a dummy Anndata object for testing
        adata = ad.AnnData(
            X=np.array([[1, 2], [3, 4]]),
            obs=pd.DataFrame({
                "obs_names": ["obs1", "obs2"],
                "SystematicName": ["NegProbe-WTX-1", "Gene-1"]
            }, index=["obs1", "obs2"]),
            var=pd.DataFrame({"var_names": ["var1", "var2"]}, index=["var1", "var2"])
        )

        # Initialize the CountQC with dummy Anndata object
        qc = CountsQC(adata = adata)

        # Test overwriting in existing file
        try:
            qc.write(filename = output_file)
            assert os.path.exists(output_file), "File was not overwritten in existing file"
        except Exception as e:
            assert False, f"Overwriting file failed: {e}"

        # Test writing in non-existing folder
        try:
            qc.write(filename = output_file)
            assert os.path.exists(os.path.dirname(temp_dir)), "Directory does not exist"
        except Exception as e:
            assert False, f"Writing to an existing directory failed: {e}"

        # Test writing to a non-existing folder
        try:
            qc.write(filename=invalid_path_file)
            assert False, "Writing to a non-existing folder should have raised an error"
        except FileNotFoundError as e:
            assert str(e).startswith("The directory"), f"Unexpected error message: {e}"

        # Ensure the non-existing folder still does not exist
        assert not os.path.exists(non_existing_folder), "The non-existing folder was unexpectedly created"

if __name__ == "__main__":
    # Run the tests
    test_qc_checks()
    test_write_function()
    print("All tests passed.")