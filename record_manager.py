daily_records = []

def add_record(plate, in_time, out_time, plate_conf, material, material_conf):
    daily_records.append({
        "plate": plate,
        "in_time": in_time,
        "out_time": out_time,
        "plate_confidence": plate_conf,
        "material": material,
        "material_confidence": material_conf
    })

def get_records():
    return daily_records
