import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from clase_datos_trabajados import Datos_trabajados
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))

def sentimientos():
    datos_trabajados=Datos_trabajados(st.session_state['datos'])


    #grafico 3d de sentimientos
    datos=st.session_state['datos']
    fig = px.scatter_3d(datos, x='negativos', y='neutros', z='positivos',
        color='sentiment', hover_name="sentiment", hover_data=["text"], width=1920, height=600,
        title="Scatter plot de los sentimientos")
    fig.update_layout(hovermode="closest")   
     

    
    fig3 = make_subplots()
    columnas=['negativos', 'neutros', 'positivos' ]
    agrupados_dia=datos_trabajados.agrupa_dia()     
    for col in columnas:
        fig3.add_trace(go.Scatter(x=agrupados_dia.ano_mes_dia.values, y=agrupados_dia[col].values,
                mode='lines+markers',				name=col))

    
    datos_palabras=datos_trabajados.cuenta_palabras()
    fig4 = plt.figure(figsize=(10, 4))
    sns.kdeplot(datos_palabras.cant_palabras, shade=True, hue=datos.sentiment)
    
    
    datos_corr=datos_trabajados.correlacion_sent_emo_hate()    
    sns.set_theme()
    fig7, ax = plt.subplots(figsize=(15, 6))
    sns.heatmap(datos_corr, annot=True,  linewidths=.8, ax=ax)


    return st.plotly_chart(fig)   ,st.plotly_chart(fig3) ,st.pyplot(fig4) ,st.pyplot(fig7) 
