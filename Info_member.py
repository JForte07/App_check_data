import pandas as pd
import unicodedata

def unique_email(df_migration_member, df_bo_member):
    # Vérifier si le nombre d'adresses e-mail uniques est le même dans les deux DataFrames
    unique_mail_same = True
    unique_emails1 = df_migration_member['E-mail address'].nunique()
    unique_emails2 = df_bo_member['email'].nunique()

    if unique_emails1 != unique_emails2:
        unique_mail_same = False
        nbr_diff = abs(unique_emails1 - unique_emails2)
        return unique_mail_same, nbr_diff
    else:
        return unique_mail_same

def email_missing(df_migration_member, df_bo_member):
    # Fusionner les DataFrames sur la colonne 'email'
    merged_df = pd.merge(df_migration_member, df_bo_member, left_on='E-mail address', right_on='email', how='inner', suffixes=('_migration', '_bo'), indicator=True)

    # Identifier les adresses e-mail manquantes dans le df_bo_member
    missing_in_file2 = merged_df[merged_df['_merge'] == 'left_only']
    email_missing_in_file2 = missing_in_file2[['email', 'first_name', 'last_name']]

    if email_missing_in_file2.shape[0] != 0:
        return email_missing_in_file2
    else:
        return None

import unicodedata

def matching_info(df_migration_member, df_bo_member):
    merged_df = pd.merge(df_migration_member, df_bo_member, how='outer', left_on=['E-mail address'], right_on=['email'])
     # Créer un tableau pour stocker les erreurs
    errors = []

    for i in range(len(merged_df)):
        if pd.notna(merged_df['E-mail address'][i]):
            def normalize_string(s):
                if isinstance(s, pd.Timestamp):
                    return unicodedata.normalize('NFKD', str(s)).casefold()
                return unicodedata.normalize('NFKD', s).casefold()
            
            if (not pd.isnull(merged_df['First name'][i]) and not pd.isnull(merged_df['first_name'][i])) and normalize_string(merged_df['first_name'][i]) != normalize_string(merged_df['First name'][i]):
                errors.append({'Erreur': 'Wrong First Name', 'email': merged_df['E-mail address'][i] ,'Valeur correcte': merged_df['First name'][i], 'Valeur incorrecte': merged_df['first_name'][i]})

            if (not pd.isnull(merged_df['Last name'][i]) and not pd.isnull(merged_df['last_name'][i])) and normalize_string(merged_df['last_name'][i]) != normalize_string(merged_df['Last name'][i]):
                errors.append({'Erreur': 'Wrong Last Name', 'email': merged_df['E-mail address'][i] ,'Valeur correcte': merged_df['Last name'][i], 'Valeur incorrecte': merged_df['last_name'][i]})

            if (not pd.isnull(merged_df['gender'][i]) and not pd.isnull(merged_df['Gender'][i])) and normalize_string(merged_df['gender'][i]) != normalize_string(merged_df['Gender'][i]):
                errors.append({'Erreur': 'Wrong gender','email': merged_df['E-mail address'][i] , 'Valeur correcte': merged_df['Gender'][i], 'Valeur incorrecte': merged_df['gender'][i]})
            
            if (not pd.isnull(merged_df['birthday'][i]) and not pd.isnull(merged_df['Date of Birth'][i])) and normalize_string(merged_df['birthday'][i]) != normalize_string(merged_df['Date of Birth'][i]):
                errors.append({'Erreur': 'Wrong Date of Birth','email': merged_df['E-mail address'][i] , 'Valeur correcte': merged_df['Date of Birth'][i], 'Valeur incorrecte': merged_df['birthday'][i]})


    # Créer un DataFrame pour afficher les erreurs
    error_df = pd.DataFrame(errors)

    # Afficher le DataFrame des erreurs
    return error_df

