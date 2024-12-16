
import pytest
from opennano.io import GeoMxProcessor


@pytest.fixture
def setup_real_data():
    """
    Fixture to set up paths to actual data files.
    """
    dcc_directory = "/Users/niamhcallinankeenan/Downloads/dcc_files/"
    pkc_file = "/Users/niamhcallinankeenan/Downloads/Mm_R_NGS_WTA_v1.0.pkc"
    metadata_file = "/Users/niamhcallinankeenan/Downloads/GSE239336_family.soft"

    return {
        "dcc_directory": dcc_directory,  # Pass the directory, not a file path
        "pkc_file": pkc_file,
        "metadata_file": metadata_file
    }

def test_geomx_processor_with_real_data(setup_real_data):
    real_data = setup_real_data
    processor = GeoMxProcessor(
        dcc_files=real_data["dcc_directory"],  # Pass the directory
        pkc_file=real_data["pkc_file"],
        metadata_file=real_data["metadata_file"]
    )
    adata = processor.process()

    assert adata is not None, "AnnData object is None"
    assert adata.obs.shape[0] > 0, "No rows in obs (RTS_ID metadata)"
    assert adata.var.shape[0] > 0, "No rows in var (ROI/sample metadata)"
    assert adata.X.size > 0, "Expression matrix is empty"
    assert len(adata.uns) > 0, "Unstructured metadata (uns) is empty"
