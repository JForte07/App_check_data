import streamlit as st
from info_subs import *

def page_sub():    

    # Titre de la page
    st.title("Page Informations sur les Souscriptions")

    # Introduction
    st.write("Sur cette page, nous vérifierons seulement les informations relatives aux membres concernant leurs souscriptions.")
    st.write("Vous avez normalement récupéré votre fichier de migration. Veuillez l'importer ici : ")

    # Chargement du premier fichier Excel (Migration)
    st.header("Étape 1 : Importer le fichier Excel de migration")
    file_1 = st.file_uploader("Sélectionnez un fichier Excel", type=["xls", "xlsx"], key="file_uploader_1")

    # Séparation
    st.write("---")

    
    # Chargement du deuxième fichier Excel (BackOffice)
    st.header("Étape 2 : Importer le fichier Excel du BackOffice")
    # Informations sur les choix du Backoffice
    st.write("Vous avez deux options pour récupérer les informations du Backoffice :")
    st.write("Option 1 : Si vous choisissez d'importer le rapport directement depuis le Backoffice, vous aurez besoin des informations suivantes : e-mails, ID de souscription et date de crédit. Veuillez importer les informations ici :")
    st.write("Option 2 : Si vous choisissez de récupérer les données depuis Metabase, vous devrez simplement fournir l'ID de la compagnie.")

    file_2 = st.file_uploader("Sélectionnez un fichier Excel", type=["xls", "xlsx"], key="file_uploader_2")

    # Bouton pour comparer les fichiers
    if st.button("Comparer les Fichiers"):
        if file_1 is not None and file_2 is not None:
            # Lire les fichiers Excel et créer des DataFrames
            df_migration = pd.read_excel(file_1, sheet_name=None)
            df_bo_sub = pd.read_excel(file_2)

            # Partie Souscription
            # Accéder aux DataFrames pour un traitement ultérieur
            df_migration_sub = df_migration['Subscriptions']

            compare_sub(df_migration_sub, df_bo_sub)

    # Bouton pour revenir à la page d'accueil
    if st.button("Revenir à la page d'accueil"):
        st.session_state.page = "Accueil"
