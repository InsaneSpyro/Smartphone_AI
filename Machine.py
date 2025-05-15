# Import pandas libary to read the excel file with training data
import pandas as pd

df = pd.read_excel("Trainingsdaten.xlsx", engine="openpyxl")

def main():
    class customer:
        # Node for the customer type and their purchase decision
        def __init__(self, age, salary, purchase_decision):
            self.age = age 
            self.salary = salary 
            self.purchase_decision = purchase_decision
    





