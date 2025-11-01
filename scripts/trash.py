import pickle
import pandas as pd

# Configure Pandas to display all rows and columns
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def load_and_display_counts(file_path):
    """
    Carrega l'objecte Counts des del fitxer indicat i imprimeix la informació:
      - Tipus d'objecte carregat.
      - Termes de la dimensió A i B.
      - DataFrame amb la matriu de comptes.
    Retorna una tupla (counts, data_df).
    """
    with open(file_path, 'rb') as file:
        counts = pickle.load(file)
    
    print("Objecte carregat:", type(counts))
    print("Terms (dim A):", counts.terms['A'].labels)
    print("Terms (dim B):", counts.terms['B'].labels)
    
    data = counts.counts
    data_df = pd.DataFrame(data, index=counts.terms['A'].labels, columns=counts.terms['B'].labels)
    
    print("\nDataFrame complet:")
    print(data_df)
    
    return counts, data_df

# Definim els camins dels fitxers per a activitats i mètriques d'exposició
activities_file = './data/counts/counts_blue_health_activities.p'
exposure_file = './data/counts/counts_blue_health_exposure_metrics.p'

print("=== Loading blue-health activity counts ===")
activities_counts, activities_df = load_and_display_counts(activities_file)

print("\n=== Loading blue-health exposure metric counts ===")
exposure_counts, exposure_df = load_and_display_counts(exposure_file)

import pickle
with open(activities_file, "rb") as f:
    obj = pickle.load(f)

print(type(obj))
print(dir(obj))
print(obj.terms["B"].labels)
