def match_plate(new_plate, existing_plates):
    for plate in existing_plates:
        if new_plate in plate or plate in new_plate:
            return plate
    return None
