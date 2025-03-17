import xml.etree.ElementTree as ET
import json

XML_FILE = r"C:\Users\marco.davanzo\Projects\DashboardOffertePython\offerte\PO_Offerte_E_MLIBERO_20250317.xml"
JSON_FILE = "data/companies.json"

def extract_partita_iva(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    print(root.tag)
    partite_iva = set()
    for piva in root.iter('PIVA_UTENTE'):
        if piva is not None and piva.text:
            partite_iva.add(piva.text.strip())
    
    return sorted(partite_iva)

def create_json_schema(partite_iva, json_file):
    data = {p_iva: "" for p_iva in partite_iva}
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
partite_iva = extract_partita_iva(XML_FILE)
create_json_schema(partite_iva, JSON_FILE)