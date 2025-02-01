from Scraping import Scraping  # Assurez-vous que Scraping.py est dans le même dossier ou dans un dossier importable
from DataPreparation import DataPreparation  # Assurez-vous que data_preparation.py est dans le même dossier
from SalaryPredictionModel import SalaryPredictionModel  # Assurez-vous que SalaryPredictionModel.py est dans le même dossier ou importable

def main():
    # --- Partie Scraping ---
    # Chemin du WebDriver
    webdriver_path = "C:/Users/eyabe/Downloads/edgedriver_win64 (1)/msedgedriver.exe"

    # Initialiser la classe Scraping avec le chemin du WebDriver
    scraper = Scraping(webdriver_path)

    # Liste de titres de jobs et localisations
    job_location_list = [
        ('Data Scientist', 'New York'),
        ('Machine Learning Engineer', 'San Francisco'),
        ('AI Engineer', 'London'),
        ('Prographic Designer', 'Washington, DC'),
        ('Project Manager', 'Chicago, IL')
    ]

    # Scraper les données
    scraper.scrape_multiple_jobs_and_locations(job_location_list, num_pages=3)

    # Fermer le WebDriver après le scraping
    scraper.close_driver()

    # --- Partie Data Preparation ---
    input_folder = 'C:/Users/eyabe/Downloads/salary_prediction_prj/Data'
    output_combined_file = 'C:/Users/eyabe/Downloads/salary_prediction_prj/combined_jobs_dataset.csv'
    output_cleaned_file = 'C:/Users/eyabe/Downloads/salary_prediction_prj/cleaned_jobs_dataset.csv'
    
    # Créer une instance de la classe DataPreparation
    data_prep = DataPreparation(input_folder, output_combined_file, output_cleaned_file)

    # Combiner les fichiers CSV
    combined_df = data_prep.combine_csv_files()

    # Nettoyer les données
    cleaned_df = data_prep.clean_data(combined_df)

    # Sauvegarder les données nettoyées
    data_prep.save_cleaned_data(cleaned_df)

    # --- Partie Model Training & Prediction ---
    # Chemin vers le fichier des données nettoyées
    data_file = 'C:/Users/eyabe/Downloads/salary_prediction_prj/cleaned_jobs_dataset.csv'
    
    # Initialisation de la classe SalaryPredictionModel
    model = SalaryPredictionModel(data_file)
    
    # Entraîner et optimiser les modèles
    model.train_and_optimize()

    # Évaluer les modèles
    model.evaluate_models()

    # Sauvegarder le meilleur modèle
    model.save_best_model()

    # Charger le modèle sauvegardé (si nécessaire)
    model.load_model('best_model.pkl')

    # Exemple de prédiction pour de nouvelles données
    # Remplacez cette partie avec de nouvelles données à prédire
    new_data = model.X_test[:5]  # Par exemple, les 5 premières lignes du jeu de test
    predicted_salaries = model.predict_salary(new_data)
    
    print("\nPrédictions de salaire pour de nouvelles données :")
    print(predicted_salaries)

if __name__ == '__main__':
    main()
