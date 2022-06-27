import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from clase_datos_trabajados import Datos_trabajados

def emociones():
    datos_trabajados=Datos_trabajados(st.session_state['datos'])


    #grafico 3d de sentimientos
    datos=st.session_state['datos']
    st.title("emociones")

    #grafico 3d de emociones
    fig2 = px.scatter_3d(datos, x='hateful', y='targeted', z='aggressive',
            color='sentiment',hover_name="sentiment", hover_data=["text"],width=1920, height=600,
            title="Scatter plot del hate")
    fig2.update_layout(hovermode="closest")
    


    fig3 = make_subplots()
    columnas=[ 'joy', 'sadness', 'surprise', 'anger', 'disgust', 'fear']    
    agrupados_dia=datos_trabajados.agrupa_dia()     
    for col in columnas:
        fig3.add_trace(go.Scatter(x=agrupados_dia.ano_mes_dia.values, y=agrupados_dia[col].values,
                mode='lines+markers',				name=col))



                

    return st.plotly_chart(fig2) ,st.plotly_chart(fig3)