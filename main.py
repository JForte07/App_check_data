import streamlit as st
import pandas as pd

from page_member import *
from page_passes import *
from pasge_sub import *


from Info_member import *
from info_pass import *
from info_subs import *

def main():
    """
    
    Menu principale avec explication 
    
    
    """
    # Titre de l'application
    st.title('Data migration Sanity Check')
    
    """
    Explication du site 
    """
    st.write("Ce site à pour but de vérifier si toutes les informations ont été correctement migrér dans le Backoffice du client. Il vous faudra vous munir du fichier de migrations, ce dernier est récupérable dans django admi ou dans le migration tracker. Il vous faudra également récupérer des informations sur metabase , en fonction de ce que vous souhaitez faire, une indication vous sera donnée pour récupérer facilement les informations")
    

    """
    Petite explication pour récupérer le fichier de migration
    """
    st.write("Pour récupérer le fichier de migration sur django. Aller dans un premier temps dans data miration")
    image1 = "App_check_data\Picture\django3.png"  
    st.image(image1, caption='Django Etape 1 ', use_column_width=True)
    st.write("Cliquez sur la migration qui vous interesse")
    image2 = "App_check_data\Picture\Capture d'écran 2023-09-04 124231.png"  
    st.image(image2, caption='Django Etape 2 ', use_column_width=True)
    st.write("Puis sur le fichier")
    image3 = "App_check_data\Picture\django1.png"  
    st.image(image3, caption='Django Etape 3 ', use_column_width=True)

    st.write("Vous pouvez également le retrouver dans le migration tracker dans certains cas. le fichier migrations s'appelle généralement avec l id de la compagnie avec un _migration à la fin. Ce qui vous permet d'avoir tout les fichier qui ont été utiliser lors de la migration et ainsi comprendre lerreur sil y a")
    image1 = "App_check_data\Picture\Capture d'écran 2023-09-04 124436.png"  
    st.image(image1, caption='Migration tracker', use_column_width=True)


    """
    Les différentes pages 
    """
    st.write("Choississez ce que vous souhaitez faire : ")
    # Ajouter un bouton
    if st.button('Vérifier informations sur les membres'):
        st.session_state.page = "Page informations membres"

    if st.button('Vérifier informations sur les passes'):
        st.session_state.page = "Page informations passes"

    if st.button('Vérifier informations sur les sosuscriptions'):
        st.session_state.page = "Page informations souscription"

# Afficher la page en fonction de la valeur de st.session_state.page
    if st.session_state.page == "Accueil":
        main()
    elif st.session_state.page == "Page informations membres":
        page_membre()
    elif st.session_state.page == "Page informations passes":
        page_pass()
    elif st.session_state.page == "Page informations souscription":
        page_sub()
    

    # Chargement du premier fichier Excel
    st.write("Télécharger le fichier Excel de migration:")
    file_1 = st.file_uploader("Choisissez un fichier", type=["xls", "xlsx"], key="file_uploader_1")

    # Chargement du deuxième fichier Excel
    st.write("Télécharger le fichier Excel du BackOffice:")
    file_2 = st.file_uploader("Choisissez un fichier", type=["xls", "xlsx"], key="file_uploader_2")

    # Ajouter un bouton pour effectuer les comparaisons
    if st.button("Comparer les Fichiers"):
        if file_1 is not None and file_2 is not None:
            # Lire les fichiers Excel et créer des DataFrames
            df_migration = pd.read_excel(file_1, sheet_name=None)
            df_bo = pd.read_excel(file_2, sheet_name=None)

            df_migration_member = df_migration['Member']
            df_bo_member = df_bo['member']

            compare_info(df_migration_member, df_bo_member)

            #Partie Pass 
            df_migration_pass = df_migration['Member']
            df_bo_pass = df_bo['pass']
            compare_pass(df_migration_pass,df_bo_pass)

            """Partie pour les souscriptions
            Dans un premier temps regarde si toutes les souscriptions ont été migrés 
            Ensuite vérifie que les informations sont égales (on s'interressent surtout à la date et aux crédits) 
            """
            df_migration_sub = df_migration['Subscriptions']
            df_bo_sub = df_bo['Sub']
            compare_sub(df_migration_sub, df_bo_sub)

        else:
            st.warning("Veuillez télécharger les deux fichiers Excel avant de comparer.")



if __name__ == "__main__":
    main()
