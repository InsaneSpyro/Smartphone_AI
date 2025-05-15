# Import pandas libary to read the excel file with training data
import pandas as pd

# Read Excel file 
df = pd.read_excel("Trainingsdaten.xlsx", engine="openpyxl")

# Make column names Python code friendly
df.columns = ["Einkommen", "Alter", "Kaufentscheidung"]
df["Einkommen"] = df["Einkommen"].map({1: "Hoch", 0: "Niedrig"})
df["Alter"] = df["Alter"].map({1: "Jung", 0: "Alt"})
df["Kaufentscheidung"] = df["Kaufentscheidung"].map({1: "Apple", 0: "Samsung"})

# Customer class with probabilities
class customer:
    # Node for the customer type and their purchase decision
    def __init__(self, age_prob, salary_prob, purchase_decision_prob):
        self.salary_prob = salary_prob # (Niedrig, Hoch)
        self.age_prob = age_prob # (Jung, Alt)
        self.purchase_decision_prob = purchase_decision_prob # (Samsung, Apple)
    





