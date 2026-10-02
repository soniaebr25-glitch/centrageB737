from openpyxl import load_workbook


def calculate_loading(
    cargo1,
    cargo4,
    oa,
    ob,
    oc,
    takeoff_fuel,
    trip_fuel
):

    # Open workbook
    workbook = load_workbook("centrage.xlsx")

    sheet = workbook["Feuil1"]     # We'll verify the sheet name later

    # -----------------------------
    # WRITE USER INPUTS
    # -----------------------------

    sheet["B5"] = cargo1
    sheet["B6"] = cargo4

    sheet["B7"] = oa
    sheet["B8"] = ob
    sheet["B9"] = oc

    sheet["D13"] = takeoff_fuel
    sheet["D14"] = trip_fuel

    # Save workbook
    workbook.save("centrage.xlsx")

    # Reopen workbook to read results
    workbook = load_workbook(
        "centrage.xlsx",
        data_only=True
    )

    sheet = workbook["Feuil1"]

    # -----------------------------
    # READ RESULTS
    # -----------------------------

    results = {

        "ZFW": sheet["B13"].value,

        "TOW": sheet["H13"].value,

        "Landing": sheet["H14"].value,

        "CG_ZFW": sheet["F17"].value,

        "CG_TOW": sheet["F18"].value,

        "CG_LDG": sheet["F19"].value

    }

    return results