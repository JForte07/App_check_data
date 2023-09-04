import streamlit as st
import pandas as pd

from page_member import page_membre
from page_passes import page_pass
from page_sub import page_sub
from page_info import page_infos

from info_pass import *
from info_subs import * 
from Info_member import *

# Initialisez st.session_state.page avec la valeur "Accueil"
if 'page' not in st.session_state:
    st.session_state.page = "Accueil"

def main():
    st.title('Data Migration Sanity Check')

    st.write("Ce site a pour but de vérifier si toutes les informations ont été correctement migrées dans le Backoffice du client.")
    
    if st.button('Informations'):
        st.session_state.page = "Page informations"

    st.header("Choisissez ce que vous souhaitez vérifier : ")

    col1, col2 = st.columns(2)

    if col1.button('Vérifier informations sur les membres'):
        st.session_state.page = "Page informations membres"

    if col1.button('Vérifier informations sur les passes'):
        st.session_state.page = "Page informations passes"

    if col2.button('Vérifier informations sur les souscriptions'):
        st.session_state.page = "Page informations souscription"
    

    st.header("Continuez ici si vous souhaitez tout vérifier : ")
    st.write("Téléchargez les fichiers Excel :")

    col1, col2 = st.columns(2)

    with col1:
        file_1 = st.file_uploader("Migration Excel", type=["xls", "xlsx"], key="file_uploader_1")
        file_2 = st.file_uploader("BackOffice Membres Excel", type=["xls", "xlsx"], key="file_uploader_2")

    with col2:
        file_3 = st.file_uploader("BackOffice Passes Excel", type=["xls", "xlsx"], key="file_uploader_3")
        file_4 = st.file_uploader("BackOffice Subscriptions Excel", type=["xls", "xlsx"], key="file_uploader_4")

    if st.button("Comparer les Fichiers"):
        if file_1 is not None and file_2 is not None and file_3 is not None and file_4 is not None:
            # Lire les fichiers Excel et créer des DataFrames
            df_migration = pd.read_excel(file_1, sheet_name=None)
            df_bo_member = pd.read_excel(file_2)
            df_bo_pass = pd.read_excel(file_3)
            df_bo_sub = pd.read_excel(file_4)

            df_migration_member = df_migration['Member']

            compare_info(df_migration_member, df_bo_member)

            # Partie Pass 
            df_migration_pass = df_migration['Member']
            compare_pass(df_migration_pass,df_bo_pass)

            """Partie pour les souscriptions
            Dans un premier temps regarde si toutes les souscriptions ont été migrées 
            Ensuite vérifie que les informations sont égales (on s'interresse surtout à la date et aux crédits) 
            """
            df_migration_sub = df_migration['Subscriptions']
            compare_sub(df_migration_sub, df_bo_sub)
        else:
            st.warning("Veuillez télécharger les deux fichiers Excel avant de comparer.")

# Afficher la page en fonction de la valeur de st.session_state.page
if st.session_state.page == "Accueil":
    main()
elif st.session_state.page == "Page informations membres":
    page_membre()
elif st.session_state.page == "Page informations passes":
    page_pass()
elif st.session_state.page == "Page informations souscription":
    page_sub()
elif st.session_state.page == "Page informations" : 
    page_infos()
