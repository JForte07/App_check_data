import streamlit as st

def page_infos():
    st.title("Comment récupérer le fichier de migration")

    st.header("Pour récupérer le fichier de migration sur Django, suivez ces étapes :")

    st.markdown("1. Allez d'abord dans le dossier des migrations.")
    image1 = "data:image/jpeg;base64,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"  
    st.image(image1, caption='Django Etape 1', use_column_width=True)

    st.markdown("2. Cliquez sur la migration qui vous intéresse.")
    image2 = "Picture\Capture d'écran 2023-09-04 124231.png"  
    st.image(image2, caption='Django Etape 2', use_column_width=True)

    st.markdown("3. Cliquez sur le fichier correspondant à la migration.")
    image3 = "Picture\django1.png"  
    st.image(image3, caption='Django Etape 3', use_column_width=True)

    st.write("Vous pouvez également le retrouver dans le migration tracker dans certains cas. Le fichier de migrations s'appelle généralement avec l'ID de la compagnie suivi d'un '_migration' à la fin. Cela vous permet d'avoir tous les fichiers qui ont été utilisés lors de la migration et de comprendre les erreurs s'il y en a.")
    image4 = "Picture\Capture d'écran 2023-09-04 124436.png"  
    st.image(image4, caption='Migration tracker', use_column_width=True)

    st.title("Pour récupérer les fichier qui sont sur le BackOficce")
    st.header("Pour récupérer les données sur Métabase, suivez ces étapes :")
    st.markdown("1. Allez dans le dossier OPS puis dans Migration Sanity Check.")

    st.markdown("2. Pour les passes récupérer la questions All members Payment packs. N'oubliez pas de changer lid de la compagnie")

    st.markdown("3. Pour les souscriptions récupérer la questions Subscription Check. N'oubliez pas de changer lid de la compagnie")
    
    st.markdown("4. Pour les informations des membres -- a venir ")

    st.markdown("Il est important de suivre ces étapes car le code à été créer en fonction de ces fichiers. Merci ")


    
    if st.button("Revenir à la page d'accueil"):
        st.session_state.page = "Accueil"
    
    
