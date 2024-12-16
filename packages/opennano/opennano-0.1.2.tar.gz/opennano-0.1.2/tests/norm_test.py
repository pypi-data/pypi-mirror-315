import unittest
import numpy as np
import pandas as pd
import anndata as ad
from opennano import normalization as norm

class TestNormalization(unittest.TestCase):

    def setUp(self):
        """
        Create a test AnnData object for normalization.
        """
        # Mock AnnData object
        data = np.random.poisson(10, size=(100, 50))  # Simulated raw count data
        obs = pd.DataFrame({"cell_id": [f"cell_{i}" for i in range(100)]}).set_index("cell_id")
        var = pd.DataFrame({"gene_id": [f"gene_{i}" for i in range(50)]}).set_index("gene_id")
        self.adata = ad.AnnData(X=data, obs=obs, var=var)

    def test_norm_CPM(self):
        """
        Test Counts Per Million normalization.
        """
        normalization = norm(self.adata)
        normalization.norm_CPM(new_layer=True)

        # Assert the layer is added
        self.assertIn("CPM_norm", self.adata.layers)
        # Check values are scaled to counts per million
        cpm_sum = self.adata.layers["CPM_norm"].sum(axis=1)
        np.testing.assert_array_almost_equal(cpm_sum, np.ones_like(cpm_sum) * 1e6, decimal=3)

    def test_norm_log1p(self):
        """
        Test log(1 + x) transformation.
        """
        normalization = norm(self.adata)
        normalization.norm_log1p(new_layer=True)

        # Assert the layer is added
        self.assertIn("log1p_norm", self.adata.layers)

        # Assert the log transformation is applied
        log1p_data = np.log1p(self.adata.to_df())
        np.testing.assert_array_almost_equal(
            log1p_data.values, self.adata.layers["log1p_norm"].toarray(), decimal=3
        )

    def test_norm_MedianRatio(self):
        """
        Test Median Ratio normalization.
        """
        normalization = norm(self.adata)
        normalization.norm_MedianRatio(new_layer="MedianRatio_norm")

        # Assert the layer is added
        self.assertIn("MedianRatio_norm", self.adata.layers)

    def test_norm_VST(self):
        """
        Test Variance Stabilizing Transformation normalization.
        """
        normalization = norm(self.adata)
        normalization.norm_VST(new_layer="VST_norm")

        # Assert the layer is added
        self.assertIn("VST_norm", self.adata.layers)

    def test_norm_Quantile(self):
        """
        Test Quantile normalization.
        """
        normalization = norm(self.adata)
        normalization.norm_Quantile(new_layer="Quantile_norm")

        # Assert the layer is added
        self.assertIn("Quantile_norm", self.adata.layers)

    def test_variance(self):
        """
        Test variance computation and identifying highly variable genes.
        """
        normalization = norm(self.adata)
        normalization.variance(layer=None, n_genes=20)

        # Check if "vars" and "highly_variable" are added to var
        self.assertIn("vars", self.adata.var.columns)
        self.assertIn("highly_variable", self.adata.var.columns)
        self.assertEqual(self.adata.var["highly_variable"].sum(), 20)

    def test_apply_vst_with_base_norm(self):
        """
        Test VST normalization with base normalization method.
        """
        normalization = norm(self.adata)
        normalization.apply_vst_with_base_norm(choice="median", new_layer="VST_with_Median")

        # Assert the layer is added
        self.assertIn("VST_with_Median", self.adata.layers)

    def test_plot_pca(self):
        """
        Test PCA plotting. This is mainly to ensure no errors are raised.
        """
        normalization = norm(self.adata)
        normalization.variance(n_genes=10)  # Precompute highly variable genes for PCA
        try:
            normalization.plot_pca(layer="VST_norm", n_genes=10)
        except Exception as e:
            self.fail(f"PCA plotting failed with exception: {e}")

    def test_plot_density(self):
        """
        Test density plotting. Ensure no errors are raised during plotting.
        """
        normalization = norm(self.adata)
        try:
            normalization.plot_density(layer=None, log_scale=False)
        except Exception as e:
            self.fail(f"Density plotting failed with exception: {e}")


if __name__ == "__main__":
    unittest.main()