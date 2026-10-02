import streamlit as st
from pathlib import Path
from datetime import date

from aircraft import AIRCRAFT
from calculations import calculate_results
from validation import validate_inputs


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="B737-228 Weight & Balance",
    page_icon="✈️",
    layout="wide"
)


# ==========================================
# LOAD CUSTOM CSS
# ==========================================

css_file = Path(__file__).resolve().parent / "style.css"

if css_file.exists():
    with open(css_file, "r", encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)
else:
    st.warning(f"style.css not found at {css_file} - running with default styling.")


# ==========================================
# SESSION STATE
# ==========================================

if "results" not in st.session_state:
    st.session_state.results = None


# ==========================================
# TOP BANNER
# ==========================================

st.markdown(
    f"""
    <div class="wb-topbar">
        <div class="wb-topbar-left">
            <div class="wb-plane-icon">✈️</div>
            <div>
                <div class="wb-title">Weight &amp; Balance</div>
                <div class="wb-subtitle">Boeing 737-228 · Load Sheet Calculator</div>
            </div>
        </div>
        <div class="wb-topbar-right">
            {date.today().strftime('%d %b %Y')}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# SIDEBAR — AIRCRAFT & FLIGHT INFO
# ==========================================

with st.sidebar:

    st.markdown(
        '<div class="wb-sidebar-brand">✈️ Flight Data</div>',
        unsafe_allow_html=True
    )

    flight_number = st.text_input("Flight Number", placeholder="e.g. AH1042")
    registration = st.text_input("Registration", placeholder="e.g. 7T-VJX")
    flight_date = st.date_input("Date", value=date.today())

    st.divider()

    st.markdown(
        '<div class="wb-sidebar-brand">🛩️ Aircraft Configuration</div>',
        unsafe_allow_html=True
    )

    config_name = st.selectbox(
        "Cabin Configuration",
        list(AIRCRAFT.keys())
    )

    config = AIRCRAFT[config_name]

    st.caption(
        f"DOW: {config['dow']:,} kg  ·  IDOW: {config['idow']}\n\n"
        f"Max PAX: {config['max_pax']}"
    )


# ==========================================
# TABS
# ==========================================

tab_input, tab_results = st.tabs(["📝  Loading Data", "📊  Results"])


# ==========================================
# TAB 1 — LOADING DATA
# ==========================================

with tab_input:

    # ---------- Passengers ----------

    st.markdown(
        """
        <div class="wb-card">
            <div class="wb-section-title">👥 Passenger Distribution</div>
        """,
        unsafe_allow_html=True
    )

    total_passengers = st.number_input(
        "Total Passengers",
        min_value=0,
        max_value=config["max_pax"],
        value=min(95, config["max_pax"]),
        step=1
    )

    st.info(
        f"Zone A max: {config['oa_max']}  |  "
        f"Zone B max: {config['ob_max']}  |  "
        f"Zone C max: {config['oc_max']}  |  "
        f"Total max: {config['max_pax']}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        oa = st.number_input(
            "Zone A", min_value=0, max_value=config["oa_max"],
            value=min(23, config["oa_max"]), step=1
        )

    with col2:
        ob = st.number_input(
            "Zone B", min_value=0, max_value=config["ob_max"],
            value=min(48, config["ob_max"]), step=1
        )

    with col3:
        oc = st.number_input(
            "Zone C", min_value=0, max_value=config["oc_max"],
            value=min(24, config["oc_max"]), step=1
        )

    passenger_sum = oa + ob + oc
    st.caption(f"Zones entered: **{passenger_sum} / {total_passengers}**")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Cargo ----------

    st.markdown(
        """
        <div class="wb-card">
            <div class="wb-section-title">📦 Cargo</div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        cargo1 = st.number_input(
            "Cargo Compartment 1 (kg)", min_value=0.0, value=2180.0, step=1.0
        )

    with col2:
        cargo4 = st.number_input(
            "Cargo Compartment 4 (kg)", min_value=0.0, value=700.0, step=1.0
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Fuel ----------

    st.markdown(
        """
        <div class="wb-card">
            <div class="wb-section-title">⛽ Fuel</div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        takeoff_fuel = st.number_input(
            "Takeoff Fuel (kg)", min_value=0.0, value=14000.0, step=100.0
        )

    with col2:
        trip_fuel = st.number_input(
            "Trip Fuel (kg)", min_value=0.0, value=5000.0, step=100.0
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- Calculate ----------

    calculate_clicked = st.button("✈️  Calculate Weight & Balance", type="primary")

    if calculate_clicked:

        is_valid, message = validate_inputs(
            config, total_passengers, oa, ob, oc, takeoff_fuel, trip_fuel
        )

        if not is_valid:
            st.error(f"❌ {message}")
            st.session_state.results = None

        else:
            st.session_state.results = calculate_results(
                config, total_passengers, oa, ob, oc,
                cargo1, cargo4, takeoff_fuel, trip_fuel
            )
            st.success("Calculation complete — see the Results tab. ✓")


# ==========================================
# TAB 2 — RESULTS
# ==========================================

with tab_results:

    results = st.session_state.results

    if results is None:

        st.markdown(
            """
            <div class="wb-empty-state">
                <span class="wb-empty-icon">📊</span>
                No results yet. Fill in the Loading Data tab and press
                <strong>Calculate Weight &amp; Balance</strong>.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="wb-card">
                <div class="wb-section-title">Flight Summary</div>
                Flight <strong>{flight_number or '—'}</strong>
                &nbsp;·&nbsp; Reg. <strong>{registration or '—'}</strong>
                &nbsp;·&nbsp; {flight_date.strftime('%d %b %Y')}
                &nbsp;·&nbsp; {config_name}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="wb-section-title">Weights &amp; Center of Gravity</div>',
            unsafe_allow_html=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Zero Fuel Weight", f"{results['ZFW']:,.1f} kg")
            st.metric("CG ZFW", f"{results['CG_ZFW']:.2f} % MAC")

        with col2:
            st.metric("Takeoff Weight", f"{results['TOW']:,.1f} kg")
            st.metric("CG TOW", f"{results['CG_TOW']:.2f} % MAC")

        with col3:
            st.metric("Landing Weight", f"{results['Landing']:,.1f} kg")
            st.metric("CG Landing", f"{results['CG_LDG']:.2f} % MAC")

        with st.expander("Index Details"):
            st.markdown(
                f"""
                | Value | Result |
                |---|---|
                | Passenger Mass | {results['Passenger_Mass']} kg |
                | IZF (Index Zero Fuel) | {results['IZF']} |
                | ITOW (Index Takeoff) | {results['ITOW']} |
                | ILW (Index Landing) | {results['ILW']} |
                """
            )