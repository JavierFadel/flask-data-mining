import pandas as pd

def load_dataset(path):
    """Loads a CSV file and returns it as a DataFrame."""
    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None