import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image

url = "https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv"
df = pd.read_csv(url)

# Titre de l'application
st.title("Analyse du dataset des voitures")

# Page "Présentation"
if st.sidebar.selectbox("Navigation", ["Présentation", "Analyse"]) == "Présentation":
    st.title("Présentation")
    
    # Ajouter l'image
    try:
        image = Image.open("C:\\Users\\maxim\\OneDrive\\Images\\WCS.png")
        st.image(image, width=200, caption="Wild Code School")
    except FileNotFoundError:
        st.warning("L'image n'a pas pu être chargée. Vérifiez le chemin du fichier.")
    
    st.write("""
    **Maxime TELLIER**
    
    Wild Code School Student 2023-2024
    
    **Challenge**
    
    A partir du dataset des voitures, nous afficherons :
    
    - Une analyse de corrélation et de distribution grâce à différents graphiques et des commentaires.
    
    - Des boutons doivent être présents pour pouvoir filtrer les résultats par région (US / Europe / Japon).
    
    L'application doit être disponible sur la plateforme de partage.
    """)
else:
    # Affichage du dataset
    st.write("Aperçu du dataset :")
    st.dataframe(df)

    # Filtrer par région
    regions = st.sidebar.multiselect("Choisir la région", df["continent"].unique())
    if regions:
        df = df[df["continent"].isin(regions)]

    # Résumé statistique
    st.write("Résumé statistique :")
    st.write(df.describe())

    # Matrice de corrélation
    st.write("Matrice de corrélation :")
    corr_matrix = df.corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig)

    # Filtrer les colonnes numériques
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    # Sélection des variables pour créer des boxplots
    selected_columns = st.multiselect('Sélectionnez les colonnes pour les boxplots', numeric_columns)

    # Affichage en boxplots
    if selected_columns:
        st.write("Boxplots :")
        for column in selected_columns:
            st.write(f"**{column}**")
            fig_boxplot, ax = plt.subplots()
            sns.boxplot(x=df[column], ax=ax)
            st.pyplot(fig_boxplot)

    # Distribution des variables
    st.write("Distribution des variables :")
    st.markdown("""
    Chaque graphique de distribution montre sur l'axe des x les différentes valeurs uniques de la variable (par exemple, des chiffres spécifiques pour une colonne numérique) et sur l'axe des y, le nombre de fois que chaque valeur apparaît dans le jeu de données. Cela peut être utile pour comprendre la répartition des valeurs et identifier des tendances, des valeurs aberrantes.
    """)
    for column in df.columns:
        if df[column].dtype != "object":
            st.write(f"**{column}**")
            st.line_chart(df[column].value_counts())

    # Scatter plot
    st.write("Scatter Plot :")
    fig_scatter = plt.figure()
    for col in df.columns:
        if col != "continent" and df[col].dtype != "object":
            plt.scatter(df[col], df["continent"], label=col, alpha=0.5)
    plt.legend()
    st.pyplot(fig_scatter)

    # Lien vers l'application Streamlit
    st.write("L'application est disponible sur [Streamlit Sharing](https://share.streamlit.io/your-username/your-repo/my_challenge_app.py)")
