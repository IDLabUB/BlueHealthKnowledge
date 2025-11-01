"""
Run analysis on collected words data.

This script loads the pre-computed counts object for the blue-health activity associations,
processes the data by dropping low-frequency components and normalizing scores,
and then extracts the top associations between terms. The results are saved as JSON files,
and the full normalized score matrix is exported as a CSV file with summary statistics printed.
"""

import os
import json
import numpy as np
import pandas as pd
from lisc.utils import SCDB, load_object

###################################################################################################
# Configuration settings

# Directories and file names for loading the counts object and term files
TERM_DIR = './terms'             # Directory for the term files (not directly used here)
DB_NAME = './data'               # Database directory where the counts object is stored
COG_F_NAME = 'counts_blue_health_activities'   # File name (without extension) for the blue-health activity counts object

# Parameters for analysis
N_TERMS = 3   # Number of top associations to extract for each term
N_DROP = 100  # Number of low-frequency items to drop before normalization

###################################################################################################

def main():
    """Main function to analyze counts data and export the top associations and scores."""
    
    print('\n\n ANALYZING COUNTS DATA \n\n')
    
    # Initialize the database object using SCDB.
    # This loads the directory structure and paths defined in DB_NAME.
    db = SCDB(DB_NAME)
    
    # Define the paths for saving the summary of counts and associations.
    # These directories will be created inside the counts directory of the database.
    counts_summary_path = os.path.join(db.paths['counts'], 'summary')
    counts_assocs_path = os.path.join(db.paths['counts'], 'assocs')
    
    # Create the summary and associations directories (recursively) if they do not already exist.
    for path in [counts_summary_path, counts_assocs_path]:
        os.makedirs(path, exist_ok=True)
    
    # Load the counts object for blue-health activities.
    # This object contains co-occurrence scores and term labels.
    print("Looking for the file at:", db.paths['counts'])
    cog_counts = load_object(COG_F_NAME, directory=db)
    
    # Pre-process the counts object:
    # 1. Drop low-frequency items.
    # 2. Compute normalized scores for dimension 'A'.
    cog_counts.drop_data(N_DROP)
    cog_counts.compute_score('normalize', dim='A')
    
    # Export the full normalized score matrix as a CSV file for further analysis.
    cog_scores_df = pd.DataFrame(cog_counts.score,
                                 index=cog_counts.terms['A'].labels,
                                 columns=cog_counts.terms['B'].labels)
    cog_csv_path = os.path.join(counts_summary_path, 'blue_health_activity_scores.csv')
    cog_scores_df.to_csv(cog_csv_path)
    print("Blue-health activity scores exported to:", os.path.abspath(cog_csv_path))
    
    # Print summary statistics for the score matrix.
    print("\nSummary statistics for blue-health activity scores:")
    print(cog_scores_df.describe())
    
    # For each term in the 'A' dimension, extract the top associations
    # from the co-occurrence scores and save them as JSON.
    for l_ind, label in enumerate(cog_counts.terms['A'].labels):
        # Initialize a dictionary to store top associations.
        top_assocs = {'top_assocs': []}
    
        # Extract the top N_TERMS associations from dimension 'B'.
        for t_ind, assoc in zip(range(N_TERMS), np.flip(np.argsort(cog_counts.score[l_ind, :]))):
            top_assocs['top_assocs'].append(cog_counts.terms['B'][assoc].label)
    
        # Save the top associations for the current 'A' term in a JSON file.
        summary_filepath = os.path.join(counts_summary_path, label + '.json')
        with open(summary_filepath, 'w') as outfile:
            json.dump(top_assocs, outfile)
    
    # Collect and save reverse associations: for each term in dimension 'B',
    # extract the top associated terms from dimension 'A'.
    associations = {}
    for l_ind, label in enumerate(cog_counts.terms['B'].labels):
        associations[label] = []
        for t_ind, assoc in zip(range(N_TERMS), np.flip(np.argsort(cog_counts.score[:, l_ind]))):
            associations[label].append(cog_counts.terms['A'][assoc].label)
    assocs_filepath = os.path.join(counts_assocs_path, 'associations.json')
    with open(assocs_filepath, 'w') as outfile:
        json.dump(associations, outfile)
    
    print('\n\n FINISHED ANALYZING COUNTS DATA \n\n')
    
if __name__ == "__main__":
    main()
