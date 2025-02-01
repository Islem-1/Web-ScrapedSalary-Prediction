import os
import pandas as pd
import re

class DataPreparation:  # Correction du nom de la classe
    def __init__(self, input_folder, output_combined_file, output_cleaned_file):
        self.input_folder = input_folder
        self.output_combined_file = output_combined_file
        self.output_cleaned_file = output_cleaned_file

    def combine_csv_files(self):
        # Liste des fichiers CSV dans le répertoire d'entrée
        csv_files = [file for file in os.listdir(self.input_folder) if file.endswith('.csv')]
        
        # Liste pour stocker les DataFrames
        df_list = []

        # Combiner les fichiers CSV avec ajout du nom du pays
        for file in csv_files:
            country_name = file.split('.')[0]  # Extraire le pays du nom du fichier
            file_path = os.path.join(self.input_folder, file)
            df = pd.read_csv(file_path)
            df['Nom du pays'] = country_name  # Ajouter la colonne 'Nom du pays'
            df_list.append(df)

        # Combiner tous les DataFrames
        combined_df = pd.concat(df_list, ignore_index=True)

        # Sauvegarder le dataset combiné
        combined_df.to_csv(self.output_combined_file, index=False)
        print(f"Fichier combiné sauvegardé dans : {self.output_combined_file}")
        return combined_df

    def extract_min_salary(self, salary):
        # Vérifier si la valeur est une chaîne
        if isinstance(salary, str):
            match = re.findall(r'\d+(?:,\d+)?', salary)
            if match:
                return float(match[0].replace(',', ''))  # Utiliser le premier nombre comme salaire minimum
        # Retourner 0.0 pour les cas où le salaire est invalide ou manquant
        return 0.0

    def extract_experience(self, exp):
        # Vérifier si l'expérience est sous forme de chaîne ou d'entier
        exp = str(exp)  # Convertir en chaîne si c'est un entier
        match = re.search(r'\d+', exp)
        return int(match.group()) if match else 0

    def clean_data(self, combined_df):
        # Remplacer les valeurs manquantes ou non spécifiées par des valeurs par défaut
        combined_df['Salary'] = combined_df['Salary'].replace('Salary Not Listed', 'Unknown').fillna('Unknown')
        combined_df['Experience Required'] = combined_df['Experience Required'].fillna('0')
        combined_df['Job Type'] = combined_df['Job Type'].replace('Job Type Not Listed', 'Unknown').fillna('Unknown')
        combined_df['Company'] = combined_df['Company'].replace('Company Not Listed', 'Unknown').fillna('Unknown')

        # Appliquer l'extraction des salaires et convertir en float
        combined_df['Salary'] = combined_df['Salary'].apply(self.extract_min_salary)

        # Convertir "Experience Required" en années numériques
        combined_df['Experience Required'] = combined_df['Experience Required'].apply(self.extract_experience)

        # Ajouter une colonne 'Nom du pays' si elle n'existe pas déjà
        if 'Nom du pays' not in combined_df.columns:
            combined_df['Nom du pays'] = 'Unknown'  # Par défaut si la colonne n'existe pas, mais normalement elle devrait déjà y être.

        return combined_df

    def save_cleaned_data(self, cleaned_df):
        cleaned_df.to_csv(self.output_cleaned_file, index=False)
        print(f"Données nettoyées enregistrées dans : {self.output_cleaned_file}")
