import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="EV Engineering Classroom Simulator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for crisp, high-contrast educational UI
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .lecture-badge {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .metric-card {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 12px 16px;
        text-align: center;
    }
    .takeaway-box {
        background-color: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 12px 16px;
        border-radius: 4px;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION & VEHICLE PRESETS
# ==========================================
st.sidebar.image("https://github.com/rohanAB111/sakec-ev-simulator/blob/main/ShahAnchor-logo-v1.png", width=70)
st.sidebar.title("EV Course Navigator")
st.sidebar.caption("First-Year Engineering Interactive Learning Platform")

lecture_options = [
    "📌 Course Overview & EV Architecture",
    "1️⃣ Lecture 1: Vehicle Dynamics & Tractive Force",
    "2️⃣ Lecture 2: Electric Traction Motors & Drives",
    "3️⃣ Lecture 3: Battery Chemistries & Range Sizing",
    "4️⃣ Lecture 4: Regenerative Braking & Energy Flow",
    "5️⃣ Lecture 5: EV Charging Infrastructure & CC-CV",
    "6️⃣ Lecture 6: Well-to-Wheel (WTW) Decarbonization",
    "7️⃣ Lecture 7: Total Cost of Ownership (TCO)",
    "📝 Lecture 8: Classroom Interactive Concept Check"
]

selected_lecture = st.sidebar.selectbox("Select Lecture Module:", lecture_options)

st.sidebar.markdown("---")
st.sidebar.subheader("Classroom Preset Vehicles")
preset_choice = st.sidebar.radio(
    "Load Reference EV Data:",
    ["Custom Configuration", "Tata Nexon EV (Compact SUV)", "Ather 450X (Electric 2W)", "Olectra e-Bus (Commercial Transit)"]
)

# Standardized parameters based on selection
if preset_choice == "Tata Nexon EV (Compact SUV)":
    default_mass = 1550
    default_cd = 0.33
    default_area = 2.42
    default_crr = 0.011
    default_batt = 40.5
    default_motor_p = 105.0
    default_motor_t = 245.0
    default_voltage = 320.0
elif preset_choice == "Ather 450X (Electric 2W)":
    default_mass = 190
    default_cd = 0.70
    default_area = 0.65
    default_crr = 0.016
    default_batt = 3.7
    default_motor_p = 6.0
    default_motor_t = 26.0
    default_voltage = 51.1
elif preset_choice == "Olectra e-Bus (Commercial Transit)":
    default_mass = 14000
    default_cd = 0.65
    default_area = 7.50
    default_crr = 0.012
    default_batt = 250.0
    default_motor_p = 250.0
    default_motor_t = 1200.0
    default_voltage = 600.0
else:
    default_mass = 1400
    default_cd = 0.32
    default_area = 2.20
    default_crr = 0.012
    default_batt = 35.0
    default_motor_p = 90.0
    default_motor_t = 200.0
    default_voltage = 300.0

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip for Instructors:** Project this platform on the classroom screen while students adjust parameters on their own smartphones or laptops to explore physical trade-offs in real time.")


# ==========================================
# MODULE 0: OVERVIEW & ARCHITECTURE
# ==========================================
if selected_lecture == "📌 Course Overview & EV Architecture":
    st.markdown('<div class="lecture-badge">MODULE 0</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Introduction to Electric Vehicle Systems</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Understanding EV Taxonomy, Powertrain Topologies, and Component Interconnections</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.subheader("1. Vehicle Powertrain Comparison")
        st.markdown("""
        Vehicles are classified by their degree of electrification and energy conversion pathways:
        * **ICE (Internal Combustion Engine):** 100% fossil fuel reliant. Tank-to-wheel thermal efficiency is typically low ($pprox 18-24\%$).
        * **HEV (Hybrid Electric Vehicle):** Combines an ICE engine with an auxiliary electric motor and small battery ($\sim 1-2	ext{ kWh}$). Charges strictly via regenerative braking and engine generation; cannot be plugged in.
        * **PHEV (Plug-in Hybrid):** Features a moderate battery pack ($\sim 10-18	ext{ kWh}$) capable of pure electric range for 40–70 km, with an ICE backup for long journeys.
        * **BEV (Battery Electric Vehicle):** Pure zero-emission electric powertrain. High battery capacity ($\sim 30-100+	ext{ kWh}$), electric traction motor, bi-directional inverter, and high-efficiency single-speed reduction transmission.
        * **FCEV (Fuel Cell Electric Vehicle):** Hydrogen gas compressed at 700 bar feeds a proton-exchange membrane (PEM) fuel cell to generate electricity for an electric motor, with pure water vapor as exhaust.
        """)

    with col2:
        st.subheader("2. Core High-Voltage EV Components")
        st.markdown("""
        Every BEV integrates key subsystems:
        1. **Traction Battery Pack:** High-voltage DC source ($48	ext{V} - 800	ext{V}$).
        2. **Power Electronic Inverter (PEU):** Converts DC from the battery to variable-frequency 3-phase AC for the motor.
        3. **Electric Traction Motor:** Converts electrical energy to mechanical wheel torque.
        4. **Single-Speed Reduction Gearbox:** High-efficiency gear reduction ($8:1$ to $10:1$) with differential.
        5. **DC-DC Converter:** Steps down High Voltage ($300	ext{V}+$) to Low Voltage ($12	ext{V}$) for headlights, wipers, and ECUs.
        6. **On-Board Charger (OBC):** Converts external AC grid power to DC to charge the pack.
        7. **Thermal Management System:** Active coolant loops maintaining cell temperatures between $20^\circ	ext{C} - 35^\circ	ext{C}$.
        """)

    st.subheader("3. Component Efficiency Cascade")
    cols = st.columns(5)
    cols[0].metric("Grid to Charger", "90%", "OBC Conversion")
    cols[1].metric("Battery Roundtrip", "92%", "Chemical-Electrical")
    cols[2].metric("Inverter Efficiency", "96%", "DC-to-AC Inversion")
    cols[3].metric("Traction Motor", "94%", "Electromechanical")
    cols[4].metric("Driveline / Gearbox", "97%", "Mechanical Mesh")

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> While a traditional petrol engine wastes over 75% of fuel energy as heat, an Electric Vehicle achieves an end-to-end tank-to-wheel efficiency of <b>75% to 82%</b>.</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 1: VEHICLE LONGITUDINAL DYNAMICS
# ==========================================
elif selected_lecture == "1️⃣ Lecture 1: Vehicle Dynamics & Tractive Force":
    st.markdown('<div class="lecture-badge">LECTURE 1</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Vehicle Dynamics & Tractive Effort Sizing</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Newtonian Mechanics Applied to Vehicle Motion & Motor Sizing</div>', unsafe_allow_html=True)

    st.latex(r"F_{	ext{te}} = F_{	ext{rr}} + F_{	ext{ad}} + F_{	ext{hc}} + F_{	ext{acc}}")

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Vehicle & Road Parameters")
        m = st.slider("Vehicle Total Mass ($m$ in kg):", 100, 18000, int(default_mass), step=50)
        v_kmh = st.slider("Cruising Speed ($v$ in km/h):", 0, 160, 60, step=5)
        grade_pct = st.slider("Road Incline / Grade (%):", 0.0, 20.0, 0.0, step=0.5)
        accel = st.slider("Linear Acceleration ($a$ in $\text{m/s}^2$):", 0.0, 3.5, 0.0, step=0.1)
        cd = st.slider("Aerodynamic Drag Coeff ($C_d$):", 0.20, 0.85, float(default_cd), step=0.01)
        af = st.slider("Frontal Area ($A_f$ in $\text{m}^2$):", 0.5, 8.0, float(default_area), step=0.1)
        crr = st.slider("Rolling Resistance Coeff ($C_{rr}$):", 0.008, 0.025, float(default_crr), step=0.001)
        eta_trans = st.slider("Transmission Efficiency ($\eta$):", 0.80, 0.98, 0.95, step=0.01)

    # Calculations
    v = v_kmh / 3.6  # m/s
    theta = np.arctan(grade_pct / 100.0)
    g = 9.81
    rho_air = 1.18  # kg/m^3

    f_rr = crr * m * g * np.cos(theta)
    f_ad = 0.5 * rho_air * cd * af * (v ** 2)
    f_hc = m * g * np.sin(theta)
    delta = 0.05  # Rotational mass factor
    f_acc = m * accel * (1 + delta)
    f_te = f_rr + f_ad + f_hc + f_acc

    p_wheel_kw = (f_te * v) / 1000.0
    p_motor_kw = p_wheel_kw / eta_trans if p_wheel_kw > 0 else 0.0

    with c2:
        st.subheader("Instantaneous Forces & Power Demand")
        m_cols = st.columns(4)
        m_cols[0].metric("Rolling Resistance ($F_{rr}$)", f"{f_rr:.1f} N")
        m_cols[1].metric("Aero Drag ($F_{ad}$)", f"{f_ad:.1f} N")
        m_cols[2].metric("Hill Climb ($F_{hc}$)", f"{f_hc:.1f} N")
        m_cols[3].metric("Acceleration ($F_{acc}$)", f"{f_acc:.1f} N")

        st.markdown(f"### Total Tractive Force: **{f_te:.1f} N** | Motor Power Required: **{p_motor_kw:.2f} kW**")

        # Dynamic plot across speed range (0 to 140 km/h)
        v_range_kmh = np.linspace(0.1, 140, 100)
        v_range = v_range_kmh / 3.6
        frr_arr = np.full_like(v_range, crr * m * g * np.cos(theta))
        fad_arr = 0.5 * rho_air * cd * af * (v_range ** 2)
        fhc_arr = np.full_like(v_range, m * g * np.sin(theta))
        fte_steady = frr_arr + fad_arr + fhc_arr
        p_motor_arr = (fte_steady * v_range) / (1000.0 * eta_trans)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(v_range_kmh, frr_arr, label=r"$F_{rr}$ (Rolling)", color="green", linestyle="--")
        ax1.plot(v_range_kmh, fad_arr, label=r"$F_{ad}$ (Aero Drag)", color="red")
        ax1.plot(v_range_kmh, fte_steady, label=r"$F_{te}$ (Total Steady)", color="blue", linewidth=2)
        ax1.axvline(v_kmh, color="black", linestyle=":", label=f"Selected ({v_kmh} km/h)")
        ax1.set_xlabel("Speed (km/h)")
        ax1.set_ylabel("Force (N)")
        ax1.set_title("Resistive Forces vs Speed")
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        ax2.plot(v_range_kmh, p_motor_arr, color="purple", linewidth=2)
        ax2.axvline(v_kmh, color="black", linestyle=":")
        ax2.axhline(p_motor_kw, color="purple", linestyle=":")
        ax2.set_xlabel("Speed (km/h)")
        ax2.set_ylabel("Motor Power (kW)")
        ax2.set_title("Cruising Motor Power Demand (kW)")
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> Notice how aerodynamic drag increases with $v^2$, meaning motor power demand increases with $v^3$. At city speeds (&lt; 45 km/h), rolling resistance and vehicle weight dominate. At highway speeds (&gt; 80 km/h), aerodynamic drag consumes over 60% of total energy.</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 2: ELECTRIC MOTORS & DRIVES
# ==========================================
elif selected_lecture == "2️⃣ Lecture 2: Electric Traction Motors & Drives":
    st.markdown('<div class="lecture-badge">LECTURE 2</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Electric Traction Motors & Torque-Speed Curves</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Constant Torque vs. Field-Weakening Constant Power Regimes</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Traction Motor Parameters")
        motor_type = st.selectbox("Motor Topology:", ["PMSM (Permanent Magnet Synchronous)", "BLDC (Brushless DC)", "Induction Motor (IM)"])
        p_rated_kw = st.slider("Rated Motor Power ($P_{\text{rated}}$ in kW):", 5.0, 300.0, float(default_motor_p), step=5.0)
        t_max_nm = st.slider("Peak Stall Torque ($T_{\text{max}}$ in Nm):", 20.0, 600.0, float(default_motor_t), step=10.0)
        n_base = st.slider("Base Speed ($N_b$ in RPM):", 1000, 6000, 3500, step=250)
        n_max = st.slider("Maximum Speed ($N_{\text{max}}$ in RPM):", 6000, 16000, 11000, step=500)
        gear_ratio = st.slider("Single-Speed Gear Reduction ($G_r$):", 4.0, 12.0, 9.0, step=0.2)
        wheel_radius_m = st.slider("Tire Rolling Radius ($r_w$ in m):", 0.20, 0.45, 0.315, step=0.01)

    # Torque curve generation
    rpm_arr = np.linspace(0, n_max, 300)
    torque_arr = np.zeros_like(rpm_arr)
    power_arr = np.zeros_like(rpm_arr)

    for i, rpm in enumerate(rpm_arr):
        if rpm <= n_base:
            torque_arr[i] = t_max_nm
            omega = (2 * np.pi * rpm) / 60.0
            power_arr[i] = (torque_arr[i] * omega) / 1000.0
        else:
            omega = (2 * np.pi * rpm) / 60.0
            # Constant power region
            p_val = p_rated_kw
            power_arr[i] = p_val
            torque_arr[i] = (p_val * 1000.0) / omega

    # Wheel parameters
    max_wheel_speed_kmh = (n_max / gear_ratio) * (2 * np.pi * wheel_radius_m) * 3.6 / 60.0
    wheel_torque_peak = t_max_nm * gear_ratio * 0.95

    with c2:
        st.subheader("Motor Torque-Speed Envelope")
        m1, m2, m3 = st.columns(3)
        m1.metric("Peak Wheel Torque", f"{wheel_torque_peak:.1f} Nm", "At Wheel Hub")
        m2.metric("Base Speed Wheel Velocity", f"{(n_base / gear_ratio) * (2 * np.pi * wheel_radius_m) * 3.6 / 60.0:.1f} km/h", "End of Const Torque")
        m3.metric("Top Speed Limit", f"{max_wheel_speed_kmh:.1f} km/h", f"At {n_max} RPM")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(rpm_arr, torque_arr, color="crimson", linewidth=2.5)
        ax1.axvline(n_base, color="gray", linestyle="--", label=f"Base Speed ({n_base} RPM)")
        ax1.fill_between(rpm_arr[rpm_arr <= n_base], torque_arr[rpm_arr <= n_base], color="mistyrose", alpha=0.6, label="Constant Torque Region")
        ax1.fill_between(rpm_arr[rpm_arr > n_base], torque_arr[rpm_arr > n_base], color="lavender", alpha=0.6, label="Field Weakening Region")
        ax1.set_xlabel("Rotor Speed (RPM)")
        ax1.set_ylabel("Torque (Nm)")
        ax1.set_title("Motor Shaft Torque Characteristic")
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc="upper right", fontsize=8)

        ax2.plot(rpm_arr, power_arr, color="teal", linewidth=2.5)
        ax2.axvline(n_base, color="gray", linestyle="--")
        ax2.set_xlabel("Rotor Speed (RPM)")
        ax2.set_ylabel("Mechanical Power (kW)")
        ax2.set_title("Motor Power Output Characteristic")
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig)

    st.markdown("""
    #### Technology Comparison for Classroom Discussion:
    * **PMSM (Permanent Magnet Synchronous):** Highest efficiency (95-97%) and power density. Preferred in modern electric cars (Tata Nexon, MG ZS, Tesla Model 3).
    * **BLDC (Brushless DC):** Cost-effective, trapezoidal back-EMF, simple control. Widely utilized in 2-wheelers, 3-wheelers, and e-rickshaws across India.
    * **Induction Motor (IM):** Rugged, low-cost rotor without rare-earth neodymium magnets; excellent high-speed field weakening behavior (used in Tata Tigor EV commercial fleets, older Tesla Model S).
    """)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> Unlike an internal combustion engine that produces zero torque at 0 RPM and requires a clutch and 5-6 gears, an electric traction motor produces <b>maximum torque right from stall</b> (0 RPM). This enables rapid off-the-line acceleration with a single fixed reduction ratio!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 3: BATTERY CHEMISTRIES & SIZING
# ==========================================
elif selected_lecture == "3️⃣ Lecture 3: Battery Chemistries & Range Sizing":
    st.markdown('<div class="lecture-badge">LECTURE 3</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Battery Pack Sizing & Range Estimation</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Cell Chemistries, S-P Combinations, and Energy Consumption (Wh/km)</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Cell & Pack Design Controls")
        chemistry = st.selectbox(
            "Lithium-ion Chemistry:",
            ["LFP (Lithium Iron Phosphate - LiFePO4)", "NMC (Nickel Manganese Cobalt)", "Lead-Acid (Legacy Baseline)"]
        )

        if "LFP" in chemistry:
            v_cell_nom = 3.2
            cell_density_wh_kg = 150.0
            cycle_life = 3000
            chem_color = "green"
        elif "NMC" in chemistry:
            v_cell_nom = 3.7
            cell_density_wh_kg = 230.0
            cycle_life = 1200
            chem_color = "royalblue"
        else:
            v_cell_nom = 2.0
            cell_density_wh_kg = 35.0
            cycle_life = 400
            chem_color = "dimgray"

        target_energy_kwh = st.slider("Target Pack Capacity ($E_{\text{pack}}$ in kWh):", 2.0, 120.0, float(default_batt), step=1.0)
        dod_pct = st.slider("Usable Depth of Discharge (DoD %):", 70, 95, 85, step=1)
        ac_hvac = st.radio("Cabin Climate Control (HVAC):", ["Off", "Eco Mode (+10% load)", "Max Cooling (+25% load)"])
        avg_speed = st.slider("Average Driving Speed (km/h):", 30, 110, 50, step=5)

    # Calculations
    hvac_factor = 1.0 if ac_hvac == "Off" else (1.10 if "Eco" in ac_hvac else 1.25)
    # Empirical Wh/km model based on mass and speed
    base_wh_km = (0.05 * default_mass) + (0.007 * (avg_speed ** 1.7))
    total_wh_km = base_wh_km * hvac_factor

    usable_kwh = target_energy_kwh * (dod_pct / 100.0)
    est_range_km = (usable_kwh * 1000.0) / total_wh_km
    est_pack_weight_kg = (target_energy_kwh * 1000.0) / cell_density_wh_kg * 1.35  # incl packaging & BMS

    with c2:
        st.subheader("Pack Specifications & Driving Range")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Nominal Cell Volts", f"{v_cell_nom} V", chemistry.split()[0])
        k2.metric("Estimated Pack Mass", f"{est_pack_weight_kg:.0f} kg", f"{cell_density_wh_kg:.0f} Wh/kg cell")
        k3.metric("Consumption Rate", f"{total_wh_km:.1f} Wh/km", f"{ac_hvac}")
        k4.metric("Estimated Range", f"{est_range_km:.1f} km", f"{dod_pct}% DoD")

        # Range vs Speed Plot
        speeds = np.linspace(20, 120, 50)
        wh_km_arr = ((0.05 * default_mass) + (0.007 * (speeds ** 1.7))) * hvac_factor
        ranges_arr = (usable_kwh * 1000.0) / wh_km_arr

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.plot(speeds, ranges_arr, color=chem_color, linewidth=2.5)
        ax1.scatter([avg_speed], [est_range_km], color="red", s=60, zorder=5, label=f"Current: {est_range_km:.0f} km")
        ax1.set_xlabel("Average Speed (km/h)")
        ax1.set_ylabel("Realistic Range (km)")
        ax1.set_title("Driving Range vs. Speed")
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # Chemistry bar chart comparison
        chem_labels = ["LFP", "NMC", "Lead-Acid"]
        densities = [150, 230, 35]
        cycles = [3000, 1200, 400]
        ax2.bar(chem_labels, densities, color=["green", "royalblue", "dimgray"], alpha=0.7)
        ax2.set_ylabel("Specific Energy (Wh/kg)")
        ax2.set_title("Chemistry Energy Density Comparison")
        ax2.grid(True, alpha=0.3)

        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> LFP is dominant in Indian electric cars because of its superior <b>thermal stability</b> (runaway onset &gt; 270°C vs 210°C for NMC) and longer cycle life (3000+ charges), even though NMC offers higher energy density. Notice also the "Weight Spiral": adding battery capacity makes the car heavier, progressively reducing incremental range gains!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 4: REGENERATIVE BRAKING
# ==========================================
elif selected_lecture == "4️⃣ Lecture 4: Regenerative Braking & Energy Flow":
    st.markdown('<div class="lecture-badge">LECTURE 4</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Regenerative Braking & Energy Recovery</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Bi-Directional Power Flow and Brake Force Blending</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Braking Simulation Inputs")
        m_brake = st.slider("Vehicle Mass ($m$ in kg):", 150, 16000, int(default_mass), step=50)
        v_init_kmh = st.slider("Initial Velocity ($v_1$ in km/h):", 20, 120, 60, step=5)
        v_final_kmh = st.slider("Final Velocity ($v_2$ in km/h):", 0, 80, 0, step=5)
        decel_g = st.slider("Braking Deceleration ($g$ units):", 0.05, 0.80, 0.18, step=0.01)
        current_soc = st.slider("Battery State-of-Charge (SoC %):", 10, 100, 65, step=5)

    # Physics calculations
    v1 = v_init_kmh / 3.6
    v2 = v_final_kmh / 3.6
    ke_initial_kj = 0.5 * m_brake * (v1 ** 2) / 1000.0
    ke_dissipated_kj = 0.5 * m_brake * (v1 ** 2 - v2 ** 2) / 1000.0

    # Regen limit logic: if SoC > 95%, regen is throttled to prevent overcharge
    regen_throttle = 1.0 if current_soc < 90 else max(0.0, (98 - current_soc) / 8.0)
    # Fraction of regen vs friction based on deceleration rate
    if decel_g <= 0.20:
        f_regen_frac = 0.90 * regen_throttle
    elif decel_g <= 0.40:
        f_regen_frac = (0.90 - (decel_g - 0.20) * 2.0) * regen_throttle
    else:
        f_regen_frac = 0.25 * regen_throttle

    eta_regen_chain = 0.95 * 0.92 * 0.95 * 0.92  # trans * gen * inverter * batt = ~0.76
    recovered_kj = ke_dissipated_kj * f_regen_frac * eta_regen_chain
    recovered_wh = recovered_kj / 3.6
    friction_heat_kj = ke_dissipated_kj - recovered_kj

    with c2:
        st.subheader("Energy Breakdown from Braking Event")
        b1, b2, b3 = st.columns(3)
        b1.metric("Total Kinetic Energy", f"{ke_dissipated_kj:.1f} kJ", f"Initial: {ke_initial_kj:.1f} kJ")
        b2.metric("Energy Recovered", f"{recovered_wh:.2f} Wh", f"{f_regen_frac*100:.0f}% Regen Share")
        b3.metric("Friction Heat Loss", f"{friction_heat_kj:.1f} kJ", "Wasted on Rotors")

        if current_soc >= 95:
            st.warning("⚠️ **High Battery SoC Warning:** Regenerative braking is automatically throttled by the BMS to protect cells from over-voltage!")

        # Visual Pie Chart
        fig, ax = plt.subplots(figsize=(6, 3.5))
        labels = [f"Recovered into Battery ({recovered_kj:.1f} kJ)", f"Friction & Thermal Losses ({friction_heat_kj:.1f} kJ)"]
        colors = ["#10B981", "#EF4444"]
        ax.pie([recovered_kj, max(0.1, friction_heat_kj)], labels=labels, colors=colors, autopct="%1.1f%%", startangle=140)
        ax.set_title(f"Energy Distribution during Deceleration ({v_init_kmh} to {v_final_kmh} km/h)")
        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> In highway cruising, regen recovers only 5–8% of energy because braking is rare. In congested city traffic (like Mumbai), continuous stop-and-go driving recovers <b>15% to 25% of energy</b>, making electric vehicles uniquely more efficient in city traffic than on highways!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 5: EV CHARGING INFRASTRUCTURE & CC-CV
# ==========================================
elif selected_lecture == "5️⃣ Lecture 5: EV Charging Infrastructure & CC-CV":
    st.markdown('<div class="lecture-badge">LECTURE 5</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">EV Charging Dynamics & CC-CV Profiles</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">AC Level 1/2 vs DC Fast Charging, C-Rate, and the 80% Taper Curve</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Charging Configuration")
        charger_type = st.selectbox(
            "Charger Standard:",
            ["Standard 15A Home Socket (AC 3.3 kW)", "AC Wallbox (7.2 kW Type 2)", "Commercial AC Fast (22 kW)", "DC Fast Charger (50 kW CCS2)", "Ultra-Fast DC (120 kW CCS2)"]
        )
        pack_size = st.slider("Battery Capacity (kWh):", 3.0, 150.0, float(default_batt), step=1.0)
        soc_start = st.slider("Starting SoC (%):", 0, 80, 10, step=5)
        soc_target = st.slider("Target SoC (%):", soc_start + 10, 100, 100, step=5)

    if "3.3 kW" in charger_type:
        p_chg = 3.3
        is_dc = False
    elif "7.2 kW" in charger_type:
        p_chg = 7.2
        is_dc = False
    elif "22 kW" in charger_type:
        p_chg = 22.0
        is_dc = False
    elif "50 kW" in charger_type:
        p_chg = 50.0
        is_dc = True
    else:
        p_chg = 120.0
        is_dc = True

    # Simulation timeline for CC-CV
    soc_timeline = np.linspace(soc_start, soc_target, 100)
    power_profile = np.zeros_like(soc_timeline)
    for i, s in enumerate(soc_timeline):
        if s <= 80:
            power_profile[i] = p_chg  # Constant current / full power
        else:
            # Tapering during CV phase
            taper_factor = (100 - s) / 20.0
            power_profile[i] = max(p_chg * 0.20, p_chg * taper_factor)

    avg_p_cc = p_chg
    delta_soc_cc = max(0, min(80, soc_target) - min(80, soc_start)) / 100.0
    time_cc_hr = (delta_soc_cc * pack_size) / (avg_p_cc * 0.90)

    delta_soc_cv = max(0, soc_target - max(80, soc_start)) / 100.0
    avg_p_cv = p_chg * 0.50
    time_cv_hr = (delta_soc_cv * pack_size) / (avg_p_cv * 0.88) if delta_soc_cv > 0 else 0.0

    total_time_hr = time_cc_hr + time_cv_hr

    with c2:
        st.subheader("Charging Time & Power Profile")
        t1, t2, t3 = st.columns(3)
        t1.metric("Total Charging Time", f"{total_time_hr*60:.0f} mins", f"({total_time_hr:.2f} hrs)")
        t2.metric("CC Stage (to 80%)", f"{time_cc_hr*60:.0f} mins", "Max Power")
        t3.metric("CV Stage (80-100%)", f"{time_cv_hr*60:.0f} mins", "Taper Phase")

        fig, ax1 = plt.subplots(figsize=(8, 4))
        ax1.plot(soc_timeline, power_profile, color="crimson", linewidth=2.5, label="Charging Power (kW)")
        ax1.axvline(80, color="gray", linestyle="--", label="80% CC to CV Switch")
        ax1.set_xlabel("Battery State-of-Charge (SoC %)")
        ax1.set_ylabel("Delivered Power (kW)", color="crimson")
        ax1.set_title(f"CC-CV Charging Curve ({charger_type})")
        ax1.grid(True, alpha=0.3)
        ax1.legend(loc="upper right")
        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> Notice how charging power aggressively drops after 80% SoC in the Constant Voltage (CV) phase to prevent cell overheating and lithium plating. This explains why highway EV route planners advise charging only up to 80% at fast chargers before continuing your journey!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 6: WELL-TO-WHEEL (WTW) DECARBONIZATION
# ==========================================
elif selected_lecture == "6️⃣ Lecture 6: Well-to-Wheel (WTW) Decarbonization":
    st.markdown('<div class="lecture-badge">LECTURE 6</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Well-to-Wheel (WTW) Life-Cycle Emissions</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Debunking the "Dirty Grid" Fallacy: Indian Grid Baseline vs. Petrol/Diesel</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Emissions Parameters")
        ice_type = st.radio("Benchmark ICE Vehicle:", ["Petrol Compact SUV (14 km/L)", "Diesel Compact SUV (18 km/L)", "Petrol 2-Wheeler (48 km/L)"])
        ev_grid_intensity = st.slider("Grid Carbon Intensity ($g\text{ CO}_2/\text{kWh}$):", 0, 950, 710, step=25, help="710 g/kWh is the national average for the Indian Electricity Grid (CEA Baseline).")
        ev_consumption_wh_km = st.slider("EV Energy Consumption (Wh/km):", 30, 200, 135, step=5)

    if "Petrol Compact" in ice_type:
        ttw_ice = (2320.0 / 14.0)  # g/km
        wtt_ice = ttw_ice * 0.20
    elif "Diesel" in ice_type:
        ttw_ice = (2680.0 / 18.0)
        wtt_ice = ttw_ice * 0.22
    else:
        ttw_ice = (2320.0 / 48.0)
        wtt_ice = ttw_ice * 0.20

    wtw_ice = ttw_ice + wtt_ice

    # EV calculations
    # Account for 18% T&D loss on grid + 10% charger loss
    grid_effective_kwh = (ev_consumption_wh_km / 1000.0) / (0.82 * 0.90)
    wtw_ev = grid_effective_kwh * ev_grid_intensity
    pct_reduction = ((wtw_ice - wtw_ev) / wtw_ice) * 100.0

    with c2:
        st.subheader("CO2 Emissions Comparison")
        e1, e2, e3 = st.columns(3)
        e1.metric("ICE Emissions (WTW)", f"{wtw_ice:.1f} g/km", "Well-to-Wheel")
        e2.metric("EV Emissions (WTW)", f"{wtw_ev:.1f} g/km", f"{ev_grid_intensity} g CO2/kWh")
        e3.metric("Net CO2 Reduction", f"{pct_reduction:.1f}%", "Lower Emissions")

        # Bar comparison
        fig, ax = plt.subplots(figsize=(8, 4))
        categories = ["ICE Total (WTW)", "EV (Indian Grid 710 g)", "EV (Clean Solar 40 g)"]
        ev_solar = grid_effective_kwh * 40.0
        emissions_values = [wtw_ice, wtw_ev, ev_solar]
        bar_colors = ["#EF4444", "#3B82F6", "#10B981"]

        bars = ax.bar(categories, emissions_values, color=bar_colors, width=0.55)
        for bar in bars:
            yval = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2.0, yval + 3, f"{yval:.1f} g/km", ha='center', va='bottom', fontweight='bold')

        ax.set_ylabel(r"Total $	ext{CO}_2$ Emissions (g/km)")
        ax.set_title("Well-to-Wheel Life-Cycle Analysis")
        ax.grid(True, alpha=0.3, axis='y')
        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> Even when charged from India\'s coal-dominant national grid (710 g CO2/kWh), an EV emits <b>30% to 45% less CO2 per km</b> than a petrol vehicle. This is because large power plants and electric motors operate at ~40% and ~95% efficiencies, whereas car petrol engines operate at only ~20% in city traffic. When solar/renewable power is used, emissions drop by over 95%!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 7: TOTAL COST OF OWNERSHIP (TCO)
# ==========================================
elif selected_lecture == "7️⃣ Lecture 7: Total Cost of Ownership (TCO)":
    st.markdown('<div class="lecture-badge">LECTURE 7</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Total Cost of Ownership & Economic Break-Even</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Evaluating Capital Expenditure (CapEx) vs. Operating Expenditure (OpEx)</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 2])
    with c1:
        st.subheader("Cost & Usage Parameters")
        annual_km = st.slider("Annual Driving Distance (km/year):", 5000, 45000, 15000, step=1000)
        petrol_price = st.slider("Fuel Price (₹/Liter):", 90.0, 120.0, 104.0, step=1.0)
        ice_mileage = st.slider("ICE Mileage (km/Liter):", 8.0, 30.0, 14.0, step=1.0)
        electricity_tariff = st.slider("Electricity Tariff (₹/kWh):", 4.0, 15.0, 7.5, step=0.5)
        ev_wh_km = st.slider("EV Consumption (Wh/km):", 80, 220, 135, step=5)
        capex_diff = st.slider("Initial Purchase Price Gap (EV - ICE in ₹ Lakh):", 1.0, 8.0, 4.0, step=0.5) * 100000

    # Economics calculation
    fuel_cost_per_km_ice = petrol_price / ice_mileage
    maint_ice_per_km = 0.85
    total_ice_per_km = fuel_cost_per_km_ice + maint_ice_per_km

    ev_cost_per_km = (ev_wh_km / 1000.0) * electricity_tariff / 0.90  # incl charging loss
    maint_ev_per_km = 0.30
    total_ev_per_km = ev_cost_per_km + maint_ev_per_km

    savings_per_km = total_ice_per_km - total_ev_per_km
    breakeven_km = capex_diff / savings_per_km if savings_per_km > 0 else float('inf')
    payback_years = breakeven_km / annual_km

    with c2:
        st.subheader("Financial Comparison & Break-Even Point")
        f1, f2, f3 = st.columns(3)
        f1.metric("ICE Running Cost", f"₹{total_ice_per_km:.2f} / km", f"Fuel: ₹{fuel_cost_per_km_ice:.2f}")
        f2.metric("EV Running Cost", f"₹{total_ev_per_km:.2f} / km", f"Electricity: ₹{ev_cost_per_km:.2f}")
        f3.metric("Break-Even Distance", f"{breakeven_km:,.0f} km", f"≈ {payback_years:.1f} Years")

        # 10-year projection graph
        years = np.arange(0, 11)
        dist_cum = years * annual_km
        cost_ice_cum = dist_cum * total_ice_per_km
        cost_ev_cum = capex_diff + (dist_cum * total_ev_per_km)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(years, cost_ice_cum / 100000.0, label="ICE Cumulative Cost", color="crimson", linewidth=2)
        ax.plot(years, cost_ev_cum / 100000.0, label="EV Cumulative Cost (with initial premium)", color="teal", linewidth=2)
        if payback_years <= 10:
            ax.axvline(payback_years, color="black", linestyle="--", label=f"Break-Even: {payback_years:.1f} Yrs")
        ax.set_xlabel("Years of Ownership")
        ax.set_ylabel("Total Expenditure (₹ Lakhs)")
        ax.set_title("10-Year Total Cost of Ownership (CapEx + OpEx)")
        ax.grid(True, alpha=0.3)
        ax.legend()
        st.pyplot(fig)

    st.markdown('<div class="takeaway-box"><b>Key Pedagogical Takeaway:</b> Although an EV has a higher upfront initial purchase price (CapEx), its operating cost (OpEx) is roughly <b>75% lower</b> than a petrol car. For commercial fleet operators (like taxis or delivery services driving 150+ km/day), the break-even is achieved in less than 1.5 years!</div>', unsafe_allow_html=True)


# ==========================================
# MODULE 8: INTERACTIVE CLASSROOM QUIZ
# ==========================================
elif selected_lecture == "📝 Lecture 8: Classroom Interactive Concept Check":
    st.markdown('<div class="lecture-badge">LECTURE 8</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Interactive Classroom Concept Check</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Live Formative Assessment for First-Year Engineering Students</div>', unsafe_allow_html=True)

    st.info("Students: Answer the questions below during class to test your understanding of Electric Vehicle physics and engineering principles!")

    score = 0
    total_q = 5

    # Question 1
    st.markdown("### Question 1: Aerodynamic Power Scaling")
    q1 = st.radio(
        "If an electric vehicle doubles its cruising speed from 50 km/h to 100 km/h, by what factor does the aerodynamic power requirement increase?",
        ["2 times", "4 times", "8 times", "Remains unchanged"],
        key="q1"
    )
    if q1 == "8 times":
        st.success("✅ **Correct!** Aerodynamic drag force scales with $v^2$, so power ($P = F \cdot v$) scales with $v^3$. Doubling velocity increases power demand by $2^3 = 8$ times.")
        score += 1
    elif q1:
        st.error("❌ **Incorrect.** Recall that $F_{\text{ad}} \propto v^2$, and $P = F_{\text{ad}} \cdot v \propto v^3$.")

    st.markdown("---")

    # Question 2
    st.markdown("### Question 2: Electric Motor vs ICE Torque")
    q2 = st.radio(
        "Why can most Battery Electric Vehicles operate with a simple single-speed reduction gearbox instead of a multi-speed transmission?",
        [
            "Electric motors are smaller in physical size",
            "Electric motors deliver peak maximum torque right from 0 RPM (stall) up to base speed",
            "Batteries can only produce direct current",
            "Electric vehicles cannot drive faster than 100 km/h"
        ],
        key="q2"
    )
    if q2 == "Electric motors deliver peak maximum torque right from 0 RPM (stall) up to base speed":
        st.success("✅ **Correct!** Because electric traction motors provide maximum torque from stall and possess a broad constant power speed range, a single-speed gearbox is sufficient.")
        score += 1
    elif q2:
        st.error("❌ **Incorrect.** The key reason is the torque-speed profile: peak torque from zero RPM eliminates the need for clutch slip and multiple gears.")

    st.markdown("---")

    # Question 3
    st.markdown("### Question 3: Battery Thermal Stability in Indian Climate")
    q3 = st.radio(
        "Why is Lithium Iron Phosphate (LFP) chemistry widely favored over NMC for mass-market electric vehicles in India?",
        [
            "LFP has higher energy density than NMC",
            "LFP cells have a much higher thermal runaway threshold (>270°C) and superior cycle life",
            "LFP cells operate at 12 Volts per cell",
            "LFP does not require any Battery Management System (BMS)"
        ],
        key="q3"
    )
    if "higher thermal runaway threshold" in q3:
        st.success("✅ **Correct!** LFP offers exceptional thermal stability and long cycle life (2500-3000+ cycles), making it resilient to tropical ambient temperatures.")
        score += 1
    elif q3:
        st.error("❌ **Incorrect.** While NMC has higher energy density, LFP is preferred due to safety, higher thermal runaway onset, and cycle life.")

    st.markdown("---")

    # Question 4
    st.markdown("### Question 4: Regenerative Braking Limitations")
    q4 = st.radio(
        "Under which condition must the Battery Management System (BMS) disable or limit regenerative braking?",
        [
            "When vehicle speed is over 40 km/h",
            "When the battery is at 98%–100% State of Charge (SoC)",
            "When driving uphill",
            "When the headlights are turned on"
        ],
        key="q4"
    )
    if "98%–100% State of Charge" in q4:
        st.success("✅ **Correct!** When the battery is full, charging it further with high regenerative braking current will cause over-voltage and thermal stress.")
        score += 1
    elif q4:
        st.error("❌ **Incorrect.** At near 100% SoC, there is no chemical capacity to accept fast charge current safely.")

    st.markdown("---")

    # Question 5
    st.markdown("### Question 5: CC-CV Fast Charging Dynamics")
    q5 = st.radio(
        "Why does charging an EV battery from 80% to 100% SoC take disproportionately longer than from 20% to 40%?",
        [
            "The charger shuts down one phase of electricity",
            "The charging system switches to Constant Voltage (CV) mode, tapering current down to protect cells",
            "Electric grid voltage drops at night",
            "Battery internal resistance drops to zero"
        ],
        key="q5"
    )
    if "Constant Voltage (CV) mode, tapering current" in q5:
        st.success("✅ **Correct!** Above ~80% SoC, voltage is clamped at maximum threshold and current decays exponentially to avoid lithium plating.")
        score += 1
    elif q5:
        st.error("❌ **Incorrect.** In the CV phase, charging current is tapered down exponentially to safeguard battery longevity.")

    st.markdown("---")
    st.markdown(f"### 🏆 Live Classroom Score: **{score} / {total_q}** ({score/total_q*100:.0f}%)")
    if score == 5:
        st.balloons()
        st.success("Outstanding! You have mastered the core First-Year Electric Vehicle concepts!")

# Footer
st.markdown("---")
st.caption("Shah & Anchor Kutchhi Engineering College (SAKEC) — Department of Electronics & Telecommunication Engineering / Basic Electrical Engineering | Developed for Classroom Interactive Simulations")
