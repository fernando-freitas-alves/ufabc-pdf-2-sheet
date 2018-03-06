# Import configuration notebook.

from config import *

# Define ```displayFileLink``` function that displays a link of a file with ```filename``` string filename prefixed by the message given by ```message``` string.

def displayFileLink(message, filename):
    divText = '<div style="display:inline-block">' + message + '&nbsp</div>'
    file = FileLink(filename, result_html_prefix=divText)
    display(file)

# Define ```downloadPDF``` function that downloads a PDF file from a link provided by ```url``` string and rename it to ```filename_pdf``` input string.

def downloadPDF(url, pdf_filename):
    result = subprocess.run(['wget', url, '-O', pdf_filename])
    result.stdout
    displayFileLink('PDF file saved as:', pdf_filename)

# Define ```convertPDFtoCSV``` function that converts a PDF file given by ```pdf_filename``` string file name to a CSV file with filename given by ```csv_filename``` input (*credits to [tabula-java team](https://github.com/tabulapdf/tabula-java)*).

def convertPDFtoCSV(pdf_filename, csv_filename):
    result = subprocess.run(['java', '-Dfile.encoding=utf-8', '-jar', 'tabula.jar', '-l', '--pages', '3', pdf_filename, '-o', csv_filename])
    result.stdout
    displayFileLink('CSV file saved as:', csv_filename)

# Define ```convertCSVtoJSON``` function that converts a CSV file with filename given by ```csv_filename``` string input to a JSON properly processed file with filename given by ```json_filename``` input and data given by ```json_data``` output.

def convertCSVtoJSON(csv_filename, json_filename):
    with open(csv_filename, encoding="utf-8") as file:
        import csv
        csv_data = csv.reader(file, delimiter=',', quotechar='"')
        full_data = []
        index = -1
        for row in csv_data:
            index = index + 1
            if index:
                column = 0
                for cell in row:
                    column = column + 1
                    data = cell.replace('\r','').replace('\n',' ').replace(' , ',', ').strip()
                    if   data == '¬': data = ''
                    elif data == '0': data = ''

                    # Código
                    if column == 1:
                        codigo = data.upper()

                    # Disciplina - turma
                    elif column == 2:
                        # Campus
                        data, _, campus = data.rpartition('(')
                        campus = title_pos_tag(campus[:-1])

                        # Disciplina
                        disciplina, _, data = data.strip().rpartition(' ')
                        disciplina = title_pos_tag(disciplina)

                        # Turma e período
                        turma, _, periodo = data.strip().rpartition('-')
                        turma   = turma.upper()
                        periodo = periodo.capitalize()

                        # Subcódigo
                        subcodigo, _, sufixo = codigo.partition('-') # DA1ESZM035-17SA = D+A1(ESZM035|-|17)SA
                        subcodigo = subcodigo[1+len(turma):] + '-' + sufixo[:2]


                    # Teoria
                    elif column == 3:
                        for week in week_names:
                            data = data.replace(week, '\n' + week)
                        teoria = data.replace(', \n','\n').strip().splitlines()

                        teoria_num_of_days = len(teoria)
                        teoria_dia_da_semana = [None]*teoria_num_of_days
                        teoria_entrada       = [None]*teoria_num_of_days
                        teoria_saida         = [None]*teoria_num_of_days
                        teoria_sala          = [None]*teoria_num_of_days
                        teoria_frequencia    = [None]*teoria_num_of_days
                        for day in range(teoria_num_of_days):
                            data = teoria[day]
                            teoria_dia_da_semana[day], _, data                   = data.partition(' das ')
                            teoria_entrada[day],       _, data                   = data.partition(' às ')
                            teoria_saida[day],         _, data                   = data.partition(', sala ')
                            teoria_sala[day],          _, teoria_frequencia[day] = data.partition(', ')

                            teoria_dia_da_semana[day] = teoria_dia_da_semana[day].capitalize()
                            teoria_frequencia[day]    = teoria_frequencia[day].capitalize()
                            teoria_sala[day]          = teoria_sala[day].upper()

                    # Prática
                    elif column == 4:
                        for week in week_names:
                            data = data.replace(week, '\n' + week)
                        pratica = data.replace(',\n','\n').strip().splitlines()

                        pratica_num_of_days = len(pratica)
                        pratica_dia_da_semana = [None]*pratica_num_of_days
                        pratica_entrada       = [None]*pratica_num_of_days
                        pratica_saida         = [None]*pratica_num_of_days
                        pratica_sala          = [None]*pratica_num_of_days
                        pratica_frequencia    = [None]*pratica_num_of_days
                        for day in range(pratica_num_of_days):
                            data = pratica[day]
                            pratica_dia_da_semana[day], _, data                    = data.partition(' das ')
                            pratica_entrada[day],       _, data                    = data.partition(' às ')
                            pratica_saida[day],         _, data                    = data.partition(', sala ')
                            pratica_sala[day],          _, pratica_frequencia[day] = data.partition(', ')

                            pratica_dia_da_semana[day] = pratica_dia_da_semana[day].capitalize()
                            pratica_frequencia[day]    = pratica_frequencia[day].capitalize()
                            pratica_sala[day]          = pratica_sala[day].upper()

                    # Docente teoria
                    elif column == 5:
                        docente_teoria = title_pos_tag(data)

                    # Docente prática
                    elif column == 6:
                        docente_pratica = title_pos_tag(data)

                teoria = []
                i = -1
                for day in range(teoria_num_of_days):
                    i = i + 1
                    teoria_new = {'id': i,
                                  'dia_da_semana': teoria_dia_da_semana[day],
                                  'horario_de_entrada': teoria_entrada[day],
                                  'horario_de_saida': teoria_saida[day],
                                  'sala': teoria_sala[day],
                                  'frequencia': teoria_frequencia[day]}
                    teoria.append(teoria_new)

                pratica = []
                i = -1
                for day in range(pratica_num_of_days):
                    i = i + 1
                    pratica_new = {'id': i,
                                   'dia_da_semana': pratica_dia_da_semana[day],
                                   'horario_de_entrada': pratica_entrada[day],
                                   'horario_de_saida': pratica_saida[day],
                                   'sala': pratica_sala[day],
                                   'frequencia': pratica_frequencia[day]}
                    pratica.append(pratica_new)

                new_data = {'id': index-1,
                            'codigo': codigo,
                            'subcodigo': subcodigo,
                            'disciplina': disciplina,
                            'campus': campus,
                            'periodo': periodo,
                            'turma': turma,
                            'teoria': teoria,
                            'pratica': pratica,
                            'docente_teoria': docente_teoria,
                            'docente_pratica': docente_pratica}
                full_data.append(new_data)

        import json
        with open(json_filename, 'w') as file:
            json.dump(full_data, file)
            displayFileLink('JSON file saved as:', json_filename)
        with open(json_filename, 'r') as file:
            json_data = json.load(file)
            return json_data

# Define ```sumMinutes``` function that returns the sum of ```minutes``` int input minutes to the ```time_str``` input string with format ```'%H:%M'```.

def sumMinutes(time_str, minutes):
    H,M = time_str.split(':')
    D = timedelta(hours=int(H), minutes=int(M)+minutes)
    D = datetime(1,1,1) + D
    new_time_str = D.strftime('%H:%M')
    return new_time_str

# Define ```compareTimes``` function that compares ```time_str_1``` and ```time_str_2``` input strings with format ```'%H:%M``` returning ```1```, ```0```, or ```-1``` if ```time_str_1``` is bigger, equal, or smaller than ```time_str_2```, respectively.

def compareTimes(time_str_1, time_str_2):
    H1,M1 = time_str_1.split(':')
    H2,M2 = time_str_2.split(':')
    H_diff = int(H1) - int(H2)
    M_diff = int(M1) - int(M2)
    if H_diff > 0 or H_diff == 0 and M_diff > 0:
        return 1
    elif H_diff == 0 and M_diff == 0:
        return 0
    else: return -1

# Define ```convertJSONtoSheet``` function that processes a JSON file with data given by ```json_data``` into a spreadsheet.

def convertJSONtoSheet(json_data):
    import numpy as np
    import pandas as pd
    # import qgrid
    
#     codigo          = []
    subcodigo       = []
    disciplina      = []
    campus          = []
    periodo         = []
    turma           = []
#     teoria          = []
#     pratica         = []
    docente_teoria  = []
    docente_pratica = []
    dias_da_semana  = []
    week_name_index = lambda week_name: [index for index,name in enumerate(week_names) if name.lower() == week_name.lower()][0]
    
    for materia in json_data:
#         codigo         .append(materia['codigo'])
        subcodigo      .append(materia['subcodigo'])
        disciplina     .append(materia['disciplina'])
        campus         .append(materia['campus'])
        if materia['periodo'].lower() == 'diurno':
            periodo_emoji = '<i class="em em-sunny"></i>'
        elif materia['periodo'].lower() == 'noturno':
            periodo_emoji = '<i class="em em-waxing_crescent_moon"></i>'
        else:
            periodo_emoji = ''
        periodo        .append(periodo_emoji + ' ' + materia['periodo'])
        turma          .append(materia['turma'])
#         teoria         .append(materia['teoria'])
#         pratica        .append(materia['pratica'])
        docente_teoria .append(materia['docente_teoria'])
        docente_pratica.append(materia['docente_pratica'])
        
        dias_da_semana_new = [''] * len(week_names)
        for day in materia['teoria'] + materia['pratica']:
#             sala_horario = day['horario_de_entrada'] + '-' + day['horario_de_saida'] + ' (' + day['sala'] + ')'
#             dia_da_semana = day['dia_da_semana']
#             for week in week_names:
#                 if week.lower() == dia_da_semana.lower():
#                     dias_da_semana_new.append(sala_horario)
#                 else:
#                     dias_da_semana_new.append('')
            index = week_name_index(day['dia_da_semana'])
            dias_da_semana_new[index] += day['horario_de_entrada'] + '-' + day['horario_de_saida'] + ' (<span class="sala">' + day['sala'] + '</span>)'
#         display(dias_da_semana_new)
        dias_da_semana.append(dias_da_semana_new)
    
    dias_da_semana_transposed = list(map(list, zip(*dias_da_semana)))
    week_names_titled = [week.title() for week in week_names]
    
    data = np.array([
        # codigo,
        subcodigo,
        disciplina,
        campus,
        periodo,
        turma,
        # teoria,
        # pratica,
    ] + dias_da_semana_transposed + [
        docente_teoria,
        docente_pratica
    ]).T
#     from pprint import pprint
#     pprint(data)
    
    columns = [
#         'Código',
        'Subcódigo',
        'Disciplina',
        'Campus',
        'Período',
        'Turma',
#         'Teoria',
#         'Prática',
    ] + week_names_titled + [
        'Docente teoria',
        'Docente prática'
    ]
    
    df = pd.DataFrame(data, columns=columns)
    df = df.set_index(['Subcódigo','Disciplina','Campus','Período','Turma'])
    df = df.sort_index(level=['Subcódigo','Período'])
#     df['#'] = df.groupby(level=[0,1]).cumcount() + 1
#     df = df.set_index('#', append=True)
    
    return df
    # grid_options = {
    #     'fullWidthRows': False,
    #     'syncColumnCellResize': True,
    #     'forceFitColumns': False,
    #     'defaultColumnWidth': 150,
    #     'rowHeight': 28,
    #     'enableColumnReorder': True,
    #     'enableTextSelectionOnCells': True,
    #     'editable': False,
    #     'autoEdit': False,
    #     'explicitInitialization': True,
    #     'maxVisibleRows': 25,
    #     'minVisibleRows': 15,
    #     'sortable': True,
    #     'filterable': True,
    #     'highlightSelectedCell': False,
    #     'highlightSelectedRow': True
    # }
    # sheet = qgrid.QGridWidget(df=df, grid_options=grid_options)
    # return sheet