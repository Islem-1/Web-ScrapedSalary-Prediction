from flask import Flask, render_template, request, send_file
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

app = Flask(__name__)

# Charger les modèles et le scaler
try:
    best_model = joblib.load('model/best_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    dummy_columns = joblib.load('model/dummy_columns.pkl')
except FileNotFoundError:
    raise Exception("Les fichiers nécessaires (modèle ou scaler) sont introuvables.")

# Charger les données pour récupérer les options
data = pd.read_csv('cleaned_jobs_dataset.csv')

# Prétraiter les données d'entrée utilisateur
def preprocess_inputs(job_title, company, country, experience):
    user_data = pd.DataFrame({
        'Job Title': [job_title],
        'Company': [company],
        'Nom du pays': [country],
        'Experience Required': [experience]
    })

    user_data_encoded = pd.get_dummies(user_data)
    
    for col in dummy_columns:
        if col not in user_data_encoded.columns:
            user_data_encoded[col] = 0
    
    user_data_encoded = user_data_encoded.reindex(columns=dummy_columns, fill_value=0)
    user_data_scaled = scaler.transform(user_data_encoded)
    
    return user_data_scaled

# Route principale pour afficher l'index
@app.route('/')
def index():
    return render_template('index.html', job_titles=data['Job Title'].unique(),
                           companies=data['Company'].unique(),
                           countries=data['Nom du pays'].unique())

# Route pour afficher le formulaire
@app.route('/form')
def form():
    return render_template('form.html', job_titles=data['Job Title'].unique(),
                           companies=data['Company'].unique(),
                           countries=data['Nom du pays'].unique())

# Route pour effectuer la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        job_title = request.form['job_title']
        company = request.form['company']
        country = request.form['country']
        experience = int(request.form['experience'])
        
        try:
            # Prétraitement des données utilisateur
            user_inputs = preprocess_inputs(job_title, company, country, experience)
            
            # Prédiction du salaire
            predicted_salary = best_model.predict(user_inputs)[0]
            prediction_text = f"Le salaire prédit pour ce poste est : {predicted_salary:.2f} euros par an."
            return render_template('index.html', prediction_text=prediction_text, 
                                   job_titles=data['Job Title'].unique(),
                                   companies=data['Company'].unique(),
                                   countries=data['Nom du pays'].unique())
        except Exception as e:
            error_text = f"Une erreur s'est produite : {str(e)}"
            return render_template('index.html', error_text=error_text,
                                   job_titles=data['Job Title'].unique(),
                                   companies=data['Company'].unique(),
                                   countries=data['Nom du pays'].unique())

# Route pour afficher le graphique des prédictions de salaires par pays
@app.route('/plot/salary_by_country')
def salary_by_country():
    # Obtenir la liste des pays
    country_columns = [col for col in dummy_columns if col.startswith('Nom du pays_')]
    countries = [col.replace('Nom du pays_', '') for col in country_columns]

    # Créer un tableau pour stocker les prédictions moyennes par pays
    predicted_salaries_by_country = []

    for country_column in country_columns:
        # Créer une entrée d'entrée vide pour chaque pays
        input_data = np.zeros((1, len(dummy_columns)))
        
        # Activer le pays correspondant dans les colonnes encodées
        country_index = dummy_columns.index(country_column)
        input_data[0, country_index] = 1  # Active la colonne du pays
        
        # Faire la prédiction avec le modèle sauvegardé
        scaled_input_data = scaler.transform(input_data)
        salary_pred = best_model.predict(scaled_input_data)
        
        # Ajouter la prédiction à la liste
        predicted_salaries_by_country.append(salary_pred[0])

    # Créer un DataFrame pour stocker les résultats
    salary_country_df = pd.DataFrame({'Pays': countries, 'Salaire Prédit': predicted_salaries_by_country})

    # Trier les pays par salaire prédit en ordre décroissant
    salary_country_df = salary_country_df.sort_values(by='Salaire Prédit', ascending=False)

    # Créer le graphique dans une route Flask
    plt.figure(figsize=(8, 5))
    plt.bar(salary_country_df['Pays'], salary_country_df['Salaire Prédit'], color='skyblue')
    plt.title("Prédictions de Salaire Moyenne par Pays")
    plt.xlabel("Pays")
    plt.ylabel("Salaire Prédit (€)")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Sauvegarder le graphique dans un buffer en mémoire
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    plt.close()

    # Retourner l'image générée au frontend
    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
