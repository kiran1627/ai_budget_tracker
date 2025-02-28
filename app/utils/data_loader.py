import pandas as pd

def load_data():
    """Load government expenditure, schemes, and budget data."""
    expenditure_df = pd.read_csv("data/expenditure.csv")
    schemes_df = pd.read_csv("data/schemes.csv")
    budget_df = pd.read_csv("data/budget_at_a_glance.csv")

    return expenditure_df, schemes_df, budget_df
