import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import os

# Fonction pour extraire les données d'un utilisateur Letterboxd
def scrape_letterboxd_data(username):
    films = []
    page_number = 1

    while True:
        url = f"https://letterboxd.com/{username}/films/page/{page_number}/"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Trouver les films sur la page
        film_list = soup.find_all('li', class_='poster-container')
        if not film_list:
            break

        for film in film_list:
            title = film.find('img')['alt']
            rating = film.find('span', class_='rating')
            rating = rating.text.strip() if rating else None
            films.append({'title': title, 'rating': rating})

        page_number += 1

    return pd.DataFrame(films)

# Fonction pour nettoyer et préparer les données
def clean_data(df):
    # Convertir les notes en nombres
    rating_map = {'½': 0.5, '★': 1, '★½': 1.5, '★★': 2, '★★½': 2.5,
                  '★★★': 3, '★★★½': 3.5, '★★★★': 4, '★★★★½': 4.5, '★★★★★': 5}
    df['rating'] = df['rating'].map(rating_map)

    # Supprimer les films sans note
    df = df.dropna(subset=['rating'])

    return df

# Fonction pour visualiser les données
def visualize_data(df):
    # Histogramme des notes
    plt.figure(figsize=(10, 6))
    plt.hist(df['rating'], bins=10, edgecolor='black', alpha=0.7)
    plt.title('Distribution des Notes')
    plt.xlabel('Note')
    plt.ylabel('Nombre de Films')
    plt.xticks([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
    plt.grid(axis='y', alpha=0.75)
    plt.show()

    # Top 10 des films les mieux notés
    top_films = df.sort_values(by='rating', ascending=False).head(10)
    plt.figure(figsize=(10, 6))
    plt.barh(top_films['title'], top_films['rating'], color='skyblue')
    plt.title('Top 10 des Films les Mieux Notés')
    plt.xlabel('Note')
    plt.ylabel('Film')
    plt.gca().invert_yaxis()
    plt.show()

# Fonction principale
def main():
    # Nom d'utilisateur Letterboxd
    username = input("Entrez votre nom d'utilisateur Letterboxd : ")

    # Extraire les données
    print("Extraction des données en cours...")
    df = scrape_letterboxd_data(username)

    # Nettoyer les données
    df = clean_data(df)

    # Afficher les premières lignes des données
    print("\nDonnées extraites :")
    print(df.head())

    # Visualiser les données
    print("\nVisualisation des données...")
    visualize_data(df)

if __name__ == "__main__":
    main()