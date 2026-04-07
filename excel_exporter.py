from openpyxl import Workbook
from record_manager import get_records
from datetime import date

def export_excel():
    wb = Workbook()
    ws = wb.active
    ws.append([
        "Plate", "In Time", "Out Time",
        "Plate Confidence", "Material", "Material Confidence"
    ])

    for r in get_records():
        ws.append(list(r.values()))

    fname = f"anpr_log_{date.today()}.xlsx"
    wb.save(fname)
    print(f"✅ Excel saved: {fname}")
