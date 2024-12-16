import pandas as pd
import numpy as np

class SEC_data:
    def __init__(self, filenames):
        self.data = []
        for filename in filenames:
            df = pd.read_csv(filename, encoding='utf-16', sep='\t', skiprows=2)
            self.data.append(df)

    def rename_columns(self):
        for i, df in enumerate(self.data):
            new_columns = ['Volume_ml', 'Absorbance_mAU'] + [f'Unnamed_{j}' for j in range(len(df.columns) - 2)]
            df.columns = new_columns

    def normalize(self):
        for df in self.data:
            df['Normalized_Absorbance_mAU'] = (df['Absorbance_mAU'] - df['Absorbance_mAU'].min()) / (df['Absorbance_mAU'].max() - df['Absorbance_mAU'].min())

    def dataframes_to_arrays(self):
        for i, df in enumerate(self.data):
            self.data[i] = df.iloc[:, :2].to_numpy()


    def adjust_baseline(self, output_filename=None, baseline_range=(0, 20), export=True):
        """
        Adjusts the baseline of each dataset to start at zero using a specified range of Volume_ml,
        overwrites the Absorbance_mAU column, creates a new DataFrame, and optionally exports it as a CSV file.
    
        :param sec_data: SECData object containing the data
        :param output_filename: Optional; Name of the CSV file to export. Required if export=True
        :param baseline_range: Tuple of (min, max) Volume_ml values to use for baseline calculation
        :param export: Boolean flag indicating whether to export the data to CSV
        :return: Combined DataFrame with adjusted data
        :raises ValueError: If export=True but output_filename is None
        """
        # Validate parameters
        if export and output_filename is None:
            raise ValueError("output_filename must be provided when export=True")
            
        adjusted_data = []
    
        for df in self.data:
            # Select data within the specified Volume_ml range for baseline calculation
            baseline_data = df[(df['Volume_ml'] >= baseline_range[0]) & (df['Volume_ml'] <= baseline_range[1])]
        
            # Calculate the baseline as the minimum Absorbance_mAU in the selected range
            baseline = baseline_data['Absorbance_mAU'].min()
        
            # Create a copy of the DataFrame to avoid modifying the original
            adjusted_df = df.copy()
        
            # Adjust the Absorbance_mAU by subtracting the baseline and ensure no negative values
            adjusted_df['Absorbance_mAU'] = (adjusted_df['Absorbance_mAU'] - baseline).clip(lower=0)
        
            adjusted_data.append(adjusted_df)
    
        # Combine all adjusted dataframes
        combined_df = pd.concat(adjusted_data, ignore_index=True)
    
        # Add two placeholder rows at the beginning
        placeholder_rows = pd.DataFrame({col: ['Placeholder'] * 2 for col in combined_df.columns})
        combined_df = pd.concat([placeholder_rows, combined_df], ignore_index=True)
    
        # Ensure 'Volume_ml' and 'Absorbance_mAU' are the first two columns
        first_columns = ['Volume_ml', 'Absorbance_mAU']
        other_columns = [col for col in combined_df.columns if col not in first_columns]
        combined_df = combined_df[first_columns + other_columns]
    
        # Export to CSV if requested
        if export:
            combined_df.to_csv(output_filename, index=False)
            print(f"Adjusted data exported to {output_filename}")
    
        return combined_df