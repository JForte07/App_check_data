import streamlit as st
from info_pass import *

def page_pass():
    # Titre de la page
    st.title("Page Informations Passes")

    # Introduction
    st.write("Bienvenue sur la page de vérification des informations des membres sur les passes.")
    st.write("Vous devez d'abord importer le fichier de migration. Suivez les étapes ci-dessous :")

    # Chargement du premier fichier Excel
    st.header("Étape 1 : Importer le fichier Excel de migration")
    file_1 = st.file_uploader("Sélectionnez un fichier Excel", type=["xls", "xlsx"], key="file_uploader_1")

    # Séparation
    st.write("---")

    # Informations sur les choix du Backoffice
    st.write("Vous avez deux options pour récupérer les informations du Backoffice :")
    st.write("Option 1 : Si vous choisissez d'importer le rapport directement depuis le Backoffice, vous aurez besoin des informations suivantes : noms, prénoms, e-mails, date d'achat, prix, crédit, date d'expiration et noms du pass. Veuillez importer les informations ici :")
    st.write("Option 2 : Si vous choisissez de récupérer les données depuis Metabase, vous devrez simplement fournir l'ID de la compagnie.")

    # Chargement du deuxième fichier Excel (BackOffice)
    st.header("Étape 2 : Importer le fichier Excel du BackOffice")
    file_2 = st.file_uploader("Sélectionnez un fichier Excel", type=["xls", "xlsx"], key="file_uploader_2")

    # Bouton pour comparer les fichiers
    if st.button("Comparer les Fichiers"):
        if file_1 is not None and file_2 is not None:
            # Lire les fichiers Excel et créer des DataFrames
            df_migration = pd.read_excel(file_1, sheet_name=None)
            df_bo_pass = pd.read_excel(file_2)

            # Partie Membre 
            # Accéder aux DataFrames pour un traitement ultérieur
            df_migration_pass = df_migration['Member']

            compare_pass(df_migration_pass, df_bo_pass)

    # Bouton pour revenir à la page d'accueil
    if st.button("Revenir à la page d'accueil"):
        st.session_state.page = "Accueil"
