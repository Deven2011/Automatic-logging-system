from datetime import datetime
from record_manager import add_record

active_trucks = {}

def handle_plate(plate, confidence):
    now = datetime.now().strftime("%H:%M:%S")

    if plate not in active_trucks:
        active_trucks[plate] = {
            "in_time": now,
            "confidence": confidence
        }
        print(f"🟢 ENTRY: {plate} at {now}")

    else:
        record = active_trucks.pop(plate)
        add_record(
            plate=plate,
            in_time=record["in_time"],
            out_time=now,
            plate_conf=confidence,
            material="REVIEW",
            material_conf="LOW"
        )
        print(f"🔴 EXIT: {plate} at {now}")
