# Instructions

* Installez Python (version >= 3.11.5), et assurez vous que pip est bien installé avec (version >= 23.2.1)
* Clonez ce repo dans un répertoire local
* Créez un environnement virtuel avec la commande : `py -m venv env`
* Entrez dans votre environnement virtuel avec la commande : `.\env\Scripts\activate`
* Installez les librairies du fichier **requirements.txt** dans votre environnement virtuel avec la commande `pip install -r requirements.txt`
* Exécutez le script python **extract.py** avec la commande `py extract.py`

# Résultats attendus

Ce script extrait des données à partir du site [Books to Scrape](http://books.toscrape.com/).
Il crée un répertoire _all_extracted_data_ qui contient un sous-répetoire pour chaque catégorie de livre.
Chaque sous-répertoire contient lui-même deux sous-répertoire:
* Un pour les données de chaque livre de la catégorie, rassemblées dans un tableau au format .csv
* L'autre pour les images de chacun de ces livres.