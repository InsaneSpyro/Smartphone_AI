# Importierung der benötigten Bibliotheken
import pandas as pd
import csv 

# Excel Datei einlesen
df = pd.read_excel("Trainingsdaten.xlsx", engine="openpyxl")
df.to_csv("Trainingsdaten.csv", index=False)

# Excel Datei zu CSV umwandeln
with open("Trainingsdaten.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

# Spaltennamen Python freundlich machen
df.columns = ["Einkommen", "Alter", "Kaufentscheidung"]

# Spalten festlegen
df["Einkommen"] = df["Einkommen"].map({1: "Hoch", 0: "Niedrig"})
df["Alter"] = df["Alter"].map({1: "Jung", 0: "Alt"})
df["Kaufentscheidung"] = df["Kaufentscheidung"].map({1: "Apple", 0: "Android"})

# Wahrscheinlichkeiten für Alter und Einkommen berechnen
P_Alter = df["Alter"].value_counts(normalize=True).to_dict()
P_Einkommen = df["Einkommen"].value_counts(normalize=True).to_dict()

# Berechnung der bedingten Wahrscheinlichkeiten: P(Kaufentscheidung | Alter, Einkommen)
grouped = df.groupby(["Alter", "Einkommen"])["Kaufentscheidung"].value_counts(normalize=True)
P_Kauf = {}
for (alter, einkommen), dist in grouped.groupby(level=[0, 1]):
    P_Kauf[(alter, einkommen)] = dist.droplevel([0, 1]).to_dict()

# Customer Klasse mit den Wahrscheinlichkeitsverteilungen
class customer:
    # Konstruktor: nimmt Wahrscheinlichkeiten für Alter, Einkommen und Kaufentscheidung entgegen
    def __init__(self, alter_prob, einkommen_prob, entscheidung_prob):
        self.alter_prob = alter_prob # (Jung, Alt)
        self.einkommen_prob = einkommen_prob # (Niedrig, Hoch)
        self.entscheidung_prob = entscheidung_prob # (Android, Apple)
    
     # Methode zur Berechnung der Wahrscheinlichkeiten ob Apple oder Android gekauft wird
    def vorhersage(self, alter, einkommen):
        result = {}
        for entscheidung in ["Apple", "Android"]:
            p_a = self.alter_prob.get(alter)
            p_e = self.einkommen_prob.get(einkommen)
            p_k = self.entscheidung_prob.get((alter, einkommen), {}).get(entscheidung, 0)
            result[entscheidung] = p_a * p_e * p_k
        # In Prozent umwandeln
        gesamt = sum(result.values())
        if gesamt > 0:
            for k in result:
                result[k] = round(100 * result[k] / gesamt, 2)
        return result

# Modell erzeugen
modell = customer(P_Alter, P_Einkommen, P_Kauf)

# Informationen der Personen abfragen
alter_input = input("Wie ist das Alter der Person?: ")
einkommen_input = input("Wie hoch ist das Einkommen der Person?: ")

# Eingaben umwandeln
alter = "Jung" if alter_input == "1" else "Alt"
einkommen = "Hoch" if einkommen_input == "1" else "Niedrig"

# Berechnung der Wahrscheinlichkeit anhand den Benutzereingaben
wahrscheinlichkeiten = modell.vorhersage(alter, einkommen)

# Ergebnis ausgeben
print(f"\nBasierend auf den Eingaben (Alter = {alter}, Einkommen = {einkommen}):")
for entscheidung, prozent in wahrscheinlichkeiten.items():
    print(f"- Wahrscheinlichkeit für {entscheidung}: {prozent}%")




