import streamlit as st 
from main import *
from info_pass import *

def page_pass():    

    st.title("Page informations passes")
    st.write("Sur cette page Nous vérifierons seulement les informations relatives aux membre sur les pass")
    st.write("Vous avez normalement récupérer votre fichier migration. Veuillez l'importer ici : ")

    # Chargement du premier fichier Excel
    st.write("Importer le fichier Excel de migration:")
    file_1 = st.file_uploader("Choisissez un fichier", type=["xls", "xlsx"], key="file_uploader_1")

    st.write("Pour récupérer les informations du Backoffice vous avez deux choix; soit par le rapport sur le BO ou alors sur metabase")
    st.write("Si vous choississez par le rapport sur le Backoffice directement , vous aurez besoin des informations suivantes : noms prenoms mails,date dachat prix credit date d'expiration noms du pass. Veuillez importer les information ici : ")
    st.write("pas encore disponible")
    
    # Chargement du deuxième fichier Excel
    st.write("Si vous récupérer le récupérer sur metabase, il vous suffira de rentre l id de la compagnie")
    
    st.write("Importer le fichier Excel du BackOffice:")
    file_2 = st.file_uploader("Choisissez un fichier", type=["xls", "xlsx"], key="file_uploader_2")
    if st.button("Comparer les Fichiers"):
        if file_1 is not None and file_2 is not None :
            # Lire les fichiers Excel et créer des DataFrames
            df_migration = pd.read_excel(file_1, sheet_name=None)
            df_bo_pass = pd.read_excel(file_2)

            #Partie Membre 
            # Accéder aux DataFrames pour un traitement ultérieur
            df_migration_pass = df_migration['Member']

            compare_pass(df_migration_pass, df_bo_pass)

    if st.button("Revenir à la page d'accueil"):
        st.session_state.page = "Accueil"

if st.session_state.page == "Accueil":
        main()