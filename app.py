import json
from dash import Dash, html, dcc, callback, Output, Input, dash_table
import plotly.express as px
import pandas as pd
import xml.etree.ElementTree as ET


tree = ET.parse(r'offerte/PO_Offerte_E_MLIBERO_20250317.xml')
root = tree.getroot()

app = Dash()

nomiPrezzi = [
     'MP EE DOME',
     'PREZZO MATERIA PRIMA',
     'Spread',
     'Prezzo Componente Energia Elettricità',
     'Corrispettivo al consumo',
     'Corrispettivo Variabile'
]

data = []
for offerta in root.iter('offerta'):
    if(offerta.find('DettaglioOfferta/TIPO_CLIENTE').text == "01"):
        company = offerta.find('IdentificativiOfferta/PIVA_UTENTE').text
        nomeOfferta = offerta.find('DettaglioOfferta/NOME_OFFERTA').text
        durata = offerta.find('DettaglioOfferta/DURATA').text
        urlOfferta = offerta.find('DettaglioOfferta/Contatti/URL_OFFERTA').text if  offerta.find('DettaglioOfferta/Contatti/URL_OFFERTA') != None else ''
        dataInizioVal = offerta.find('ValiditaOfferta/DATA_INIZIO').text.split('_')[0]
        dataFineVal = offerta.find('ValiditaOfferta/DATA_FINE').text.split('_')[0]
        costoKw = ''
        costoEnergiaVerde = ''
        for componente in offerta.findall('ComponenteImpresa'):
            nome = componente.find('NOME').text
            if nome == "Prezzo":
                costoKw = f"{componente.find('IntervalloPrezzi/PREZZO').text} €/kWh"
            if nome in nomiPrezzi:
                for prezzo in componente.findall('IntervalloPrezzi'):
                    fascia = prezzo.find('FASCIA_COMPONENTE').text
                    costo = prezzo.find('PREZZO').text
                    costoKw += f"Fascia {fascia}: {costo} €/kWh\n"
            if nome == 'Energia Verde':
                    costoEnergiaVerde = componente.find('IntervalloPrezzi/PREZZO').text
        data.append({"Azienda": company, 
                    "Nome Offerta" : nomeOfferta, 
                    "Durata" : durata, 
                    "URL" : urlOfferta,
                    "Data Inizio" : dataInizioVal,
                    "Data Fine" : dataFineVal,
                    "Costo kW" : costoKw,
                    "Costo Energia Verde" : costoEnergiaVerde
                    })
    

# Requires Dash 2.17.0 or later
app.layout = [
    
     html.H1(children='Offerte ultimo mese', style={'textAlign':'center','font-family': 'system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"'}),
     dash_table.DataTable(
        data=data,
        page_size=30,
        id='offerte',
        columns=[
                  {"name": "Azienda", 'id': "Azienda" },
                  {"name": "Nome Offerta", 'id': "Nome Offerta" },
                  {"name": "Durata", 'id': "Durata" },
                  {"name": "URL", 'id': "URL" },
                  {"name": "Data Inizio", 'id': "Data Inizio" },
                  {"name": "Data Fine", 'id': "Data Fine" },
                  {"name": "Costo kW", 'id': "Costo kW" },
                  {"name": "Costo Energia Verde", 'id': "Costo Energia Verde" },
            
        ],
        style_cell = {'text-align' : 'left'},
        style_header={
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white'
        },
        style_data={
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white'
        },
        filter_action='native',
                        
    )
                            
]

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
