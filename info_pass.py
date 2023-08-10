import pandas as pd
import numpy as np
import streamlit as st 

def unique_pass(df_migration_pass, df_bo_pass):
    # Groupement par adresse e-mail et comptage unique du nombre de pass
    grouped_counts_migration = df_migration_pass.groupby('E-mail address')['Name of the pass'].nunique()
    grouped_counts_bo = df_bo_pass.groupby('email')['base_name'].nunique()

    nbr_pass_migration = len(grouped_counts_migration)
    nbr_pass_bo = len(grouped_counts_bo)

    return nbr_pass_bo,nbr_pass_migration

def check_info_pass(data_migration_pass, data_bo_pass):
    email_with_good_pass = []
    errors = []
    total_records = len(data_migration_pass['E-mail address'])
    # Suivi de l'avancement
    st.title("Vérification des données de migration")
    st.write("En cours de traitement...")
    progress_bar = st.progress(0)  # Initialiser la barre de progression
    
    # Compteurs d'erreurs
    incorrect_pass_count = 0
    incorrect_price_count = 0
    incorrect_credits_count = 0
    
    for i in range(len(data_migration_pass['E-mail address'])):
        # Mettre à jour la barre de progression
        progress_percent = (i + 1) / total_records
        if progress_percent <= 1.0:
            progress_bar.progress(progress_percent)

        if data_migration_pass['E-mail address'][i]:
            for j in range(len(data_bo_pass['email'])):
                if data_migration_pass['E-mail address'][i] == data_bo_pass['email'][j]:
                    if data_migration_pass['Name of the pass'][i] == data_bo_pass['base_name'][j]:
                        email_with_good_pass.append(data_migration_pass['E-mail address'][i] + '/' + data_migration_pass['Name of the pass'][i])
                        
                        # Vérifier si les prix et les crédits correspondent
                        if (data_migration_pass['Price of the pass'][i] != data_bo_pass['base_price'][j]):
                            incorrect_price_count += 1
                            errors.append({'Erreur': 'Prix incorrect',
                            'E-mail address': data_migration_pass['E-mail address'][i],
                            'Pass':data_migration_pass['Name of the pass'][i],
                            'valeur correcte dans le fichier migration': data_migration_pass['Price of the pass'][i],
                            'valeur incorrecte dans le BO': data_bo_pass['base_price'][j]})
                        elif (data_migration_pass['Remaining credits left on the pass'][i] != data_bo_pass['credits'][j]):
                            incorrect_credits_count += 1
                            errors.append({'Erreur': 'Credits incorrect',
                            'E-mail address': data_migration_pass['E-mail address'][i],
                            'Pass':data_migration_pass['Name of the pass'][i],
                            'valeur correcte dans le fichier migration': data_migration_pass['Remaining credits left on the pass'][i],
                            'valeur incorrecte dans le BO': data_bo_pass['credits'][j]})
                        else:  # Cas où les prix et les crédits correspondent
                            errors.append({'Erreur': 'Prix et crédits corrects',
                            'E-mail address': data_migration_pass['E-mail address'][i],
                            'Pass':data_migration_pass['Name of the pass'][i]})
                            
    # Vérifier si le courriel a au moins un match dans data_bo_pass
    if not email_with_good_pass:
        errors.append({'Erreur': 'Aucune correspondance trouvée pour l\'e-mail',
                        'E-mail address': data_migration_pass['E-mail address'][i]})
    
    errors_df = pd.DataFrame(errors)
    
    # Nettoyage final : supprimer les lignes avec valeurs correctes et incorrectes vides
    errors_df = errors_df.dropna(subset=['valeur correcte dans le fichier migration', 'valeur incorrecte dans le BO'])
    
    # Afficher les compteurs d'erreurs
    st.write("Nombre de passes incorrects :", incorrect_pass_count)
    st.write("Nombre de prix incorrects :", incorrect_price_count)
    st.write("Nombre de crédits incorrects :", incorrect_credits_count)
    
    return errors_df

