import streamlit as st
import pandas as pd


from Info_member import *
from info_pass import *

def main():
    # Titre de l'application
    st.title('Data Post Migration')

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

            #Partie Membre 
            # Accéder aux DataFrames pour un traitement ultérieur
            df_migration_member = df_migration['Member']
            df_bo_member = df_bo['Member ']

            # Appels aux fonctions définies dans info_member
            unique_email_result, nbr_diff = unique_email(df_migration_member, df_bo_member)
            email_missing_result = email_missing(df_migration_member, df_bo_member)
            
            # Affichage des résultats dans l'interface utilisateur
            if unique_email_result == False : 
                st.write("Nombre de différences d'adresses e-mail :", nbr_diff)
            if email_missing_result is not None:
                st.write("Adresses e-mail manquantes :", email_missing_result)
            else:
                st.write("Aucune adresse e-mail manquante.")

            error_info_member = matching_info(df_migration_member, df_bo_member)
            # Afficher le DataFrame des erreurs
            if error_info_member is not None and not error_info_member.empty:
                st.title('Récapitulatif des Erreurs sur les infos des membres')
                st.write(error_info_member)
                st.write("Nombre d'erreurs par type :")
                error_counts_member = error_info_member.groupby('email')['Erreur'].count()
                error_counts = error_info_member.groupby('Erreur').size().reset_index(name='Nombre')
                for index, row in error_counts.iterrows():
                    st.write(f"{row['Erreur']}: {row['Nombre']}")

                st.write("Nombre de personnes qui ont de mauvaises informations:", len(error_counts_member), '/', df_migration_member['E-mail address'].nunique())
                st.download_button(label="Télécharger CSV", data=error_info_member.to_csv(), file_name="Erreur membre.csv")
            else : 
                st.write("Nombre de personnes qui ont de mauvaises informations:", 0, '/', df_migration_member['E-mail address'].nunique())

            #Partie Pass 
            df_migration_pass = df_migration['Member']
            df_bo_pass = df_bo['pass ']
            nbr_pass_bo,nbr_pass_migration = unique_pass(df_migration_pass,df_bo_pass)
            error_df = check_info_pass(df_migration_pass, df_bo_pass)
            if nbr_pass_bo != nbr_pass_migration :
                st.write('Pas le même nbr de pass, mais plus de pass donc surement ajout')
                if nbr_pass_migration<nbr_pass_bo :
                    st.write('Il Manque des Pass')

            # Titre de l'application
            st.title('Récapitulatif des Erreurs des pass')

            if not error_df.empty:
                st.write(error_df)
                error_counts = error_df.groupby('E-mail address')['Erreur'].count()
                st.write("Nombre de membres avec des données de pass faux :", len(error_counts), '/', df_migration_pass['E-mail address'].nunique())
                st.download_button(label="Télécharger CSV", data=error_df.to_csv(), file_name="Erreur pass.csv")
            else: 
                st.write("Nombre de membres avec des données de pass faux :",0, '/', df_migration_pass['E-mail address'].nunique())
        else:
            st.warning("Veuillez télécharger les deux fichiers Excel avant de comparer.")

if __name__ == "__main__":
    main()
