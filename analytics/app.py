import streamlit as st
import pandas as pd
from Sentimientos import sentimientos
from Emociones import emociones

st.set_page_config(layout="wide")

datos=pd.read_csv("https://raw.githubusercontent.com/sebasur90/tweets_credicoop/main/tweets_historicos/tweets.csv")
st.session_state['datos']=datos


def main():
    pages = {
        "Principal": page_home,
        "sentimientos":sentimientos,
        "emociones":emociones,
        "Movimientos": "pagina_movimientos_funcion",
        # "PCA":page_pca,
        # "Random forest":random_forest,
        # "KNN: vecinos mas cercanos":page_knn

    }

    # If 'page' is present, update session_state with itself to preserve
    # values when navigating from Home to Settings.
    if "page" in st.session_state:
        st.session_state.update(st.session_state)

    # If 'page' is not present, setup default values for settings widgets.
    else:
        st.session_state.update({
            # Default page
            "page": "Home",
        })

    with st.sidebar:
        page = st.radio("Seleccionar pagina", tuple(pages.keys()))

    pages[page]()
    

def page_home():
    st.title("Termometro Twitts ")
    st.dataframe(datos)
    
    


if __name__ == "__main__":
    main()