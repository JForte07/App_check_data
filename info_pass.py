import pandas as pd
import numpy as np
import streamlit as st 

def unique_pass(df_migration_pass, df_bo_pass):
    # Groupement par adresse e-mail et comptage unique du nombre de pass
    grouped_counts_migration = df_migration_pass.groupby('E-mail address')['Name of the pass'].nunique()
    grouped_counts_bo = df_bo_pass.groupby('user_email')['payment_pack_name'].nunique()

    nbr_pass_migration = len(grouped_counts_migration)
    nbr_pass_bo = len(grouped_counts_bo)

    return nbr_pass_bo,nbr_pass_migration

def check_info_pass(data_migration_pass, data_bo_pass):
    # Concaténer les colonnes en une nouvelle colonne 'info pass concat' sous forme de chaînes
    data_migration_pass['info pass concat'] = (data_migration_pass['E-mail address'].astype(str) +
                                    data_migration_pass['Name of the pass'].astype(str) +
                                    data_migration_pass['Purchase date of the pass'].astype(str) +
                                    #data_migration_pass['Expiry date of the pass'].astype(str) +
                                    data_migration_pass['Remaining credits left on the pass'].astype(str))
    data_migration_pass['mail pass'] = (data_migration_pass['E-mail address'].astype(str) +
                                    data_migration_pass['Name of the pass'].astype(str) 
                                    )

    data_bo_pass['credit'] = data_bo_pass['home_paymentpack - payment_pack_id → credits'] - data_bo_pass['used_credits']
    data_bo_pass['info pass concat']= (data_bo_pass['user_email'].astype(str) +
                                    data_bo_pass['payment_pack_name'].astype(str) +
                                    data_bo_pass['date_bought'].astype(str) +
                                    #data_bo_pass['ending_date_computed'].astype(str) +
                                    data_bo_pass['credit'].astype(str))
    data_bo_pass['mail pass']= (data_bo_pass['user_email'].astype(str) +
                                    data_bo_pass['payment_pack_name'].astype(str) )
    
    # Convertir les colonnes 'info pass concat' en ensembles pour une recherche plus efficace
    migr_info_pass_set = set(data_bo_pass['info pass concat'])

    aucun_match = []  # Liste pour stocker les indices de data_migration_pass sans correspondance

    for i, row_migr in data_migration_pass.iterrows():
        if row_migr['info pass concat'] not in migr_info_pass_set:
            aucun_match.append(i)

    miss_pass = {'mail': [], 'pass': []}

    # Convertir la colonne 'mail pass' en ensembles pour une recherche plus efficace
    bo_mail_pass_set = set(data_bo_pass['mail pass'])

    for j in range(len(aucun_match)):
        if data_migration_pass['mail pass'][j] not in bo_mail_pass_set:
            miss_pass['mail'].append(data_migration_pass['E-mail address'][j])
            miss_pass['pass'].append(data_migration_pass['Name of the pass'][j])
    df_miss_pass = pd.DataFrame(miss_pass)
    st.write('Nombre de pass non présent dans le BO :',len(miss_pass['mail']))
    st.write('Membre concernés:',df_miss_pass)
    st.download_button(label="Télécharger CSV", data=df_miss_pass.to_csv(), file_name="pass manquant.csv")
    incorrect_price_count = 0
    incorrect_credits_count = 0
    incorrect_date_count = 0
    errors = []
    # Create a progress bar
    progress_bar = st.progress(0)

    total_iterations = len(aucun_match)

    for idx, i in enumerate(aucun_match):
        for j, row_bo in data_bo_pass.iterrows():
            if row_bo['mail pass'] == data_migration_pass['mail pass'][i]:
                if data_migration_pass['Price of the pass'][i] != row_bo['initial_price']:
                    incorrect_price_count += 1
                    errors.append({
                        'Erreur': 'Prix incorrect',
                        'E-mail address': data_migration_pass['E-mail address'][i],
                        'Pass': data_migration_pass['Name of the pass'][i],
                        'valeur correcte dans le fichier migration': data_migration_pass['Price of the pass'][i],
                        'valeur incorrecte dans le BO': row_bo['initial_price']
                    })
                elif data_migration_pass['Remaining credits left on the pass'][i]!= row_bo['credit']:
                    incorrect_credits_count += 1
                    errors.append({
                        'Erreur': 'Credits incorrect',
                        'E-mail address': data_migration_pass['E-mail address'][i],
                        'Pass': data_migration_pass['Name of the pass'][i],
                        'valeur correcte dans le fichier migration': data_migration_pass['Remaining credits left on the pass'][i],
                        'valeur incorrecte dans le BO': row_bo['credit']
                    })
                elif data_migration_pass['Purchase date of the pass'][i] != row_bo['date_bought']:
                    incorrect_date_count += 1
                    errors.append({
                        'Erreur': 'date incorrecte',
                        'E-mail address': data_migration_pass['E-mail address'][i],
                        'Pass': data_migration_pass['Name of the pass'][i],
                        'valeur correcte dans le fichier migration': data_migration_pass['Purchase date of the pass'][i],
                        'valeur incorrecte dans le BO': row_bo['date_bought']
                    })

        # Update the progress bar after each iteration
        progress_percent = (idx + 1) / total_iterations
        progress_bar.progress(progress_percent)

    # Close the progress bar
    progress_bar.empty()

        
    # Afficher les compteurs d'erreurs
    st.write("Nombre de dates  incorrects :", incorrect_date_count)
    st.write("Nombre de prix incorrects :", incorrect_price_count)
    st.write("Nombre de crédits incorrects :", incorrect_credits_count)

    errors_df = pd.DataFrame(errors)
    
    return errors_df

def compare_pass(df_migration_pass,df_bo_pass):
    nbr_pass_bo,nbr_pass_migration = unique_pass(df_migration_pass,df_bo_pass)
    error_df = check_info_pass(df_migration_pass, df_bo_pass)
    
    st.subheader("Résultats de la comparaison :")

    if nbr_pass_bo != nbr_pass_migration:
        st.write('Le nombre de passes ne correspond pas. Il manque des passes.')

    if not error_df.empty:
        st.write("Erreurs détectées :")
        st.write(error_df)
        st.write(f"Nombre de membres avec des données de pass incorrectes : {len(error_df)} / {df_migration_pass['E-mail address'].nunique()}")
        st.download_button(label="Télécharger le CSV des erreurs", data=error_df.to_csv(), file_name="Erreurs_pass.csv")
    else: 
        st.write("Aucune erreur détectée.")

