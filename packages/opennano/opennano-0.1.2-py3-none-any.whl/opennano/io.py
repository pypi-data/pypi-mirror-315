import os
import re
import json
import numpy as np
import pandas as pd
import anndata as ad
import glob


class GeoMxProcessor:
    """
    A class for processing NanoString GeoMx data.

    Combines file validation, parsing, and data integration into a single interface.
    """


    def __init__(self, dcc_files, pkc_file, metadata_file):
        """
        Initialize the `GeoMxProcessor` with paths to `.dcc`, `.pkc`, and GEO SOFT metadata files.

        Parameters
        ----------
        dcc_files : str
            Path to the directory containing `.dcc` files.
        pkc_file : str
            Path to the `.pkc` file.
        metadata_file : str
            Path to the GEO SOFT metadata file.

        Raises
        ------
        ValueError
            If the provided paths are invalid.
        """
        self.dcc_files = dcc_files
        self.pkc_file = pkc_file
        self.metadata_file = metadata_file
        self.dcc_data = {}
        self.pkc_data = {}
        self.metadata = None



    @staticmethod
    def read_dcc_files(file_path):
        """
        Parses `.dcc` files into structured data.

        Parameters
        ----------
        file_path : str
            Path to the directory containing `.dcc` files to parse.

        Returns
        -------
        dict
            Dictionary of dictionaries for sections of the `.dcc` file with keys:
            - "Header": Metadata from the header section.
            - "Scan_Attributes": Scan-specific metadata.
            - "NGS_Processing_Attributes": Processing-specific metadata.
            - "Code_Summary": DataFrame with RTS_IDs and counts.

        Raises
        ------
        FileNotFoundError
            If the specified `.dcc` files path is not found.
        ValueError
            If the files are not correctly formatted.

        Examples
        --------
        Example `.dcc` File Content:

        .. code-block:: text

           <Header>
            key1,value1
            key2,value2
            </Header>
            <Code_Summary>
            RTS001,10
            RTS002,20

        Parsing the File:

        .. code-block:: python

            dcc_data = GeoMxProcessor.read_dcc_files("path_to_DCC/")
            print(dcc_data["DCC_1"])
            # Output:
            # {'Header': 'values1', 'Scan_Attributes': 'values2', 
            #  'NGS_Processing_Attributes' : 'values3', 'Code_Summary' : 'values4'}

            print(dcc_data["DCC_1"]["Code_Summary"])
            # Output:
            #  RTS_ID  Count
            # 0  RTS001     10
            # 1  RTS002     20
        """
        # Creating dcc_data object
        dcc_directory = file_path + "*"
        dcc_data = {}

        # Running glob to retrieve files
        for file in glob.glob(dcc_directory):

            # Initialize dictionaries to store parsed data
            header = {}
            scan_attributes = {}
            ngs_processing_attributes = {}
            code_summary = []

            # Read the file line by line
            with open(file, 'r') as f:
                section = None
                for line in f:
                    line = line.strip()
                    # Identify sections
                    if line == "<Header>":
                        section = "header"
                    elif line == "<Scan_Attributes>":
                        section = "scan_attributes"
                    elif line == "<NGS_Processing_Attributes>":
                        section = "ngs_processing_attributes"
                    elif line == "<Code_Summary>":
                        section = "code_summary"
                    elif line.startswith("</") and section:
                        section = None
                    elif section:
                        # Parse each section line by line
                        if section == "header":
                            key, value = line.split(",", 1)
                            header[key.strip()] = value.strip().strip('"')
                        elif section == "scan_attributes":
                            key, value = line.split(",", 1)
                            scan_attributes[key.strip()] = value.strip()
                        elif section == "ngs_processing_attributes":
                            key, value = line.split(",", 1)
                            ngs_processing_attributes[key.strip()] = value.strip()
                        elif section == "code_summary":
                            # Parse RTS_ID and Count, handling potential errors
                            try:
                                rts_id, count = line.split(",", 1)
                                code_summary.append(
                                    {'RTS_ID': rts_id.strip(), 'Count': int(count.strip())})
                            except ValueError:
                                print(
                                    f"Warning: Skipping malformed line in Code_Summary: {line}")

            # Convert Code Summary to DataFrame for easier manipulation
            if code_summary:
                code_summary_df = pd.DataFrame(code_summary)
            else:
                # Fallback to an empty DataFrame if Code Summary has no valid
                # entries
                code_summary_df = pd.DataFrame(columns=['RTS_ID', 'Count'])

            # Return all parsed data
            dcc_data[file.split("/")[-1]] = {
                'Header': header,
                'Scan_Attributes': scan_attributes,
                'NGS_Processing_Attributes': ngs_processing_attributes,
                'Code_Summary': code_summary_df
            }
        
        return dcc_data


    def parse_dcc_files(self):
        """
        Parses all `.dcc` files in the specified directory and stores their content.

        This method validates that the `self.dcc_files` attribute points to a valid directory, 
        then uses the `read_all_dcc_files` method to parse all `.dcc` files in the directory. 
        The parsed content is stored in the `self.dcc_data` attribute for further processing.

        Parameters
        ----------
        None
            This method operates on the `self.dcc_files` attribute, which should contain the path 
            to the directory with `.dcc` files.

        Returns
        -------
        None
            The parsed `.dcc` file data is stored in the `self.dcc_data` attribute as a dictionary.

        Raises
        ------
        ValueError
            If the `self.dcc_files` attribute is not a valid directory.

        Notes
        -----
        This method relies on `read_all_dcc_files` to perform the parsing of `.dcc` files.

        The parsed data is structured as a dictionary, with `.dcc` file names as keys and 
        the parsed content as values.
        
        """
        import os

        # Validate that self.dcc_files is a directory
        if not os.path.isdir(self.dcc_files):
            raise ValueError(f"Provided .dcc path is not a directory: {self.dcc_files}")

        # Use read_all_dcc_files to parse the directory
        self.dcc_data = self.read_dcc_files(self.dcc_files)



    @staticmethod
    def read_pkc(file_path):
        """
        Parses a `.pkc` file into a dictionary of probe information.

        Parameters
        ----------
        file_path : str
            Path to the `.pkc` file to parse.

        Returns
        -------
        dict
            Dictionary where keys are gene names, and values are lists of probe dictionaries.

        Raises
        ------
        FileNotFoundError
            If the `.pkc` file does not exist.
        JSONDecodeError
           If the `.pkc` file is not valid JSON.

        Examples
        --------
        Example `.pkc` File Content:

        .. code-block:: json

           {
               "Targets": [
                 {"DisplayName": "Gene1", "Probes": [{"RTS_ID": "RTS001", "ProbeID": "P001"}]},
                 {"DisplayName": "Gene2", "Probes": [{"RTS_ID": "RTS002", "ProbeID": "P002"}]}
                ]
            }

        Parsing the File:

        .. code-block:: python

           pkc_data = GeoMxProcessor.read_pkc("probes.pkc")
            print(pkc_data["Gene1"])
            # Output:
            # [{'RTS_ID': 'RTS001', 'ProbeID': 'P001'}]
            
        """
        
        pkc = {}
        with open(file_path, 'r') as file:
            pkc_data = json.load(file)
        for target in pkc_data.get("Targets", []):
            gene_name = target.get("DisplayName")
            if gene_name:
                pkc[gene_name] = target.get("Probes", [])
        return pkc

    def parse_pkc_file(self):
        """
        Parse the .pkc file and store its content using read_pkc.
        """
        print(f"Parsing {self.pkc_file}...")
        self.pkc_data = self.read_pkc(self.pkc_file)
        print("Probe file parsed successfully.")



    @staticmethod
    def parse_geo_soft_metadata_with_identifier(file_path):
        """
        Parses a GEO SOFT metadata file to extract series and sample metadata.

        Parameters
        ----------
        file_path : str
            Path to the GEO SOFT format metadata file.

        Returns
        -------
        tuple
            - series_metadata (dict): General series-level metadata.
            - sample_metadata_df (pandas.DataFrame): Sample-specific metadata with structured characteristics.

        Raises
        ------
        FileNotFoundError
            If the metadata file is not found.
        ValueError
            If the file is not in the correct GEO SOFT format.

        Examples
        --------
        Example GEO SOFT Metadata File:

        .. code-block:: text

            ^SERIES = GSE12345
            !Series_title = Example Series
            ^SAMPLE = GSM123456
            !Sample_title = Sample 1
            !Sample_description = DSP-123-A-S1

        Parsing the File:

        .. code-block:: python

           series_metadata, sample_metadata = GeoMxProcessor.parse_geo_soft_metadata_with_identifier("metadata.txt")
            print(series_metadata)
            # Output:
            # {'^SERIES': 'GSE12345', '!Series_title': 'Example Series'}

            print(sample_metadata)
            # Output:
            #   Sample_ID   !Sample_title     !Sample_description
            # 0  GSM123456     Sample 1          DSP-123-A-S1
            
        """    
        series_metadata = {}
        sample_data = []
        current_sample = {}
        in_sample_section = False

        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()

                # Detect series-level metadata
                if line.startswith("^SERIES") or line.startswith("!Series_"):
                    key, value = line.split(" = ", 1)
                    series_metadata[key] = value

                # Start of a new sample section
                elif line.startswith("^SAMPLE ="):
                    if current_sample:
                        sample_data.append(current_sample)
                    current_sample = {'Sample_ID': line.split(" = ")[1]}
                    in_sample_section = True

                # Process sample-specific metadata
                elif in_sample_section:
                    if line.startswith("!Sample_") and not line.startswith("!Sample_characteristics_ch1"):
                        key, value = line.split(" = ", 1)
                        # Capture only the identifier format in `Sample_description`
                        if key == "!Sample_description" and re.match(r"^DSP-\d+-[A-Z]-\w+$", value):
                            current_sample["!Sample_description"] = value
                        elif key not in current_sample:
                            current_sample[key] = value
                    
                    # Capture characteristics in a structured format
                    elif line.startswith("!Sample_characteristics_ch1"):
                        characteristic_line = line.split(" = ", 1)[1]
                        if ":" in characteristic_line:
                            characteristic, value = characteristic_line.split(":", 1)
                            current_sample[characteristic.strip()] = value.strip()

            # Append the last sample
            if current_sample:
                sample_data.append(current_sample)

        # Convert sample data to DataFrame
        sample_metadata_df = pd.DataFrame(sample_data)

        return series_metadata, sample_metadata_df

    def parse_metadata(self):
        """
        Parses the GEO SOFT metadata file and stores its content.

        This method uses the `parse_geo_soft_metadata_with_identifier` function to process 
        the GEO SOFT metadata file specified in the `self.metadata_file` attribute. The parsed 
        content is stored in the `self.series_metadata` and `self.metadata` attributes.

        Parameters
        ----------
        None
            This method operates on the `self.metadata_file` attribute, which should contain the path 
            to the GEO SOFT metadata file.

        Returns
        -------
        None
            The parsed metadata is stored in the `self.series_metadata` (series-level metadata) and 
            `self.metadata` (sample-level metadata as a pandas DataFrame) attributes.

        Raises
        ------
        FileNotFoundError
            If the specified metadata file does not exist.
        ValueError
            If the metadata file is not in the correct GEO SOFT format.


        Notes
        -----
        
        - The series-level metadata (e.g., general information about the series) is stored as a dictionary in `self.series_metadata`.
        - The sample-level metadata (e.g., details about individual samples) is stored as a pandas DataFrame in `self.metadata`.
        - This method is part of the high-level data integration workflow and assumes that the metadata file exists and is formatted correctly.
        
        """
        print(f"Parsing {self.metadata_file}...")
        self.series_metadata, self.metadata = self.parse_geo_soft_metadata_with_identifier(self.metadata_file)
        print("Metadata file parsed successfully.")


    @staticmethod
    def create_single_anndata(dcc_data, pkc_data, sample_metadata_df):
        """
        Creates a single AnnData object with RTS_IDs as observations (obs) and ROIs (samples) as variables (vars).

        This function integrates parsed `.dcc` files, `.pkc` probe information, and GEO SOFT metadata
        to construct an `AnnData` object. The resulting `AnnData` object contains:

        - `obs`: Information about RTS_IDs (features).
        - `var`: Information about samples (ROIs).
        - `X`: Expression counts aligned by RTS_IDs and ROIs.
        - `uns`: Unstructured metadata for further analysis.

        Parameters
        ----------
        dcc_data : dict
           A dictionary where keys are file names of `.dcc` files, and values are parsed dictionaries.
           Each parsed dictionary should include a `Code_Summary` DataFrame containing `RTS_ID` and `Count`.
        pkc_data : dict
            A dictionary where keys are gene names and values are lists of probe dictionaries.
            Each probe dictionary should include fields like `RTS_ID`, `SystematicName`, `GeneID`, and `ProbeID`.
        sample_metadata_df : pandas.DataFrame
            A DataFrame containing sample-level metadata parsed from GEO SOFT files.
            Each row should represent a sample and must include the column specified by `description_col`.
        description_col : str, optional
            The column name in `sample_metadata_df` that contains the descriptions matching `.dcc` filenames.
            Default is `"!Sample_description"`.

        Returns
        -------
        ad.AnnData
            An `AnnData` object where:
            - `obs` contains RTS_ID-level metadata.
            - `var` contains ROI-level (sample-level) metadata.
            - `X` contains expression counts.
            - `uns` contains unstructured metadata mapped to samples.

        Raises
        ------
        KeyError
            If required columns like `RTS_ID` or `Count` are missing in `dcc_data` or `pkc_data`.
        ValueError
           If there are mismatches between `.dcc` data and metadata descriptions.

        Examples
        --------
        Example Data Structure:

        .. code-block:: python

            dcc_data = {
               "sample1.dcc": {
                    "Code_Summary": pd.DataFrame({
                        "RTS_ID": ["RTS001", "RTS002"],
                        "Count": [10, 20]
                   })
               }
            }
            pkc_data = {
                "Gene1": [{"RTS_ID": "RTS001", "ProbeID": "P001", "GeneID": "G1"}, {"RTS_ID": "RTS002", "ProbeID": "P002", "GeneID": "G1"}],
                "Gene2": [{"RTS_ID": "RTS003", "ProbeID": "P003", "GeneID": "G2"}]
            }
           sample_metadata_df = pd.DataFrame({
               "!Sample_description": ["DSP-123-A-S1", "DSP-123-A-S2"],
                "!Sample_title": ["Sample 1", "Sample 2"]
            })
            adata = GeoMxProcessor.create_single_anndata(dcc_data, pkc_data, sample_metadata_df)
            print(adata)

        Expected Output:

        .. code-block:: text

            AnnData object with n_obs × n_vars = 3 × 2
        """
 
        # Normalize RTS_ID in pkc_data to ensure consistent formatting
        for i in pkc_data.keys():
            for j in range(0, len(pkc_data[i])):
                pkc_data[i][j]["RTS_ID"] = pkc_data[i][j]["RTS_ID"].strip().upper()

        flattened_data_cleaned = []
        for gene, probes in pkc_data.items():
            for probe in probes:
                probe_cleaned = probe.copy()
                probe_cleaned['Gene'] = gene
                # Flatten lists to strings
                for key in ['SystematicName', 'Accession', 'GenomeCoordinates', 'GeneID']:
                    if key in probe_cleaned and isinstance(probe_cleaned[key], list):
                        probe_cleaned[key] = ', '.join(map(str, probe_cleaned[key]))
                flattened_data_cleaned.append(probe_cleaned)
        
        # Create a DataFrame from the cleaned flattened data
        pkc_df = pd.DataFrame(flattened_data_cleaned)
        pkc_df.set_index('ProbeID', inplace=True)
        pkc_df.loc[pkc_df["Gene"] == "NegProbe-WTX", "SystematicName"] = pkc_df.loc[pkc_df["Gene"] == "NegProbe-WTX", "DisplayName"]
        

        combined_obs = None
        var_labels = []
        sample_metadata_list = []
        sample_names = []
        sample_titles = []
        counts_dict = {}

        for dcc_filename, dcc_content in dcc_data.items():
            
            # Extract sample description from the filename
            match = re.search(r'(GSM\d+)_(DSP-\d+-[A-Z]-\w+)\.dcc$', dcc_filename)
            if match:
                sample_description = match.group(1).strip()
                matched_rows = sample_metadata_df[sample_metadata_df["!Sample_geo_accession"].str.strip() == sample_description]

                if not matched_rows.empty:
                    sample_info = matched_rows.iloc[0].to_dict()
                    sample_title = sample_info.get('!Sample_title', None)
                    roi_x = sample_info.get('roi x coordinate', None)
                    roi_y = sample_info.get('roi y coordinate', None)
                    if roi_x != None and roi_y != None:
                        roi_label = f"ROI:{roi_x}-{roi_y}"
                    else:
                        roi_label = sample_info.get('!Sample_title', None)

                    code_summary_df = dcc_content.get('Code_Summary')
                    if isinstance(code_summary_df, pd.DataFrame) and 'RTS_ID' in code_summary_df.columns:
                        code_summary_df['RTS_ID'] = code_summary_df['RTS_ID'].str.strip().str.upper()
                        relevant_rts_ids = set(code_summary_df['RTS_ID'].unique())
                        matched_probes_df = pkc_df[pkc_df['RTS_ID'].isin(set(code_summary_df["RTS_ID"]))]
                        final_matched_df = code_summary_df.merge(matched_probes_df, on='RTS_ID', how='inner')

                        if not final_matched_df.empty:
                            counts_dict[roi_label] = final_matched_df.set_index('RTS_ID')['Count']

                            if combined_obs is None:
                                combined_obs = final_matched_df[['RTS_ID', 'SystematicName', 'GeneID', 'GenomeCoordinates']].drop_duplicates()

                            var_labels.append(roi_label)
                            sample_names.append(dcc_filename)
                            sample_titles.append(sample_title)
                            sample_metadata_list.append(sample_info)
                        else:
                            print(f"Warning: No matched probes found for sample {dcc_filename}")
                    else:
                        print(f"Warning: 'RTS_ID' column missing in Code_Summary for {dcc_filename}")
                else:
                    print(f"Warning: No metadata match found for sample description '{sample_description}' from .dcc file '{dcc_filename}'")
            else:
                print(f"Warning: Could not extract description from .dcc file name '{dcc_filename}'")

        if counts_dict:
            all_rts_ids = pd.Index(set().union(*[counts.index for counts in counts_dict.values()]))
            aligned_counts = []
            for roi_label in var_labels:
                counts = counts_dict[roi_label].reindex(all_rts_ids, fill_value=0)
                aligned_counts.append(counts)

            X = np.column_stack(aligned_counts)
            obs = combined_obs.set_index('RTS_ID').reindex(all_rts_ids).reset_index()
            obs = obs.rename(columns={'index': 'RTS_ID'})
            obs = obs.set_index('RTS_ID')

            # Create var DataFrame with ROI coordinate labels and sample names
            var = pd.DataFrame({'Sample_Name': dcc_filename, "Sample_Title" : sample_titles}, index=var_labels)

            adata = ad.AnnData(X=X, obs=obs, var=var)

            metadata_dict = {}
            for roi_label, sample_info in zip(var_labels, sample_metadata_list):
                metadata_dict[roi_label] = sample_info

            adata.uns = metadata_dict

            if any(adata.obs["SystematicName"].isna() == True):
                adata = adata[~adata.obs['SystematicName'].isna()]
            # Replace "NegProbe-WTX_*" with "NegProbe-WTX"
            adata.obs.loc[adata.obs["SystematicName"].str.startswith("NegProbe-WTX"), "SystematicName"] = \
            adata.obs.loc[adata.obs["SystematicName"].str.startswith("NegProbe-WTX"), "SystematicName"].str.replace(r'_\d+$', '', regex=True)
            
            return adata
        else:
            print("Warning: No data combined into AnnData object.")
            return None

    def process(self):
        """
        High-level method to process GeoMx data and create an `AnnData` object.

        This method serves as a single entry point for parsing and integrating GeoMx data. 
        It orchestrates the following steps:
    
        1. Parses `.dcc` files to extract code summary and metadata.
        2. Parses `.pkc` files to retrieve probe information.
        3. Parses GEO SOFT metadata files for series and sample metadata.
        4. Combines all parsed data into a unified `AnnData` object.

        Returns
        -------
        AnnData
            A unified `AnnData` object containing:
            - `obs`: Metadata about RTS_IDs (features).
            - `var`: Metadata about ROIs (regions of interest or samples).
            - `X`: Expression counts aligned by RTS_IDs and ROIs.
            - `uns`: Unstructured metadata for further analysis.

        Raises
        ------
        ValueError
           If any of the required files (`dcc_files`, `pkc_file`, or `metadata_file`) are invalid or not properly formatted.

        Notes
        -----
        This method leverages three internal parsing methods:
        - `parse_dcc_files`: Parses and validates `.dcc` files.
        - `parse_pkc_file`: Parses and validates `.pkc` files.
        - `parse_metadata`: Extracts metadata from GEO SOFT files.

        The final `AnnData` object is created using `GeoMxProcessor.create_single_anndata`, 
        which integrates all parsed data into a single, consistent format for downstream analysis.

        Examples
        --------
        Process GeoMx data and generate an `AnnData` object:

        .. code-block:: python

            processor = GeoMxProcessor(
                dcc_files="path/to/dcc_directory",
                pkc_file="path/to/probes.pkc",
                metadata_file="path/to/metadata.txt"
            )
            adata = processor.process()
            print(adata)
            # Output: AnnData object with n_obs × n_vars = 100 × 10
        """
        self.parse_dcc_files()
        self.parse_pkc_file()
        self.parse_metadata()
        return GeoMxProcessor.create_single_anndata(
            self.dcc_data,
            self.pkc_data,
            self.metadata
        )