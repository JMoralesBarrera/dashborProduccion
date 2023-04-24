import pandas as pd

from dash import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
#import dash_bootstrap_components as dbc
from flask import Flask
import dash_table
from func_crea_Graficos import crear_grafico_pie
from func_crea_tablas_simple import create_table_simple
from decorador_Grafico import *
import decorador_dropdown
from func_crea_tabla_comparativa import crear_tabla_comparativa
import dash_auth

# import dash_bootstrap_components as dbc
LISTA_USUARIO =[['DIRECCION','A01'],['SUBDIRECCION','A02'],['JESUS','A03'],['JEFEDEPTO','A04']]

meta_tags= [{'name':'viewport',
            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2,minimum-scale=0,5'}]
#external_stylesheets=[meta_tags,'assets/css.css','assets/normalize.css']
#https://necolas.github.io/normalize.css/

app = dash.Dash(__name__)#,  external_stylesheets=external_stylesheets)
server = Flask(__name__)
auth= dash_auth.BasicAuth(app,LISTA_USUARIO)
#server=app.server
# Read data from Excel file
df = pd.read_excel('Plantilla.xlsx', sheet_name='Resultados')
df = df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
df = df[[ 'RFC', 'A.Paterno', 'A.Materno', 'Nombre', 'SUELDO TAB', 'CÓDIGO', 'ADSCRIPCION', 'Area Hosp', 'Sub_Area_Hosp', 'NUCLEOS', 'RAMA', 'UNIDAD', 'TURNO', 'EN_PLANTILLA', 'TIPO CONTRATO','NORMATIVA']]

# Define colors for the app
colors = {
    'background': '#621132',
    'background2': '#b38e5d',
    'background3': '#000000',
    'text': '#b38e5d',
    'text1': '#621132',
    'text2': '#ffffff',
    'text3': '#000000',
}
 
#-------------Decorador que da iteractividad al segundo dropdown------------------
@app.callback(
  
    Output('seleccionaUnidades', 'options'),
    Input('seleccionaUnidad', 'value')
)

def set_cities_options(chosen_state):       
            dff = df[df['UNIDAD']==(chosen_state)]   
            return [{'label': c, 'value': c} for c in sorted(dff.ADSCRIPCION.unique())]

#--------------- Decorador para mostrar una unidad al inicio del programa --------------------
@app.callback(
    Output('seleccionaUnidades', 'value'),
    Input('seleccionaUnidades', 'options')
    )
def set_cities_options(chosen_state1):  
        return [k['value']for k in chosen_state1 ][0]

#--------------- Decorador para mostrar unidadades al inicio del programa ---xx-----------------
@app.callback(
    Output('seleccionaUnidad', 'value'),
    Input('seleccionaUnidad', 'options')
    )
def set_cities_options(chosen_state1):  
    return [k['value']for k in chosen_state1 ][0]

 #----------------Decorador gráfico -----------------------------------------
def update_graph_pie(component_id_Output, component_id_Input, tipo ,columna_numero, columna_nombre, titulo):
    @app.callback(
        Output(component_id=component_id_Output, component_property='figure'),
        Input(component_id=component_id_Input, component_property='value')
    )
    def update_graph(my_dropdown):
        return crear_grafico_pie(df, tipo, my_dropdown, columna_numero, columna_nombre, titulo)
    return update_graph

# Uso de la función de actualización de gráfico para generar las funciones de devolución de llamada
update_graph_pie1 = update_graph_pie('the_graphRama', 'seleccionaUnidad','UNIDAD','numeroRama', 'RAMA', 'Distribución Global por Ramas')
update_graph_pie2 = update_graph_pie('the_graphTurnos','seleccionaUnidad', 'UNIDAD','numeroTurno', 'TURNO', 'Distribución Global por Turnos')
update_graph_pie3 = update_graph_pie('theGraphUnidadRamas','seleccionaUnidades', 'ADSCRIPCION','numeroRama', 'RAMA', 'Distribución por Unidad  por Ramas')
update_graph_pie4 = update_graph_pie('theGraphUnidadTurnos','seleccionaUnidades', 'ADSCRIPCION','numeroTurno', 'TURNO', 'Distribución por Unidad  por Turnos')

#------------------Decorador tabla global rama---------------------
def generate_callback(component_id_output, component_id_input, component_property,tipo, groupby_column):
    @app.callback(
        Output(component_id=component_id_output, component_property=component_property),
        Input(component_id=component_id_input, component_property='value')
    )
    def update_table(seleccionaUnidad):
        dffTabla = df[df[tipo] == seleccionaUnidad]
        dffTabla = dffTabla.groupby([groupby_column]).size().reset_index(name='EN_PLANTILLA')

        # Calcula el total de la columna 'EN_PLANTILLA'
        TOTAL = dffTabla['EN_PLANTILLA'].sum()

        # Agrega una fila al final de la tabla con el total
        dffTabla = dffTabla.append({groupby_column: 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

        return dffTabla.to_dict('records')

# Llamada a la función para generar el callback
generate_callback('tabla', 'seleccionaUnidad','data','UNIDAD', 'RAMA')
generate_callback('tabla2', 'seleccionaUnidad','data', 'UNIDAD','TURNO')
generate_callback('tabla3', 'seleccionaUnidades','data', 'ADSCRIPCION','RAMA')
generate_callback('tabla4', 'seleccionaUnidades','data', 'ADSCRIPCION','TURNO')

#------------decorador tabla global rama ----------------
@app.callback(
 Output(component_id='tabla6', component_property='data'),   
 Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
      
     dffTabla6= df.groupby(['UNIDAD']).size().reset_index(name='EN_PLANTILLA')
     
      # Calcula el total de la columna 'EN_PLANTILLA'
     TOTAL = dffTabla6['EN_PLANTILLA'].sum()

    # Agrega una fila al final de la tabla con el total
     dffTabla6 = dffTabla6.append({'UNIDAD': 'TOTAL', 'EN_PLANTILLA': TOTAL}, ignore_index=True)

     return dffTabla6.to_dict('records')  

#----------------------------------------------------------------------------

#data table
@app.callback(
Output(component_id='table1X', component_property='data'),
Input(component_id='seleccionaUnidades', component_property='value')    
)

def update_table(seleccionaUnidades):
   
    tipo_hospital={
        
        'C0':{'MATUTINA':0, 'VESPERTINA':0, 'VELADA A':0, 'VELADA B':0, 
        'ESPECIAL DIURNA':0, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C30':{'MATUTINA':72, 'VESPERTINA':29, 'VELADA A':9, 'VELADA B':8, 
        'ESPECIAL DIURNA':10, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C60':{'MATUTINA':123, 'VESPERTINA':56, 'VELADA A':31, 'VELADA B':29, 
        'ESPECIAL DIURNA':30, 'ESPECIAL NOCTURNA':0, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C90':{'MATUTINA':229, 'VESPERTINA':115, 'VELADA A':60, 'VELADA B':46, 
        'ESPECIAL DIURNA':36, 'ESPECIAL NOCTURNA':1, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        'C120':{'MATUTINA':269, 'VESPERTINA':144, 'VELADA A':71, 'VELADA B':64, 
        'ESPECIAL DIURNA':44, 'ESPECIAL NOCTURNA':9, 'JORNADA ACUMULADA':0,'NO_DEFINIDO':0},

        }
   
    # Inicializamos dffTabla1x como un DataFrame vacío
    dffTabla1x = pd.DataFrame()
 
    if seleccionaUnidades in ('HOSPITAL GENERAL DE APAN','HOSPITAL GENERAL DE ACTOPAN','HOSPITAL MATERNO INFANTIL','HOSPITAL GENERAL DE HUEJUTLA'):        
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C60'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades in ('HOSPITAL GENERAL DE HUICHAPAN', 'HOSPITAL INTEGRAL DE JACALA', 'HOSPITAL ZIMAPAN'):
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C30'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades in ('HOSPITAL GENERAL DEL VALLE DEL MEZQUITAL IXMIQUILPAN', 'HOSPITAL GENERAL DE TULA'):
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C90'][x] if not pd.isnull(x) else 0)
    elif seleccionaUnidades == 'HOSPITAL GENERAL TULANCINGO':
            df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C120'][x] if not pd.isnull(x) else 0)
    else:   df['NORMATIVA'] = df['TURNO'].apply(lambda x: tipo_hospital['C0'][x] if not pd.isnull(x) else 0)
 
    dffTabla = df[df['ADSCRIPCION']==(seleccionaUnidades)]
    dffTabla1x= dffTabla.groupby(['ADSCRIPCION','TURNO','NORMATIVA']).size().reset_index(name='EN_PLANTILLA')
    
        # Calcula el total de la columna 'EN_PLANTILLA'
    TOTAL = dffTabla1x['EN_PLANTILLA'].sum()
    TOTAL1= dffTabla1x['NORMATIVA'].sum()
    # Agrega una fila al final de la tabla con el total
    dffTabla1x =  dffTabla1x.append({'ADSCRIPCION': 'TOTAL', 'EN_PLANTILLA': TOTAL,  'NORMATIVA':TOTAL1}, ignore_index=True)

    return dffTabla1x.to_dict('records')
  
  #DECORADOR TABLA3
@app.callback(   
   
    Output(component_id='table3A', component_property='data'),    
    
    Input('table1X', 'derived_virtual_data'),     
    Input('table1X', 'derived_virtual_selected_rows'),
    Input('table1X', 'selected_rows'),)     
        
def update_graphs(derived_virtual_data,derived_virtual_selected_rows,selected_rows):
    
    if (selected_rows)is None:
        selected_rows = []
    else:
          
        df=pd.DataFrame(derived_virtual_data)
        df_filterd = df[df.index.isin(selected_rows)]
        return df_filterd.to_dict('records')
   
#DECORADOR TABLA4
@app.callback(
    Output(component_id='table4A', component_property='data'),
   [Input('table3A','data')])
       
def update_graphs(data):
  
    global dataf 
           
    if data !=None:
                
        for dataf in data:
            del dataf['EN_PLANTILLA']                   
                   
            d= df[(df['ADSCRIPCION'] ==dataf['ADSCRIPCION']) &  (df['TURNO'] ==dataf['TURNO']) ]
             
            sjs= pd.DataFrame(d)           
       
            return sjs.to_dict('records')
       
#----------------------app.layout-------------------------

app.layout = html.Div([
   #---------------------Create header--------------------------------------------------------   
        html.Div(className='header_title',     
            children=[
                html.Img(src='assets/logo.png'),
                html.Marquee(id='marquee', children = 'Prevengamos las picaduras de mosquitos ¡no a la malaria!') ,
                html.H1('DIRECCIÓN DE RECURSOS HUMANOS',),
                html.H4('QNA 6/2023'),
                html.Hr() ]
        ),
    
#--------------------------tabla global secretaria----------------------------        
        html.Div(children=[
            html.Label('Distribucion Global:', className='etiqueta'),
            create_table_simple('tabla6', 'UNIDAD', 'UNIDAD'), 
            html.Hr(),           
        ]),

        html.Div(className='dist_Unidad',
                  
            children=[
                
                html.Label('Seleccione una Unidad:', className='etiqueta'),
#-------------------Primer Dropdown-----------------------------------------
                dcc.Dropdown(
                id='seleccionaUnidad',
                options=[{'label': s, 'value': s} for s in sorted(df.UNIDAD.unique())],
                value='HOSPITALES',
                clearable=False,
                searchable=False,
                style={'backgroundColor': colors['background2'], }),
       
            ]),  
   
    html.Div(className= 'distUnidadRama',
        children=[
            dcc.Graph(id='the_graphRama'),
            create_table_simple('tabla', 'RAMA', 'RAMA')
        ],style= {'backgroundColor':  colors['background2'],'display':'flexbox'},
    ),
    html.Div(className= 'distUnidadturno',
        children=[
            dcc.Graph(id='the_graphTurnos'),
            create_table_simple('tabla2', 'TURNO', 'TURNO')
        ]),

      ############################################## 
         
        html.Div([
                html.Label('Seleccione una Adscripción:', className='etiqueta'),
                #----------------------Segundo Dropdown--------------------------------------
                dcc.Dropdown(  
                id='seleccionaUnidades',   
                options=[],
                multi=False,
                style={'backgroundColor': colors['background2'],})        
        ],style={'border-color': '#333', 'border-width': '2px', }),

        html.Div(className= 'distAdscripcionRama',
                 children=[             
                dcc.Graph(id='theGraphUnidadRamas'),
                create_table_simple('tabla3', 'RAMA', 'RAMA'),               
        ]),

        html.Div(className= 'distAdscripcionTurno',
                 children=[     
         dcc.Graph(id='theGraphUnidadTurnos'), 
         create_table_simple('tabla4', 'TURNO', 'TURNO'),     

#  compara la normativa contra la plantilla

        ]), 

html.Div([
   html.Hr(),
html.Label('Comparación de Normativa VS Plantilla:', className='etiqueta'),
 # tabla nucleos
    crear_tabla_comparativa(df),

html.Label('Analítico por Trabajador:', className='etiqueta'),              
# tabla POR PERSONAS
dash_table.DataTable(
        id='table3A',      
       
        #data=df.to_dict('records'),
        #data = dffTabla1.to_dict('records'),
        columns = [{'id':i, 'name':i, 'deletable':True} for i in 
                   #SI SE LE PONE RFC DESGLOSA UNO A UNO CASO CONTRARIO ACUMULA
                   df.loc[:,['TURNO','EN_PLANTILLA']]],
    
            
),
# Ulitma tabla sirve para mostrar el detalle de los trabajadores
dash_table.DataTable(
        id='table4A',      
     
        columns = [{'id':i, 'name':i, 'deletable':True,} for i in 
                   #SI SE LE PONE RFC DESGLOSA UNO A UNO CASO CONTRARIO ACUMULA
                   df.loc[:,['RFC','A.Paterno','A.Materno','Nombre','CÓDIGO','TIPO CONTRATO']]
                                        
                   ],    

                style_data={
              
                'color':  '#ffffff',
                'backgroundColor':'#621132'
            },
            fixed_rows = {'headers':True},

#le da estilo a la ultima tabla:
            style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff',
                            },

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},
            
)

])

],className='contenedor')

df.to_csv('modificado.csv')

if __name__  == '__main__':
       app.run(host="0.0.0.0",port=8000,debug=True)