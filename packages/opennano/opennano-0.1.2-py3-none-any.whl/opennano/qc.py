from typing import Literal, Sequence

import os
import numpy as np
import pandas as pd
import anndata as ad
import scipy.sparse
import matplotlib.pyplot as plt
import seaborn as sns

from opennano.io import GeoMxProcessor

class CountsQC:
    """
    A class for performing quality control (QC) checks on an AnnData object.
    """

    def __init__(
        self,
        adata=None,
        dcc_directory=None,
        pkc_file=None,
        metadata_file=None,
        minSegmentReads=1000,
        percentTrimmed=80,
        percentStitched=80,
        percentAligned=75,
        percentSaturation=50,
        minNegativeCount=10,
        maxNTCCount=9000,
        minNuclei=20,
        minArea=1000,
        negative_probe_cutoff=1.1,
    ):
        """
        Initialize the `CountsQC` class for performing quality control on GeoMx data.

        This constructor initializes a `CountsQC` object either from an existing `AnnData` object 
        or by processing `.dcc`, `.pkc`, and metadata files to generate an `AnnData` object. It 
        also sets quality control thresholds for various metrics.

        Parameters
        ----------
        adata : AnnData, optional
            An existing `AnnData` object to initialize the QC process. If not provided, the `dcc_directory`, 
            `pkc_file`, and `metadata_file` parameters must be specified to create the `AnnData` object.
        dcc_directory : str, optional
            Path to the directory containing `.dcc` files. Required if `adata` is not provided.
        pkc_file : str, optional
            Path to the `.pkc` file. Required if `adata` is not provided.
        metadata_file : str, optional
            Path to the GEO SOFT metadata file. Required if `adata` is not provided.
        minSegmentReads : int, default=1000
            Minimum number of reads required for a segment to pass QC.
        percentTrimmed : int, default=80
            Minimum percentage of trimmed reads required for a segment to pass QC.
        percentStitched : int, default=80
            Minimum percentage of stitched reads required for a segment to pass QC.
        percentAligned : int, default=75
            Minimum percentage of aligned reads required for a segment to pass QC.
        percentSaturation : int, default=50
            Minimum sequencing saturation percentage required for a segment to pass QC.
        minNegativeCount : int, default=10
            Minimum count of negative probes required for a segment to pass QC.
        maxNTCCount : int, default=9000
            Maximum count for no-template control (NTC) probes allowed for a segment to pass QC.
        minNuclei : int, default=20
            Minimum number of nuclei required for a segment to pass QC.
        minArea : int, default=1000
            Minimum area (in pixels or other units) required for a segment to pass QC.

        Raises
        ------
        ValueError
            If `adata` is not provided and any of `dcc_directory`, `pkc_file`, or `metadata_file` is missing.

        Notes
        -----
        - If `adata` is not provided, the class processes the GeoMx data from the provided files 
          (`dcc_directory`, `pkc_file`, and `metadata_file`) using the `GeoMxProcessor` class.
        - The initialized object contains metadata and quality control thresholds that can be 
          used for running QC checks and generating filtered datasets.

        Attributes
        ----------
        adata : AnnData
            The `AnnData` object containing the GeoMx data, either provided or created during initialization.
        df : pandas.DataFrame
            DataFrame representation of the expression matrix from the `AnnData` object.
        roi_metadata : list
            List of regions of interest (ROIs) from the unstructured metadata in the `AnnData` object.
        neg_probe_indices : pandas.Index
            Indices of negative probes in the `AnnData` object.
        passed_rois : list
            List of ROIs that pass all QC checks, initialized as empty.
        """
        
        if adata is None:
            if not all([dcc_directory, pkc_file, metadata_file]):
                raise ValueError(
                    "If adata is not provided, specify dcc_directory, pkc_file, and metadata_file."
                )
            print("Creating AnnData object from GeoMx data. This may take a moment...")
            processor = GeoMxProcessor(
                dcc_files=dcc_directory,
                pkc_file=pkc_file,
                metadata_file=metadata_file
            )
            adata = processor.process()

        self.adata = adata
        self.minSegmentReads = minSegmentReads
        self.percentTrimmed = percentTrimmed
        self.percentStitched = percentStitched
        self.percentAligned = percentAligned
        self.percentSaturation = percentSaturation
        self.minNegativeCount = minNegativeCount
        self.maxNTCCount = maxNTCCount
        self.minNuclei = minNuclei
        self.minArea = minArea
        
        self.negative_probe_cutoff = negative_probe_cutoff

        self.df = adata.to_df()
        self.roi_metadata = list(adata.uns.keys())
        self.neg_probe_indices = adata.obs.index[adata.obs["SystematicName"].str.startswith("NegProbe-WTX")]
        self.passed_rois = []

    def _print_progress(self, metric_name, failed_count, total_segments):
        """
        Helper method to display QC check progress.
        """
        passed_count = total_segments - failed_count
        passed_percentage = (passed_count / total_segments) * 100
        print(
            f"Metric: {metric_name} | Passed: {passed_count}/{total_segments} "
            f"({passed_percentage:.2f}%) | Failed: {failed_count}/{total_segments}\n"
        )
        return passed_percentage

    def check_metric(self, metric_name, threshold, calc_function, unit="%"):
        """
        Evaluates a specific quality control (QC) metric for each segment and identifies segments that fail.

        This method applies a calculation function (`calc_function`) to compute a QC metric for 
        each region of interest (ROI) in the dataset. It compares the computed values against a 
        specified threshold to determine which segments pass or fail the QC check.

        Parameters
        ----------
        metric_name : str
            Name of the metric being checked (e.g., "Percent Trimmed", "Total Reads").
        threshold : float or int
            Minimum acceptable value for the metric. Segments with values below this threshold fail the QC check.
        calc_function : callable
            A function that calculates the metric for a given segment. It should take the `adata` object 
            and a segment identifier (`idx`) as inputs and return the computed value.
        unit : str, optional
            Unit of the metric for display purposes (default is "%").

        Returns
        -------
        set
            A set of segment identifiers (ROIs) that pass the QC check.

        Raises
        ------
        Exception
            If the `calc_function` encounters an error during computation.

        Notes
        -----
        - This method iterates over all segment identifiers (`roi_metadata`) in the dataset.
        - Segments that fail the QC check are printed with a warning message, displaying the 
          metric value and the threshold.
        - The progress and percentage of passing segments are displayed using `_print_progress`.

        Examples
        --------
        Define a metric calculation function:

        .. code-block:: python

            def calc_total_reads(adata, idx):
                return adata[idx].sum()

        Check the "Total Reads" metric:

        .. code-block:: python

            passed_segments = qc.check_metric(
                metric_name="Total Reads",
                threshold=1000,
                calc_function=calc_total_reads,
                unit="reads"
            )
            print("Segments passing QC:", passed_segments)
        """
        print(f"Checking {metric_name} for each segment (Threshold: {threshold}{unit})...")
        failed_rois = []

        for idx in self.roi_metadata:
            value = calc_function(self.adata, idx)
            if value < threshold:
                failed_rois.append(idx)
                print(
                    f'[WARNING] Segment "{idx}" failed: {metric_name} = {value:.2f}{unit} '
                    f"(Threshold: {threshold}{unit})."
                )

        failed_count = len(failed_rois)
        passed_percentage = self._print_progress(metric_name, failed_count, len(self.roi_metadata))
        return set(self.roi_metadata) - set(failed_rois)

    def calc_total_reads(self, adata, idx):
        """
        Calculate the total number of reads for a specific region of interest (ROI).

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        int
            The sum of all reads for the specified ROI.
        """
        return self.df[idx].sum()

    def calc_percent_trimmed(self, adata, idx):
        """
        Calculate the percentage of trimmed reads for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        float
            The percentage of reads that were trimmed.
        """
        return (int(adata.uns[idx]["trimmedreads"]) / int(adata.uns[idx]["rawreads"])) * 100

    def calc_percent_stitched(self, adata, idx):
        """
        Calculate the percentage of stitched reads for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        float
            The percentage of reads that were stitched.
        """
        return (int(adata.uns[idx]["stitchedreads"]) / int(adata.uns[idx]["rawreads"])) * 100

    def calc_percent_aligned(self, adata, idx):
        """
        Calculate the percentage of aligned reads for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        float
            The percentage of reads that were aligned.
        """
        return (int(adata.uns[idx]["alignedreads"]) / int(adata.uns[idx]["rawreads"])) * 100

    def calc_percent_saturation(self, adata, idx):
        """
        Calculate the sequencing saturation for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        float
            The sequencing saturation value for the ROI.
        """
        return float(adata.uns[idx]["sequencingsaturation"])

    def calc_min_nuclei(self, adata, idx):
        """
        Retrieve the minimum nuclei count for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        int
            The minimum nuclei count for the ROI.
        """
        return int(adata.uns[idx]["nuclei_counts"])

    def calc_min_area(self, adata, idx):
        """
        Retrieve the minimum area for a specific ROI.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing expression and metadata.
        idx : str
            The key of the ROI in the unstructured data (`uns`) of the AnnData object.

        Returns
        -------
        int
            The minimum area for the ROI.
        """
        return int(adata.uns[idx]["area"])

    @staticmethod
    def filter_by_negativeProbes(adata, negative_probe_cutoff=1.1, save_negatives=False):
        """
        Filters genes based on their background ratios compared to negative probes.

        Parameters
        ----------
        adata : AnnData
            The AnnData object containing gene expression data.

        cutoff : float, optional
            The threshold for filtering genes based on their background ratios.
            Genes with ratios below this threshold are removed (default is ``1.1``).

        save_negatives : bool, optional
            If ``True``, returns a second AnnData object containing only the negative probes
            (default is ``False``).

        Returns
        -------
        AnnData or tuple of AnnData
            - If `save_negatives` is ``False``, returns the filtered AnnData object.
            - If `save_negatives` is ``True``, returns a tuple:
              (filtered AnnData object, AnnData object of negative probes).

        Raises
        ------
        ValueError
            If the `adata` object does not contain the required "SystematicName" column.

        Examples
        --------
        Filter genes by negative probes and save the negative probes:

        .. code-block:: python

            qc = QC()
            filtered_adata, negatives = qc.filter_by_negativeProbes(adata, cutoff=1.5, save_negatives=True)

        Filter genes by negative probes without saving negatives:

        .. code-block:: python

            qc = QC()
            filtered_adata = qc.filter_by_negativeProbes(adata, cutoff=1.2)
        """
        def geom_mean(series):
        # Calculate the geometric mean of a series
            return np.exp(np.mean(np.log(series + 1e-9)))

        # Ensure "SystematicName" is in obs
        if "SystematicName" not in adata.obs:
            raise ValueError("The AnnData object must contain a 'SystematicName' column in `obs`.")

        # Separate negative probes and genes
        adata_genes = adata[adata.obs["SystematicName"] != "NegProbe-WTX"].copy()
        if save_negatives:
            neg_adata = adata[adata.obs["SystematicName"] == "NegProbe-WTX"].copy()
        neg_df = adata.to_df().loc[adata.obs[adata.obs["SystematicName"] == "NegProbe-WTX"].index]

        # Calculate geometric mean for the negative probes
        neg_list = neg_df.sum(axis=0) / len(neg_df)
        geom_neg = geom_mean(neg_list)

        # Calculate background ratios for every gene and add it as a new column
        adata_genes.obs["Background_Ratios"] = adata_genes.to_df().apply(lambda row: geom_mean(row) / geom_neg, axis=1)

        # Filter genes based on the cutoff
        filtered_adata = adata_genes[adata_genes.obs["Background_Ratios"] > negative_probe_cutoff].copy()

        # Debugging output: Number of genes filtered out
        num_filtered = adata_genes.shape[0] - filtered_adata.shape[0]
        print(f"[INFO] Filtered {num_filtered} genes with Background Ratios below {negative_probe_cutoff}. Remaining genes: {filtered_adata.shape[0]}.")
        print(adata_genes.obs["Background_Ratios"].describe())
        print(f"Number of genes passing cutoff: {(adata_genes.obs['Background_Ratios'] > negative_probe_cutoff).sum()}")


        if save_negatives:
            return filtered_adata, neg_adata
        else:
            return filtered_adata
        
    def run_all_checks(self, return_negative_probes=False, negative_probe_cutoff=None):
        """
        Run all QC checks and return filtered AnnData objects.

        Parameters
        ----------
        return_negative_probes : bool, optional
            Whether to return an AnnData object containing only the negative probes (default is ``False``).

        negative_probe_cutoff : float, optional
            The cutoff for filtering genes based on their background ratios compared to negative probes (default is ``1.1``).

        Returns
        -------
        filtered_adata : AnnData
            AnnData object with only ROIs passing all QC checks.

        negative_probes_adata : AnnData, optional
            AnnData object with only negative probes (if requested).
        """
        print("\n=== Starting QC Checks ===\n")

        # Define QC metrics and thresholds
        metrics = {
            "total reads": (self.minSegmentReads, self.calc_total_reads, ""),
            "percent trimmed": (self.percentTrimmed, self.calc_percent_trimmed, "%"),
            "percent stitched": (self.percentStitched, self.calc_percent_stitched, "%"),
            "percent aligned": (self.percentAligned, self.calc_percent_aligned, "%"),
            "percent saturation": (self.percentSaturation, self.calc_percent_saturation, "%"),
            "min nuclei count": (self.minNuclei, self.calc_min_nuclei, ""),
            "min area": (self.minArea, self.calc_min_area, "")
        }

        # Step 1: ROI-based filtering
        self.passed_rois = set(self.roi_metadata)
        for metric_name, (threshold, calc_function, unit) in metrics.items():
            passed_rois_for_metric = self.check_metric(metric_name, threshold, calc_function, unit)
            self.passed_rois &= passed_rois_for_metric

        print("=== ROI QC Checks Completed ===")
        print(f"[INFO] ROIs passing all checks: {len(self.passed_rois)}")

        filtered_adata = self.adata[:, self.adata.var.index.isin(self.passed_rois)]

        if filtered_adata.n_obs == 0:
            print("[WARNING] No ROIs remaining after QC filtering!")
            return None

        # Step 2: Gene-based filtering (negative probe filtering)
        if negative_probe_cutoff is None:
            negative_probe_cutoff = self.negative_probe_cutoff

        if return_negative_probes:
           filtered_adata, negative_probes_adata = CountsQC.filter_by_negativeProbes(
               filtered_adata, negative_probe_cutoff=negative_probe_cutoff, save_negatives=True
            )
        else:
            filtered_adata = CountsQC.filter_by_negativeProbes(filtered_adata, negative_probe_cutoff=negative_probe_cutoff)

        if filtered_adata.n_obs == 0 or filtered_adata.n_vars == 0:
            print("[WARNING] No data remaining after gene QC filtering!")
            return None

        # Summary
        print("=== Summary ===")
        print(f"Total ROIs: {len(self.roi_metadata)}")
        print(f"ROIs Passing All Checks: {len(self.passed_rois)}")
        print(f"Filtered AnnData Object Dimensions: {filtered_adata.shape}")
        if return_negative_probes:
            print(f"Negative Probes AnnData Object Dimensions: {negative_probes_adata.shape}")

        self.adata = filtered_adata

        return (filtered_adata, negative_probes_adata) if return_negative_probes else filtered_adata
    
    def write(self, filename: str = None, compression: Literal["gzip", "lzf"] = None):
        """
        Write the Anndata object to disk.

        Parameters
        ----------
        filename : str
            The name and the location of the file to write the Anndata object to.
        compression : str, optional
            Compression strategy to use ('gzip' or 'lzf').

        Raise
        -----
        ValueError:
            If the 'filename' is not provided or is invalid.
        """
        # Validate input
        if filename is None:
            raise ValueError("Filename must be provided to write the AnnData object.")

        # Check if the file already exists
        directory = os.path.dirname(filename)
        if directory and not os.path.exists(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist. Please provide a valid path.")

        # Write the AnnData object to the specified file
        print(f"Writing AnnData object to '{filename}' with compression={compression}...")
        self.adata.write(filename, compression=compression)
        print(f"AnnData object successfully written to '{filename}'.")

    def plot_qc_results(self):
        """
        Generate visualizations for Quality Control (QC) metrics.

        This method generates a series of plots to visualize QC metrics across all 
        regions of interest (ROIs) in the dataset. The visualizations include:
    
        1. Bar plot showing the percentage of segments passing QC thresholds.
        2. Histograms for each metric with optional threshold overlays.
        3. A heatmap of QC failures across metrics.
        4. A scatter plot comparing "Percent Trimmed" and "Percent Stitched" reads.

        Thresholds for each metric are defined in the class attributes (e.g., `minSegmentReads`, 
        `percentTrimmed`). Metrics without defined thresholds are visualized without overlays.

        Parameters
        ----------
        None

        Returns
        -------
        None
            This method generates and displays the plots but does not return any data.

        Notes
        -----
        - The metrics visualized include:
            - Total Reads
            - Percent Trimmed
            - Percent Stitched
            - Percent Aligned
            - Percent Saturation
            - Min Nuclei
            - Min Area
        - Metrics without valid data or missing thresholds are handled gracefully.
        - If thresholds are defined, they are indicated on the plots as dashed lines.

        Example
        -------
        .. code-block:: python

            qc = CountsQC(adata=my_adata)
            qc.plot_qc_results()
        """
        metrics = {
            "Total Reads": [self.calc_total_reads, getattr(self, "minSegmentReads", None)],
            "Percent Trimmed": [self.calc_percent_trimmed, getattr(self, "percentTrimmed", None)],
            "Percent Stitched": [self.calc_percent_stitched, getattr(self, "percentStitched", None)],
            "Percent Aligned": [self.calc_percent_aligned, getattr(self, "percentAligned", None)],
            "Percent Saturation": [self.calc_percent_saturation, getattr(self, "percentSaturation", None)],
            "Min Nuclei": [self.calc_min_nuclei, getattr(self, "minNuclei", None)],
            "Min Area": [self.calc_min_area, getattr(self, "minArea", None)],
        }

        # Prepare data for plotting
        results = {metric: [] for metric in metrics}
        for idx in self.roi_metadata:
            for metric_name, (calc_func, _) in metrics.items():
                try:
                    results[metric_name].append(calc_func(self.adata, idx))
                except KeyError:
                    results[metric_name].append(None)  # Handle missing data gracefully

        # Convert to DataFrame
        results_df = pd.DataFrame(results)

        # 1. Bar Plot - Percentage of Passing Segments
        pass_percentages = {
            metric: (results_df[metric] >= threshold).mean() * 100
            for metric, (_, threshold) in metrics.items() if threshold is not None
        }
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(pass_percentages.keys()), y=list(pass_percentages.values()))
        plt.xticks(rotation=45, ha="right")
        plt.ylabel("Percentage of Segments Passing")
        plt.title("QC Metrics: Percentage of Passing Segments")
        plt.show()

        # 2. Histogram for Each Metric
        for metric, (_, threshold) in metrics.items():
            plt.figure(figsize=(8, 5))
            sns.histplot(results_df[metric], kde=True, bins=20, label="Distribution")
            if threshold is not None:
                plt.axvline(x=threshold, color='red', linestyle='--', label=f"Threshold: {threshold}")
            plt.title(f"Distribution of {metric}")
            plt.xlabel(metric)
            plt.ylabel("ROIs")
            plt.legend()
            plt.show()

        # 3. Heatmap for QC Failures
        failure_matrix = pd.DataFrame(
            {metric: results_df[metric] < threshold for metric, (_, threshold) in metrics.items() if
             threshold is not None}
        )
        plt.figure(figsize=(10, 8))
        sns.heatmap(failure_matrix, cmap="Reds", cbar=True, yticklabels=False)
        plt.title("QC Failures (1 = Failed)")
        plt.xlabel("Metrics")
        plt.ylabel("Segments")
        plt.show()

        # 4. Scatter Plot - Trimmed vs. Stitched Reads
        if "Percent Trimmed" in metrics and "Percent Stitched" in metrics:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(
                x=results_df["Percent Trimmed"],
                y=results_df["Percent Stitched"],
                hue=(results_df["Percent Trimmed"] > getattr(self, "percentTrimmed", -1)) &
                    (results_df["Percent Stitched"] > getattr(self, "percentStitched", -1)),
                palette={True: "green", False: "red"}
            )
            if self.percentTrimmed is not None:
                plt.axvline(x=self.percentTrimmed, color='blue', linestyle='--',
                            label=f"Trimmed Threshold: {self.percentTrimmed}")
            if self.percentStitched is not None:
                plt.axhline(y=self.percentStitched, color='red', linestyle='--',
                            label=f"Stitched Threshold: {self.percentStitched}")
            plt.title("Trimmed Reads vs. Stitched Reads")
            plt.xlabel("Percent Trimmed")
            plt.ylabel("Percent Stitched")
            plt.legend(title="Passed QC", loc="upper left")
            plt.show()

    def plot_before_after_filtering(self):
        """
        Generate visualizations to compare data before and after QC filtering.

        This method creates visualizations to show the differences in expression 
        data before and after applying QC filters. The plots generated include:

        1. Scatter plots of total expression sums per sample (before and after filtering).
        2. Histograms of expression sum distributions (before and after filtering).

        Parameters
        ----------
        None

        Returns
        -------
        None
            The method generates and displays plots but does not return any data.

        Notes
        -----
        - This method uses the `run_all_checks` method to filter the data based on QC metrics.
        - The raw and filtered `AnnData` objects are compared to highlight the impact of QC filtering.
        - The expression sums are computed across all samples for visualization.

        Examples
        --------
        .. code-block:: python

            qc = CountsQC(adata=my_adata)
            qc.plot_before_after_filtering()
        """
        # Extract raw data
        raw_adata = self.adata
        raw_sample_titles = raw_adata.var['Sample_Title']
        raw_expression_sums = raw_adata.X.sum(axis=0)  # Sum expression counts per sample

        # Extract filtered data
        filtered_adata = self.run_all_checks(return_negative_probes=False)  # Run QC and retrieve filtered AnnData
        filtered_sample_titles = filtered_adata.var['Sample_Title']
        filtered_expression_sums = filtered_adata.X.sum(axis=0)  # Sum expression counts per sample

        # Scatter Plot: Expression Sums vs Samples (Before vs After)
        fig, axs = plt.subplots(1, 2, figsize=(16, 7))

        # Raw Data Scatter Plot
        sns.scatterplot(ax=axs[0], x=raw_sample_titles, y=raw_expression_sums, color='red', alpha=0.6, s=30)
        axs[0].set_title("Before Filtering: Expression Sums per Sample")
        axs[0].set_xlabel("Sample Title")
        axs[0].set_ylabel("Expression Sum")
        axs[0].tick_params(axis='x', rotation=45)
        axs[0].grid()

        # Filtered Data Scatter Plot
        sns.scatterplot(ax=axs[1], x=filtered_sample_titles, y=filtered_expression_sums, color='green', alpha=0.6, s=30)
        axs[1].set_title("After Filtering: Expression Sums per Sample")
        axs[1].set_xlabel("Sample Title")
        axs[1].set_ylabel("Expression Sum")
        axs[1].tick_params(axis='x', rotation=45)
        axs[1].grid()

        plt.tight_layout()
        plt.show()

        # Histograms: Expression Sums (Before vs After)
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))

        # Histogram: Expression Sums (Raw)
        sns.histplot(raw_expression_sums, kde=True, ax=axs[0], color='red', bins=30, alpha=0.7)
        axs[0].set_title("Expression Sums Distribution (Before Filtering)")
        axs[0].set_xlabel("Expression Sum")
        axs[0].set_ylabel("Frequency")

        # Histogram: Expression Sums (Filtered)
        sns.histplot(filtered_expression_sums, kde=True, ax=axs[1], color='green', bins=30, alpha=0.7)
        axs[1].set_title("Expression Sums Distribution (After Filtering)")
        axs[1].set_xlabel("Expression Sum")
        axs[1].set_ylabel("Frequency")

        plt.tight_layout()
        plt.show()