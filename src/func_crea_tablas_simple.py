from dash import dash_table


def create_table_simple(id, name, data):
    return dash_table.DataTable(
        id=id,
        columns = [
            {"name": data, "id": data},
            {"name": "EN_PLANTILLA","id": "EN_PLANTILLA",},
        ],
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        style_data=   {'color':  '#ffffff',
                       'backgroundColor':'#621132'},
        fixed_rows =  {'headers':True},
        style_table = {'maxHeight':'px',
                       'backgroundColor':'#621132',                        
                       'color':  '#ffffff'},
        style_header = {'backgroundColor':'#000000',
                        'fontWeight':'bold',
                        'border':'4px solid white',
                        'textAlign':'center'},
        style_cell =  { 'textAlign':'left',
                        'border':'4px solid white',
                        'color':'#b38e5d',
                        'maxWidth':'3px',                           
                        'textOverflow':'ellipsis'
            }
    )
