# Projet_US_SBA

Ce projet vise à développer un système de prédiction d'assurance de prêt bancaire en utilisant différentes technologies telles que Light GBM pour le modèle de machine learning, FastAPI pour l'API de prédiction, et Django pour l'interface utilisateur.

## Structure du Projet

Le projet est divisé en trois parties principales :

1. **api_predict/** : Cette partie contient les fichiers nécessaires pour créer et exécuter l'API de prédiction basée sur FastAPI.
   - `Dockerfile` : Fichier de configuration Docker pour créer l'environnement de l'API.
   - `main.py` : Le code principal de l'API.
   - `modelLGBM.pkl` : Le modèle Light GBM pré-entraîné.
   - `model_utils.py` : Utilitaires pour charger et utiliser le modèle.
   - `requirements.txt` : Liste des dépendances Python nécessaires.

2. **django_us_sba/** : Cette partie contient les fichiers pour l'application Django qui affiche l'interface utilisateur.
   - `Dockerfile` : Fichier de configuration Docker pour créer l'environnement de Django.
   - `manage.py` : Point d'entrée pour les commandes de gestion de Django.
   - `requirements.txt` : Liste des dépendances Python nécessaires.

3. **ML/** : Cette partie contient les notebooks Jupyter utilisés pour le nettoyage des données, l'exploration des données et l'entraînement des modèles.
   - `01-nettoyage.ipynb` : Notebook pour le nettoyage des données.
   - `02-EDA.ipynb` : Notebook pour l'exploration des données.
   - `03-LGBM.ipynb` : Notebook pour l'entraînement du modèle Light GBM.
   - `03-pycaret.ipynb` : Notebook pour l'entraînement du modèle avec PyCaret.
   - `02-EDA2.ipynb` : Deuxième notebook pour l'exploration des données.
   - `02-sweetviz.ipynb` : Notebook pour l'analyse de données avec SweetViz.
   - `03-LGBM_resultats.ipynb` : Notebook pour l'évaluation des résultats du modèle Light GBM.
   - `03-résultats_pycaret.ipynb` : Notebook pour l'évaluation des résultats du modèle PyCaret.
   - `requirement.txt` : Liste des dépendances Python pour les notebooks.

## Utilisation

Pour exécuter le projet localement, assurez-vous d'avoir Docker installé sur votre système. Utilisez Docker Compose pour gérer les conteneurs Docker pour chaque partie du projet :

```bash
docker-compose up
```
Cela démarrera les conteneurs Docker pour l'API de prédiction, l'application Django et la base de données PostgreSQL.

Assurez-vous également d'installer les dépendances Python spécifiées dans les fichiers requirements.txt pour chaque partie du projet avant de lancer les conteneurs Docker.
Contribuer

Les contributions sont les bienvenues ! Si vous souhaitez contribuer à ce projet, veuillez suivre ces étapes :

   - Fork du projet
   - Créez une nouvelle branche (git checkout -b feature)
   - Faites vos modifications
   - Commitez vos modifications (git commit -am 'Ajout d'une nouvelle fonctionnalité')
   - Poussez sur la branche (git push origin feature)
   - Créez une nouvelle Pull Request

Auteurs

Ce projet a été développé par Kévin et Christian.


Ce README.md fournit des informations sur la structure du projet, comment l'exécuter localement, comment contribuer et qui sont les auteurs du projet. Vous pouvez bien sûr l'adapter selon vos besoins spécifiques.
