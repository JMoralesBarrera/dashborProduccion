from dash import dash_table


def crear_tabla_comparativa(df):
    return dash_table.DataTable(
        id='table1X',
        #data = dffTabla1.to_dict('records'),
        columns = [{'id':c, 'name':c} for c in df.loc[:,['ADSCRIPCION','TURNO','EN_PLANTILLA','NORMATIVA']]],
        #virtualization=True,
        row_selectable='multi',
        style_data={
            #'color':  '#b38e5d',
            'color':  '#ffffff',
            'backgroundColor':'#621132'
        },
        fixed_rows = {'headers':True},

        style_table = {'maxHeight':'450px',
                          'backgroundColor':'#621132',
                         #  'color':  '#b38e5d'},
                           'color':  '#ffffff'},

            style_header = {'backgroundColor':'#000000',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'textAlign':'center'},

            style_data_conditional = [
                     {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  > {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'red',
                'fontWeight': 'bold',
                'textAlign':'center',         
            },
                
                  {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  < {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'yellow',
                'fontWeight': 'bold',
                 'textAlign':'center',     
            },
                
               {
                'if': {
                    'filter_query': '{EN_PLANTILLA}  = {NORMATIVA}' ,
                    'column_id': 'EN_PLANTILLA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'right',   
            },
                {
                'if': {
                    'filter_query': '{NORMATIVA} = {NORMATIVA}',
                    'column_id': 'NORMATIVA'
                },
                'color': 'lime',
               'fontWeight': 'bold',
                'textAlign':'center',   
            }  

              ],

            style_cell = {
                'textAlign':'left',
                'border':'4px solid white',
                 'color':'#b38e5d',
                 
                'maxWidth':'50px',
                # 'whiteSpace':'normal'
                'textOverflow':'ellipsis'

                });
 