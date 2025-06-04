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
    
    def common_probability(self, Einkommen, Alter, Kaufentscheidung):
        p_e = self.salary_prob.get(Einkommen, 0)
        p_a = self.age_prob.get(Alter, 0)
        p_k = self.purchase_decision_prob.get(Kaufentscheidung, 0)
        return p_e * p_a * p_k

    def purchase_probability(self, Einkauf):
        total = 0
        for Alter in self.age_prob:
            for Einkommen in self.salary_prob:
                total += self.common_probability(Einkommen, Alter, Einkauf)
        return total    

# Calculate probabilities from training data
P_Alter = df["Alter"].value_counts(normalize=True).to_dict()
P_Einkommen = df["Einkommen"].value_counts(normalize=True).to_dict()

# Conditional probabilities P(Einkauf | Alter, Einkommen)
grouped = df.groupby(["Alter", "Einkommen"])["Kaufentscheidung"].value_counts(normalize=True)
P_Einkauf = {}

for (Alter, Einkommen), dist in grouped.groupby(level=[0, 1]):
    P_Einkauf[(Alter, Einkommen)] = dist.droplevel([0, 1]).to_dict()

# Create model 
model = customer(P_Alter, P_Einkommen, P_Einkauf)

# Example
print("P(Einkauf = Apple):", round(model.purchase_probability("Apple"), 3))
print("P(Einkauf = Samsung):", round(model.purchase_probability("Samsung"), 3))




