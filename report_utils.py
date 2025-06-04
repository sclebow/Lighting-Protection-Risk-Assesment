import pandas as pd
import io
from odf.opendocument import OpenDocumentText
from odf.text import P, H
from odf.table import Table, TableRow, TableCell

def generate_csv_report(data_dict):
    df = pd.DataFrame([data_dict])
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue().encode('utf-8')

def generate_odt_report(data_dict):
    doc = OpenDocumentText()
    doc.text.addElement(H(outlinelevel=1, text='NFPA 780 Lightning Risk Assessment Report'))
    doc.text.addElement(P(text='This report summarizes the results of the simplified lightning risk assessment.'))
    doc.text.addElement(H(outlinelevel=2, text='Input Parameters'))
    table = Table()
    for k, v in data_dict.items():
        row = TableRow()
        cell1 = TableCell()
        cell1.addElement(P(text=str(k)))
        cell2 = TableCell()
        cell2.addElement(P(text=str(v)))
        row.addElement(cell1)
        row.addElement(cell2)
        table.addElement(row)
    doc.text.addElement(table)
    output = io.BytesIO()
    doc.save(output)
    output.seek(0)
    return output.read()
