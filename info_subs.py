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

def compare_sub(df_migration_sub, df_bo_sub):
    miss_sub = missing_sub(df_bo_sub,df_migration_sub)
    if len(miss_sub)!=0:
        st.write(len(miss_sub),"Souscriptions n'ont pas été migré")
        st.write('Les souscriptions qui ne sont pas migrés',miss_sub)
    return 
