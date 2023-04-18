import plotly.express as px


def crear_grafico_pie(df, filtrarPor, my_dropdown, name,names,title):
    # filtrar el dataframe por la unidad seleccionada
    dff = df[df[filtrarPor]==my_dropdown]
    
    # contar el número de elementos por rama
    dff = dff.groupby([names]).size().reset_index(name=name)
    
    # crear el gráfico de tarta
    fig_pie = px.pie(
        data_frame=dff,
        names=names,
        values=name,
        color_discrete_sequence=px.colors.sequential.RdBu,
        title=title,
        width=500, # Ancho del gráfico en píxeles
        height=500,# Alto del gráfico en píxeles
      
    )                   
    # Modifica el tamaño de la letra de los porcentajes
   
    
    return fig_pie


