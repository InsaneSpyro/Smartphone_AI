# Import pandas libary to read the excel file with training data
import pandas as pd

df = pd.read_excel("Trainingsdaten.xlsx", engine="openpyxl")

class customer:
    # Node for the customer type and their purchase decision
    def __init__(self, age, salary, purchase_decision):
        self.age = age # (Jung, Alt)
        self.salary = salary # (Niedrig, Hoch)
        self.purchase_decision = purchase_decision # (Samsung, Apple)
    





