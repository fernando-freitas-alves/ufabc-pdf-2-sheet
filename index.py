# Define the url and filename's string variables that contain the URL of the PDF file to be converted and the new files name, repectively.
url = "http://prograd.ufabc.edu.br/pdf/turmas_salas_docentes_sa_2018.1.pdf"
filename = "2018.1_SA" # without extention
pdf_filename  = filename + '.pdf'
csv_filename  = filename + '.csv'
json_filename = filename + '.json'

# Import functions notebook.
from functions import *

# Download and preview the PDF file.
downloadPDF(url, pdf_filename)
IFrame(pdf_filename, 600, 300)

# The PDF file is converted to a CSV file (this might take a while).
convertPDFtoCSV(pdf_filename, csv_filename)

# The CSV file is then processed into a properly configured JSON file.
json_data = convertCSVtoJSON(csv_filename, json_filename)

# Preview the JSON data.
showJSON(json_data)

# Finally, process the JSON data into a spreadsheet.
# %run functions.ipynb
sheet = convertJSONtoSheet(json_data)
df = sheet.df
# sheet

df.reset_index()

from IPython.display import display, HTML
include = """
    <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    </head>
"""
js = """
    <script> 
        $('option').mousedown(function(e) {
            e.preventDefault();
            $(this).prop('selected', $(this).prop('selected') ? false : true);
            $(this).parent().focus();
            return false;
        });
    </script>
"""

getColumnIndex = lambda column_name: [index for index,column in enumerate(df.index.names) if column_name in column][0]

df_reseted = df.reset_index()
columnsList = ['Subcódigo', 'Disciplina', 'Período', 'Turma']
# options = sorted(df.reset_index()['Disciplina'].unique().tolist())
options = sorted(['[' + '] '.join(item[0:2]) + ' (' + item[2] + ', ' + item[3] + ')' for item in df_reseted[columnsList].values.tolist()])
allItems = 'Todas'
allOptions = [allItems] + options


from ipywidgets import *
 
Filter = Text(
    description = '',
    placeholder = 'Pesquisar',
    value       = ''
)

ClearFilter = Button(
    button_style = '', # 'success', 'info', 'warning', 'danger' or ''
    tooltip      = 'Clique para limpar o filtro',
    icon         = 'remove', # https://www.w3schools.com/icons/fontawesome_icons_webapp.asp
#     layout       = Layout(width='30px')
    layout       = {'width': '30px'}
)

List = SelectMultiple(
    description = '',
    options     = options,
    value       = (),
    layout       = {'width': '50%', 'height': '200px'}
)

Choice = SelectMultiple(
    options     = allOptions,
    value       = (allItems,),
    disabled    = True,
    layout      = {'display': 'none'}
)

ClearChoice = Button(
    description  = 'Limpar seleção',
    button_style = '', # 'success', 'info', 'warning', 'danger' or ''
    tooltip      = 'Clique para limpar a seleção',
    icon         = 'eraser', # https://www.w3schools.com/icons/fontawesome_icons_webapp.asp
    layout       = {'width': '50%'}
)

def filterOnChange(*args):
    value = Filter.value.lower()
    Choice_value = Choice.value
    if value:
        List.options = [item for item in options if value in item.lower() or item in Choice_value]
    else:
        List.options = options
    List.value = [item for item in Choice_value if item in List.options]
    Choice.value = Choice_value
Filter.observe(filterOnChange, 'value')

def filterOnSubmit(text):
    List.value = List.options
    listOnChange()
Filter.on_submit(filterOnSubmit)

def clearFilterOnClick(button=None):
    Filter.value = ''
    filterOnChange()
ClearFilter.on_click(clearFilterOnClick)

def listOnChange(*args):
    query = List.value
    if query:
        Choice.value = query
List.observe(listOnChange, 'value')

def clearChoiceOnClick(button):
    Choice.value = (allItems,)
    clearFilterOnClick()
ClearChoice.on_click(clearChoiceOnClick)

def filterTable(query = ()):
    if allItems in query:
        df2 = df
    else:
        df2 = filterDataFrameByColumn(df, columnsList, query)
    display(df2.style.set_properties(**{'text-align': 'left'}))
    display(HTML(include))
    display(HTML(js))
    return None

def filterDataFrameByColumn(df, column_name, query):
    items = []
    for column in column_name:
        column_index = getColumnIndex(column)
        column_items = df.index.get_level_values(column_index)
        column_items = [item.lower() for item in column_items]
        items.append(column_items)
    
    indexes_group = []
    for i in range(len(query)):
        q = query[i]
        subcodigo,  _, q     = q[1:].partition('] ')
        disciplina, _, q     = q.rpartition(' (')
        periodo,    _, turma = q[:-1].rpartition(', ')
        valuesToFilterBy = [subcodigo, disciplina, periodo, turma]
        
        indexes_list = []
        for j in range(len(valuesToFilterBy)):
            value = valuesToFilterBy[j].lower()
            indexes_list.append([index for index,item in enumerate(items[j]) if value == item])
        indexes_group.append(indexes_list)

    indexes = []
    for item in indexes_group:
        indexes_set = set(item[0])
        for index_list in item[1:]:
            indexes_set &= set(index_list)
        indexes += list(indexes_set)

    return df.iloc[indexes]

form_items = [
#     Box([Label(value='Pesquisar:', layout=Layout(width='70px')), Label(), Label()], layout={'flex_flow':'column'}),
    Box([HBox([Filter, ClearFilter]),
         List,
         ClearChoice],  layout={'flex_flow':'column', 'width':'100%'})
]

display(VBox([
    Label(value='Selecione as disciplinas na lista abaixo para filtrar a tabela.'),
    Box(form_items)
]))
interact(filterTable, query=Choice);

