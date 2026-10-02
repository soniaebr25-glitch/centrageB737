# calculations.py

from fuel import get_fuel_index


def calculate_results(config,
                       passengers,
                       oa,
                       ob,
                       oc,
                       cargo1,
                       cargo4,
                       tof,
                       tf):

    # -----------------------------
    # AIRCRAFT DATA
    # -----------------------------
    dow = config["dow"]
    idow = config["idow"]

    # -----------------------------
    # PASSENGER MASSES
    # NOTE: confirm 84 kg is the standard mass value your ops manual
    # requires (some carriers use different standard/average masses).
    # -----------------------------
    mass_pax = passengers * 84

    # -----------------------------
    # ZERO FUEL WEIGHT
    # -----------------------------
    zfw = dow + mass_pax + cargo1 + cargo4

    # -----------------------------
    # VARIATION INDICES
    # NOTE: coefficients below (-8.11, 8.38, -10.38, 10.13) and the
    # /10 vs /1000 scaling must match your loading manual's index
    # tables exactly. ob_index is hardcoded to 0 because Zone B's
    # arm is assumed to coincide with the reference station used to
    # define idow -- confirm this is actually true for your aircraft,
    # otherwise Zone B is missing an index contribution.
    # -----------------------------
    oa_index = oa * (-8.11) / 10
    ob_index = 0
    oc_index = oc * (8.38) / 10

    cargo1_index = cargo1 * (-10.38) / 1000
    cargo4_index = cargo4 * (10.13) / 1000

    # -----------------------------
    # INDEX ZFW
    # -----------------------------
    izf = (
        idow
        + oa_index
        + ob_index
        + oc_index
        + cargo1_index
        + cargo4_index
    )

    # -----------------------------
    # FUEL INDICES
    # NOTE: itf is computed by feeding trip fuel through the same
    # curve as total fuel on board. This subtraction method
    # (itow - itf) is only valid if your fuel index chart was
    # specifically built for that purpose (as some Boeing charts
    # are). Confirm against your manual -- otherwise landing index
    # should be computed directly from the remaining fuel quantity:
    # get_fuel_index(tof - tf).
    # -----------------------------
    itof = get_fuel_index(tof)
    itf = get_fuel_index(tf)

    # -----------------------------
    # TAKEOFF WEIGHT / INDEX
    # -----------------------------
    tow = zfw + tof
    itow = izf + itof

    # -----------------------------
    # LANDING WEIGHT / INDEX
    # -----------------------------
    lw = tow - tf
    ilw = itow - itf

    # -----------------------------
    # CG FUNCTION
    # NOTE: constants 508, 25, 16.256, 15.8902, 3.4163 must match
    # your reduction factor (K), reference index, LEMAC and MAC
    # length. Confirm these against the B737-200 W&B manual.
    # -----------------------------
    def cg(weight, index):
        return (
            (100 / 3.4163)
            * (
                508 * ((index - 25) / weight)
                + 16.256
                - 15.8902
            )
        )

    cg_zfw = cg(zfw, izf)
    cg_tow = cg(tow, itow)
    cg_lw = cg(lw, ilw)

    # -----------------------------
    # RETURN RESULTS
    # Keys match what app.py expects (no spaces, consistent naming)
    # -----------------------------
    return {
        "Passenger_Mass": round(mass_pax, 1),
        "ZFW": round(zfw, 1),
        "IZF": round(izf, 2),
        "TOW": round(tow, 1),
        "ITOW": round(itow, 2),
        "Landing": round(lw, 1),
        "ILW": round(ilw, 2),
        "CG_ZFW": round(cg_zfw, 2),
        "CG_TOW": round(cg_tow, 2),
        "CG_LDG": round(cg_lw, 2)
    }