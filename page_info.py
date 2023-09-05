import streamlit as st
from PIL import Image

def page_infos():
    st.title("Comment récupérer le fichier de migration")

    st.header("Pour récupérer le fichier de migration sur Django, suivez ces étapes :")

    st.markdown("1. Allez d'abord dans le dossier des migrations.")
    image = Image.open("Picture/django3.png")
    st.image(image, caption='Django Etape 1', use_column_width=True)

    st.markdown("2. Cliquez sur la migration qui vous intéresse.")
    image2 = "Picture/Capture d'écran 2023-09-04 124231.png"  
    st.image(image2, caption='Django Etape 2', use_column_width=True)

    st.markdown("3. Cliquez sur le fichier correspondant à la migration.")
    image3 = "Picture/django1.png"  
    st.image(image3, caption='Django Etape 3', use_column_width=True)

    st.write("Vous pouvez également le retrouver dans le migration tracker dans certains cas. Le fichier de migrations s'appelle généralement avec l'ID de la compagnie suivi d'un '_migration' à la fin. Cela vous permet d'avoir tous les fichiers qui ont été utilisés lors de la migration et de comprendre les erreurs s'il y en a.")
    image4 = "Picture/Capture d'écran 2023-09-04 124436.png"  
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
    
    
