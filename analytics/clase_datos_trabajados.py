

class Datos_trabajados():
    def __init__(self,datos) -> None:
        self.datos_crudos=datos

    def agrega_col_ano_mes_dia(self):
        def funcion(a,b,c):                
            return f"{str(a)}-{str(b)}-{str(c)}"
        self.datos_crudos['ano_mes_dia']=self.datos_crudos.apply(lambda x: funcion(a = x['ano'], b = x['mes'], c = x['dia']), axis=1)    
        return self.datos_crudos

    def agrupa_dia(self):
        self.agrega_col_ano_mes_dia()
        agrupados_dia=self.datos_crudos.groupby('ano_mes_dia')['negativos', 'neutros', 'positivos',
        'joy', 'sadness', 'surprise', 'anger', 'disgust', 'fear', 'hateful', 'targeted', 'aggressive'].mean()  
        agrupados_dia=agrupados_dia.reset_index()  
        return agrupados_dia

    def cuenta_palabras(self):
        self.datos_crudos['cant_palabras']=self.datos_crudos.text.map(lambda x : len(x.split(" ")))    
        return self.datos_crudos

    def correlacion_sent_emo_hate(self):
        datos_corr=self.datos_crudos[['negativos', 'neutros', 'positivos',
       'joy', 'sadness', 'surprise', 'anger', 'disgust', 'fear',
        'hateful', 'targeted', 'aggressive']]
        datos_corr=datos_corr.corr()    
        return datos_corr