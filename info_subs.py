import pandas as pd
import streamlit  as st 

def missing_sub(df_sub_bo, df_sub_migr):
    # Concaténez les deux colonnes dans une nouvelle colonne
    df_sub_bo['member_sub'] = df_sub_bo['user_gold → email'] + df_sub_bo['contract_gold → id'].astype(str)
    df_sub_migr['member_sub'] = df_sub_migr['member email'] + df_sub_migr['subscription id'].astype(str)

    # Obtenez les ensembles d'abonnés uniques pour chaque DataFrame
    unique_abo_bo = set(df_sub_bo['member_sub'].unique())
    unique_abo_migr = set(df_sub_migr['member_sub'].unique())

    # Trouvez les membres uniques dans df_sub_migr qui ne sont pas présents dans df_sub_bo
    membres_manquants = unique_abo_migr - unique_abo_bo

    # Créez un dictionnaire pour stocker l'email et l'ID de souscription des membres manquants
    membres_manquants_info = {}

    # Parcourez df_sub_migr pour récupérer les informations des membres manquants
    for member_sub in membres_manquants:
        # Filtrer df_sub_migr pour le membre manquant
        sub_migr_info = df_sub_migr[df_sub_migr['member_sub'] == member_sub]
        
        # Obtenez l'email et l'ID de souscription du membre manquant
        email = sub_migr_info['member email'].values[0]
        subscription_id = sub_migr_info['subscription id'].values[0]
        
        # Stockez les informations dans le dictionnaire
        membres_manquants_info[member_sub] = {'email': email, 'subscription_id': subscription_id}

    # Créez un DataFrame à partir du dictionnaire
    df_membres_manquants = pd.DataFrame.from_dict(membres_manquants_info, orient='index')

    return df_membres_manquants

def compare_info_sub(df_sub_migr, df_sub_bo):
    # Convertissez la colonne 'Date' en type datetime pour effectuer des opérations de date
    df_sub_bo['date_bought'] = pd.to_datetime(df_sub_bo['date_bought'])
    # Convertissez la colonne 'Date' en type datetime pour effectuer des opérations de date
    df_sub_migr['starting date'] = pd.to_datetime(df_sub_migr['starting date'])


    indices_min1 = df_sub_bo.groupby('member_sub')['date_bought'].idxmin()
    indices_min2 = df_sub_migr.groupby('member_sub')['starting date'].idxmin()

    # Utilisez ces indices pour extraire la date minimale et la valeur correspondante dans la colonne 'AutreColonne'
    result1 = df_sub_bo.loc[indices_min1, ['member_sub', 'date_bought', 'Remaining Credits']]
    result2 = df_sub_migr.loc[indices_min2, ['member_sub', 'starting date', 'Credits Remaining Current Period']]

    result1 = result1.reset_index()
    result2 = result2.reset_index()
    # Créer une liste vide pour stocker les erreurs
    erreurs = []

    # Parcourir les données de result1 et result2
    for i in range(len(result1)):
        for j in range(len(result2)):
            if result1['member_sub'][i] == result2['member_sub'][j]:
                if result1['date_bought'][i] == result2['starting date'][j]:
                    # Supprimer les lignes avec des valeurs None dans les colonnes de crédits
                    result1_credits = result1['Remaining Credits'][i]
                    result2_credits = result2['Credits Remaining Current Period'][j]
                    if pd.notna(result1_credits) and pd.notna(result2_credits):
                        if result1_credits != result2_credits:
                            # Ajouter les informations sur l'erreur de crédits à la liste
                            erreur = {
                                'Type_Erreur': 'Crédits',
                                'Member_Sub': result1['member_sub'][i],
                                'Date_Bought': result1['date_bought'][i],
                                'Remaining_Credits_Result1': result1_credits,
                                'Remaining_Credits_Result2': result2_credits
                            }
                            erreurs.append(erreur)
                    # Vérifier si les dates sont différentes
                    elif result1['date_bought'][i] != result2['starting date'][j]:
                        # Ajouter l'erreur de date
                        erreur = {
                            'Type_Erreur': 'Dates',
                            'Member_Sub': result1['member_sub'][i],
                            'Date_Bought_Result1': result1['date_bought'][i],
                            'Date_Bought_Result2': result2['starting date'][j],
                            'Remaining_Credits_Result1': result1_credits,
                            'Remaining_Credits_Result2': result2_credits
                        }
                        erreurs.append(erreur)

    # Créer un DataFrame à partir de la liste d'erreurs
    df_erreurs = pd.DataFrame(erreurs)
    return df_erreurs


def compare_sub(df_migration_sub, df_bo_sub):
    miss_sub = missing_sub(df_bo_sub,df_migration_sub)
    if len(miss_sub)!=0:
        st.write(str(len(miss_sub)),'/',str(len(df_migration_sub)),"Souscriptions n'ont pas été migré")
        st.write('Les souscriptions qui ne sont pas migrés',miss_sub)

    sub_error = compare_info_sub(df_migration_sub,df_bo_sub)
    if len(sub_error)!=0:
        st.write(len(sub_error),"erreurs ont étés detectés")
        st.write('Les erreurs sont les suiavntes:',sub_error)
        st.download_button(label="Télécharger le CSV des erreurs", data=sub_error.to_csv(), file_name="Erreurs_sub.csv")
    return 
