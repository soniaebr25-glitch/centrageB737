# validation.py

def validate_inputs(config, passengers, oa, ob, oc,
                     takeoff_fuel=None, trip_fuel=None):

    # Maximum passengers
    if passengers > config["max_pax"]:
        return False, f"Maximum passengers = {config['max_pax']}"

    # OA
    if oa > config["oa_max"]:
        return False, f"OA cannot exceed {config['oa_max']}"

    # OB
    if ob > config["ob_max"]:
        return False, f"OB cannot exceed {config['ob_max']}"

    # OC
    if oc > config["oc_max"]:
        return False, f"OC cannot exceed {config['oc_max']}"

    # Passenger distribution
    if oa + ob + oc != passengers:
        return False, "Passenger distribution is incorrect."

    # Fuel sanity check (only if fuel values are provided)
    if takeoff_fuel is not None and trip_fuel is not None:
        if trip_fuel > takeoff_fuel:
            return False, "Trip fuel cannot exceed takeoff fuel."

    return True, "OK"