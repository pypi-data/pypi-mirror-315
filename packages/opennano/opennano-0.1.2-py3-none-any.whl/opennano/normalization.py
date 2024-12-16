
import numpy as np
import pandas as pd
import scipy
from scipy.sparse import issparse
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns


class Normalization:
    """
    A class for performing normalization on data using various methods and plotting PCA.

    Methods
    -------
    norm_CPM(adata, new_layer=True):
        Performs Counts Per Million normalization.

    norm_log1p(adata, new_layer=True):
        Applies log(1 + x) transformation to the data.

    norm_MedianRatio(adata, new_layer="MedianRatio_norm"):
        Normalizes data using the median ratio method.

    norm_VST(adata, size_factors=None, dispersion=None, new_layer="VST_norm", layer=None):
        Performs Variance Stabilizing Transformation (VST) normalization.

    norm_Quantile(adata, layer=None, new_layer="Quantile_norm"):
        Normalizes data using quantile normalization.

    variance(adata, layer="Test", n_genes=500):
        Computes variance and identifies highly variable genes.
    
    apply_vst_with_base_norm(adata, choice="median", new_layer="VST_norm"):
        Applies VST normalization with a specified base normalization method.

    plot_pca(adata, layer="Test", n_genes=500):
        Plots PCA on the top variable genes.
    """

    def __init__(self, adata):
        """
        Initialize the Normalization class with the provided AnnData object.

        Parameters
        ----------
        adata : AnnData
            The input AnnData object to normalize and analyze.
        """
        self.adata = adata

    def norm_CPM(self, new_layer=True):
        """
        Perform Counts Per Million (CPM) normalization on the AnnData object.

        This method normalizes raw counts data to CPM values, which represent
        counts per million reads for each feature, adjusted by the total library size.

        Parameters
        ----------
        new_layer : bool, optional
            If ``True``, saves the CPM-normalized data as a new layer named ``"CPM_norm"``
            in the AnnData object. If ``False``, returns the CPM-normalized data as a
            pandas DataFrame (default is ``True``).

        Returns
        -------
        pandas.DataFrame or None
            - If ``new_layer`` is ``False``, returns a pandas DataFrame containing the
              CPM-normalized data.
            - If ``new_layer`` is ``True``, returns ``None`` and stores the normalized data
              in the AnnData object's layers as ``"CPM_norm"``.

        Raises
        ------
        ValueError
            If the specified AnnData object does not contain raw counts data.

        Examples
        --------
        Normalize data and save as a new layer:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_CPM(new_layer=True)
            # Output: Added layer 'CPM_norm' to:
            #         AnnData object with n_obs × n_vars = 100 × 200

        Return normalized data as a DataFrame:

        .. code-block:: python

            normalization = Normalization(adata)
            cpm_data = normalization.norm_CPM(new_layer=False)
            print(cpm_data.head())
        """
        raw_counts = self.adata.to_df()
        library_sizes = raw_counts.sum(axis=0)

        if new_layer:
            self.adata.layers["CPM_norm"] = raw_counts.divide(library_sizes, axis=1) * 1e6
            print(f"Added layer 'CPM_norm' to:\n  {self.adata}")
        else:
            return raw_counts.divide(library_sizes, axis=1) * 1e6

    def norm_log1p(self, new_layer=True):
        """
        Apply log(1 + x) transformation to CPM-normalized data.

        This method first performs CPM normalization on the data (if not already done),
        then applies a log(1 + x) transformation.

        Parameters
        ----------
        new_layer : bool, optional
            If ``True``, saves the log-transformed data as a new layer named ``"log1p_norm"``
            in the AnnData object. If ``False``, creates the log-transformed data as a
            pandas DataFrame (default is ``True``).

        Returns
        -------
        pandas.DataFrame or None
            - If ``new_layer`` is ``False``, returns a pandas DataFrame containing the
              log-transformed data.
            - If ``new_layer`` is ``True``, returns ``None`` and stores the transformed data
              in the AnnData object's layers as ``"log1p_norm"``.

        Raises
        ------
        ValueError
            If the input data is not a valid AnnData object or does not contain
            raw counts data.

        Examples
        --------
        Apply log(1 + x) transformation and save as a new layer:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_log1p(new_layer=True)
            # Output: Added layer 'log1p_norm' to:
            #         AnnData object with n_obs × n_vars = 100 × 200

        Return log-transformed data as a DataFrame:

        .. code-block:: python

            normalization = Normalization(adata)
            log1p_data = normalization.norm_log1p(new_layer=False)
            print(log1p_data.head())
        """
        data = self.norm_CPM(new_layer=False)

        if new_layer:
            self.adata.layers["log1p_norm"] = np.log1p(data)
            print(f"Added layer 'log1p_norm' to:\n  {self.adata}")
        else:
            return np.log1p(data)

    def norm_MedianRatio(self, new_layer="MedianRatio_norm"):
        """
        Normalize data using the median ratio method.

        This method computes the geometric mean for each feature (gene) and normalizes
        the data by dividing each value by its respective median across samples.

        Parameters
        ----------
        new_layer : str or None, optional
            Name of the new layer to store the median ratio-normalized data. If ``None``,
            the normalized data is returned as a pandas DataFrame without modifying the
            AnnData object (default is ``"MedianRatio_norm"``).

        Returns
        -------
        pandas.DataFrame or None
            - If ``new_layer`` is ``None``, returns a pandas DataFrame containing the
              median ratio-normalized data.
            - If ``new_layer`` is specified, returns ``None`` and stores the normalized
              data in the AnnData object's layers.

        Raises
        ------
        ValueError
            If the input data is not a valid AnnData object or does not contain
            raw counts data.

        Examples
        --------
        Normalize data using the median ratio method and save as a new layer:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_MedianRatio(new_layer="MedianRatio_norm")
            # Output: Added layer 'MedianRatio_norm' to:
            #         AnnData object with n_obs × n_vars = 100 × 200

        Return the normalized data as a DataFrame:

        .. code-block:: python

            normalization = Normalization(adata)
            median_ratio_data = normalization.norm_MedianRatio(new_layer=None)
            print(median_ratio_data.head())
        """
        counts = self.adata.to_df().astype(float)
        for gene in counts.index:
            total = np.exp(np.mean(np.log(counts.loc[gene] + 1e-9)))
            counts.loc[gene] = counts.loc[gene].divide(total)
        medians = counts.median()

        if new_layer is not None:
            self.adata.layers[new_layer] = self.adata.to_df() / medians
            print(f"Added layer '{new_layer}' to:\n  {self.adata}")
        else:
            return counts

    def norm_VST(self, size_factors=None, dispersion=None, new_layer="VST_norm", layer=None):
        """
        Perform Variance Stabilizing Transformation (VST) normalization.

        This method stabilizes the variance of normalized count data. It first normalizes
        raw counts using size factors, optionally computes dispersion estimates, and then
        applies the variance stabilizing transformation.

        Parameters
        ----------
        size_factors : array-like, optional
            Pre-computed size factors for normalization. If ``None``, size factors
            are computed as the sum of counts divided by the median library size 
            (default is ``None``).

        dispersion : array-like, optional
            Dispersion estimates for variance stabilization. If ``None``, dispersion is
            estimated as the inverse square root of the mean counts (default is ``None``).

        new_layer : str or None, optional
            Name of the new layer to store the VST-normalized data. If ``None``,
            the normalized data is returned as a pandas DataFrame without modifying the
            AnnData object (default is ``"VST_norm"``).

        layer : str or None, optional
            Name of the existing layer in AnnData to apply VST normalization to.
            If ``None``, the default raw counts from the AnnData object are used
            (default is ``None``).

        Returns
        -------
        pandas.DataFrame or None
            - If ``new_layer`` is ``None``, returns a pandas DataFrame containing the
                VST-normalized data.
            - If ``new_layer`` is specified, returns ``None`` and stores the normalized
                data in the AnnData object's layers.

        Raises
        ------
        ValueError
            If ``layer`` is not found in the AnnData object or the input data is invalid.

        Examples
        --------
        Normalize data using VST with default parameters and save as a new layer:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_VST(new_layer="VST_norm")
            # Output: Added layer 'VST_norm' to:
            #         AnnData object with n_obs × n_vars = 100 × 200

        Return the VST-normalized data as a DataFrame:

        .. code-block:: python

            normalization = Normalization(adata)
            vst_data = normalization.norm_VST(new_layer=None)
            print(vst_data.head())
        """
        if layer != None:
            counts = self.adata.to_df(layer=layer)
        else:
            counts = self.adata.to_df()
    
        # Step 1: Normalize counts by size factors
        if size_factors is None:
            size_factors = counts.sum(axis=0) / np.median(counts.sum(axis=0))
    
        normalized_counts = counts.divide(size_factors, axis=1)

        # Step 2: Estimate dispersions if not provided
        if dispersion is None:
            mean_counts = normalized_counts.mean(axis=1)
            dispersion = np.where(mean_counts > 0, 1 / np.sqrt(mean_counts), 1)

        # Step 3: Apply the variance stabilizing transformation
        vst_transformed = normalized_counts.apply(
            lambda col: np.log2((col + 1) / dispersion), axis=0
        )

        if new_layer != None:
            self.adata.layers[new_layer] = vst_transformed
            print(f"Added layer 'VST_norm' to:\n  {self.adata}")
        else:
            return vst_transformed


    def norm_Quantile(self, layer=None, new_layer="Quantile_norm"):
        """
        Perform quantile normalization.

        This method normalizes the data by ranking the values and replacing each
        value with the mean value of its rank across all samples.

        Parameters
        ----------
        layer : str or None, optional
            Name of the existing layer in AnnData to apply quantile normalization to.
            If ``None``, the raw counts (``adata.X``) are used (default is ``None``).

        new_layer : str or None, optional
            Name of the new layer to store the quantile-normalized data. If ``None``,
            the normalized data replaces the raw counts in ``adata.X`` (default is
            ``"Quantile_norm"``).

        Returns
        -------
        None
            Normalized data is stored in the specified `new_layer` or replaces the raw
            counts in ``adata.X``.

        Raises
        ------
        ValueError
            If the specified `layer` is not found in the AnnData object.

        Examples
        --------
        Normalize data using quantile normalization and save as a new layer:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_Quantile(new_layer="Quantile_norm")
            # Output: Added layer 'Quantile_norm' to:
            #         AnnData object with n_obs × n_vars = 100 × 200

        Replace raw counts with quantile-normalized data:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.norm_Quantile(new_layer=None)
            print(adata.X)
        """
        if layer:
            if layer not in self.adata.layers:
                raise ValueError(f"Layer {layer} not found in AnnData.")
            data = self.adata.layers[layer]
        else:
            data = self.adata.X

        if issparse(data):
            data = data.toarray()

        df = pd.DataFrame(data)
        rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
        normalized_df = df.rank(method='min').stack().astype(int).map(rank_mean).unstack()

        if new_layer is not None:
            self.adata.layers[new_layer] = normalized_df.values
            print(f"Added layer '{new_layer}' to:\n  {self.adata}")
        else:
            self.adata.X = normalized_df.values


    def variance(self, adata=None, layer=None, n_genes=500):
        """
        Compute variance for each feature and identify highly variable genes.

        This method calculates the variance across all samples for each feature (gene)
        in the specified layer and flags the top `n_genes` as highly variable.

        Parameters
        ----------
        layer : str or None, optional
            Name of the existing layer in AnnData to compute variance from. If ``None``,
            the default raw counts (``adata.X``) are used (default is ``None``).

        n_genes : int, optional
            Number of top variable features to mark as highly variable (default is ``500``).

        Returns
        -------
        None
            The variance is added to ``adata.var["vars"]``, and highly variable genes
            are flagged in ``adata.var["highly_variable"]``.

        Raises
        ------
        ValueError
            If the specified `layer` is not found in the AnnData object.

        Examples
        --------
        Compute variance and mark highly variable genes:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.variance(layer="Quantile_norm", n_genes=300)
            print(adata.var.head())
        """
        
        if adata is None:
            adata = self.adata
        
        if layer:
            data = adata.layers[layer]
        else:
            data = adata.X

        if scipy.sparse.issparse(data):
            data = data.toarray()
            
        vars = np.var(data, axis=0, ddof=1)
        adata.var["vars"] = vars

        adata.var['highly_variable'] = False  
        top_n_idx = adata.var.sort_values(by="vars", ascending=False).head(n_genes).index
        adata.var.loc[top_n_idx, 'highly_variable'] = True


    def apply_vst_with_base_norm(self, choice="median", new_layer="VST_norm", ):
        """
        Apply Variance Stabilizing Transformation (VST) on data with a specified base normalization.

        This method allows the user to apply a base normalization method (e.g., CPM, log1p, quantile,
        or median ratio) before performing VST. The results are saved as a new layer in the AnnData
        object.

        Parameters
        ----------
        choice : str, optional
            The base normalization method to apply before VST. Options are:
            - ``"cpm"``: Counts Per Million normalization.
            - ``"log1p"``: Log(1 + x) transformation.
            - ``"quantile"``: Quantile normalization.
            - ``"median"``: Median ratio normalization (default).

        new_layer : str, optional
            Name of the new layer to store the VST-normalized data. The default is ``"VST_norm"``.

        Returns
        -------
        AnnData
            The AnnData object with the VST-normalized data added as a new layer.

        Raises
        ------
        ValueError
            If an invalid `choice` is provided.

        Examples
        --------
        Apply VST normalization with median ratio as the base normalization:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.apply_vst_with_base_norm(choice="median", new_layer="VST_norm")
            # Output: VST normalization applied on base normalization 'median' and saved as layer 'VST_norm'

        Apply VST normalization with quantile normalization as the base:

        .. code-block:: python

            normalization = Normalization(adata)
            normalization.apply_vst_with_base_norm(choice="quantile", new_layer="Quantile_VST_norm")
        """
        base_layer = None

        if choice == "cpm":
            self.norm_CPM(new_layer="CPM_norm")
            base_layer = "CPM_norm"
        elif choice == "log1p":
            self.norm_log1p(new_layer="log1p_norm")
            base_layer = "log1p_norm"
        elif choice == "quantile":
            self.norm_Quantile(new_layer="Quantile_norm")
            base_layer = "Quantile_norm"
        elif choice == "median":
            self.norm_MedianRatio(new_layer="MedianRatio_norm")
            base_layer = "MedianRatio_norm"
        else:
            raise ValueError(f"Invalid normalization choice: {choice}")

        if base_layer:
            self.norm_VST(new_layer="VST_norm", layer=base_layer)
            print(f"VST normalization applied on base normalization '{choice}' and saved as layer '{new_layer}'")
        return self.adata
    
    
    def plot_pca(self, layer="VST_norm", n_genes=500):
        """
        Perform PCA on the most variable genes and generate a PCA plot.

        This method computes PCA on the specified layer of the AnnData object using the
        top `n_genes` most variable features. It requires that a specified layer (e.g., a
        VST-normalized layer) is available in the AnnData object.

        Parameters
        ----------
        layer : str, optional
            Name of the layer in AnnData to perform PCA on. The default is ``"VST_norm"``.
            The layer must contain pre-normalized data (e.g., via VST).

        n_genes : int, optional
            Number of top variable features to use for PCA computation. The default is ``500``.

        Returns
        -------
        None
            The PCA plot is displayed directly.

        Raises
        ------
        ValueError
            If the specified `layer` is not found in the AnnData object.

        Examples
        --------
        Generate a PCA plot using the VST-normalized layer:

        .. code-block:: python

            normalization = norm_VST(adata)
            normalization.plot_pca(layer="VST_norm", n_genes=500)

        Generate a PCA plot using a custom normalized layer:

        .. code-block:: python

            normalization = norm_VST(adata)
            normalization.plot_pca(layer="Quantile_norm", n_genes=300)
    """
        # Transpose the data so that ROIs (columns) are treated as observations
        adata_transposed = self.adata.copy().T

        # Take only the 500 most variable
        # sc.pp.highly_variable_genes(adata_transposed, layer="Test", n_top_genes=500, inplace=True)
        # variance(adata_transposed, n_genes=500)

        # Perform PCA using Scanpy
        sc.tl.pca(adata_transposed, layer="VST_norm") # mask_var="highly_variable"

        # Remove the reps
        adata_transposed.obs["Sample_Title"] = adata_transposed.obs["Sample_Title"].str.replace(r'_rep\d+$', '', regex=True)
        adata_transposed.obs["Sample_Title"] = adata_transposed.obs["Sample_Title"].astype('category')

        # Labels
        variance_ratio = adata_transposed.uns['pca']['variance_ratio']
        pc1_percentage = variance_ratio[0] * 100
        pc2_percentage = variance_ratio[1] * 100

        # Plot PCA scatter plot
        ax = sc.pl.scatter(adata_transposed, basis='pca', x='PC1', y='PC2', color="Sample_Title", title="PCA of ROIs", size=200, show=False)
        plt.xlabel(f'PC1: {round(pc1_percentage, 2)}%')
        plt.ylabel(f'PC2: {round(pc2_percentage, 2)}%')
        # plt.savefig("PCA_Filtered_7799.png", dpi=300)
        plt.show()

        
    def plot_density(self, layer=None, title=None, figsize=(10, 6), log_scale=False):
        """
        Generate density plots to visualize expression distributions across samples for a given normalization.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing gene expression data.

        layer : str, optional
            Name of the layer in AnnData to plot. If ``None``, uses `adata.X` (default is ``None``).

        title : str, optional
            Title of the plot (default is ``None``).

        figsize : tuple, optional
            Size of the plot (default is ``(10, 6)``).

        log_scale : bool, optional
            If ``True``, applies a log10 transformation to the expression data before plotting (default is ``False``).

        Returns
        -------
        None
            Displays the density plot.
        """
        # Extract data from the specified layer or `adata.X`
        if layer:
            if layer not in self.adata.layers:
                raise ValueError(f"Layer '{layer}' not found in AnnData object.")
            data = self.adata.layers[layer].toarray() if hasattr(self.adata.layers[layer], "toarray") else self.adata.layers[layer]
        else:
            data = self.adata.X.toarray() if hasattr(self.adata.X, "toarray") else self.X

        # Apply log10 transformation if requested
        if log_scale:
            data = np.log10(data + 1e-9)

        # Create a DataFrame for easier handling
        df = pd.DataFrame(data, columns=self.adata.var_names)

        # Plot density for each sample
        plt.figure(figsize=figsize)
        for column in df.columns:
            sns.kdeplot(df[column], label=column, alpha=0.6)

        # Customize the plot
        plt.title(title or "Density Plot of Expression Distributions", fontsize=14)
        plt.xlabel("Expression Values" if log_scale else "Expression Values", fontsize=12)
        plt.ylabel("Density", fontsize=12)
        plt.legend(title="Samples", loc="upper right", fontsize=8)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Display the plot
        plt.show()