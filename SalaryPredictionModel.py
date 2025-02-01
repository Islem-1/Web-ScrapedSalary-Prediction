import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
import joblib

class SalaryPredictionModel:
    def __init__(self, data_file):
        # Charger les données nettoyées depuis le fichier
        self.data = pd.read_csv(data_file)
        
        # Préparer les features et la target
        self.X = pd.get_dummies(self.data[['Job Title', 'Company', 'Experience Required', 'Nom du pays']], drop_first=True)
        self.y = self.data['Salary']
        
        # Standardiser les données
        self.scaler = StandardScaler()
        self.X_scaled = self.scaler.fit_transform(self.X)

        # Diviser les données en ensembles d'entraînement et de test
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X_scaled, self.y, test_size=0.2, random_state=42)

        # Dictionnaire des modèles à tester
        self.models = {
            'Random Forest': RandomForestRegressor(),
            'Gradient Boosting': GradientBoostingRegressor(),
            'Ridge Regression': Ridge()
        }

        # Dictionnaires pour les hyperparamètres
        self.param_grids = {
            'Random Forest': {'n_estimators': [50, 100, 200], 'max_depth': [5, 10, None], 'min_samples_split': [2, 5, 10]},
            'Gradient Boosting': {'n_estimators': [50, 100, 200], 'learning_rate': [0.01, 0.1, 0.5], 'max_depth': [3, 5, 7]},
            'Ridge Regression': {'alpha': [0.01, 0.1, 1, 10]}
        }

    def train_and_optimize(self):
        # Recherche des meilleurs hyperparamètres pour chaque modèle
        self.best_models = {}
        for model_name, model in self.models.items():
            grid_search = GridSearchCV(model, self.param_grids[model_name], cv=5, scoring='neg_mean_squared_error')
            grid_search.fit(self.X_train, self.y_train)
            self.best_models[model_name] = grid_search.best_estimator_

    def evaluate_models(self):
        # Évaluation des modèles sur les données de test
        evaluation_results = {}
        for model_name, model in self.best_models.items():
            y_pred = model.predict(self.X_test)
            mse = mean_squared_error(self.y_test, y_pred)
            evaluation_results[model_name] = {'MSE': mse}
            print(f"{model_name} - Mean Squared Error (MSE): {mse:.2f}")
        return evaluation_results

    def save_best_model(self):
        # Choisir le modèle avec le MSE le plus faible
        best_model_name = min(self.best_models, key=lambda x: mean_squared_error(self.y_test, self.best_models[x].predict(self.X_test)))
        best_model = self.best_models[best_model_name]
        
        # Sauvegarder le scaler, le modèle et les colonnes utilisées
        joblib.dump(self.scaler, 'scaler.pkl')
        print("Le scaler a été sauvegardé sous 'scaler.pkl'.")

        joblib.dump(best_model, 'best_model.pkl')
        print("Le meilleur modèle a été sauvegardé sous 'best_model.pkl'.")

        joblib.dump(self.X.columns.tolist(), 'dummy_columns.pkl')
        print("Les colonnes utilisées ont été sauvegardées sous 'dummy_columns.pkl'.")

    def load_model(self, model_file):
        # Charger un modèle depuis un fichier
        self.model = joblib.load(model_file)
        print(f"Modèle chargé depuis : {model_file}")

    def predict_salary(self, new_data):
        # Prédire les salaires pour de nouvelles données
        new_data_scaled = self.scaler.transform(new_data)
        return self.model.predict(new_data_scaled)
