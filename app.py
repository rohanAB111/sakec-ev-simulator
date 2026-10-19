import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import time

from ev_quizzes import EV_MODULES_DATA
from ev_backend import (
    authenticate_user,
    add_user,
    reset_user_password,
    delete_user,
    bulk_upload_users_csv,
    load_users,
    complete_simulation,
    get_student_profile,
    get_all_students_progress,
    export_master_excel
)
import onedrive_sync

# ==========================================
# PAGE CONFIGURATION & INSTITUTIONAL THEME
# ==========================================
st.set_page_config(
    page_title="SAKEC EV Simulation & Learning Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SAKEC Custom Styling
st.markdown("""
<style>
    .inst-header {
        background: linear-gradient(135deg, #101426, #1c233d);
        border: 1px solid #2d375d;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .inst-title {
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: 0.8px;
        color: #F2B705;
        text-transform: uppercase;
        margin: 0;
    }
    .inst-sub {
        font-size: 0.85rem;
        color: #A0AEC0;
        margin: 4px 0 0;
    }
    .developer-tag {
        display: inline-block;
        background: rgba(242, 183, 5, 0.15);
        color: #F2B705;
        border: 1px solid rgba(242, 183, 5, 0.3);
        padding: 2px 10px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-top: 6px;
    }
    .main-title {
        font-size: 2.0rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .lecture-badge {
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .takeaway-box {
        background-color: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .reflection-box {
        background: #F8FAFC;
        border: 2px solid #E2E8F0;
        border-radius: 12px;
        padding: 20px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .quiz-card {
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }
    .pass-badge {
        background: #DCFCE7;
        color: #15803D;
        border: 1px solid #86EFAC;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .fail-badge {
        background: #FEF3C7;
        color: #B45309;
        border: 1px solid #FCD34D;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .footer {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        border-top: 1px solid #E2E8F0;
        padding-top: 18px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# Render Institutional Header
st.markdown("""
<div class="inst-header">
    <div class="inst-title">Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai</div>
    <div class="inst-sub">An Autonomous Institute Affiliated to University of Mumbai · NAAC 'A' Grade · Approved by AICTE</div>
    <div class="developer-tag">Electric Vehicle Simulation Platform · Developed by Dr. Rohan Borgalli</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# AUTHENTICATION & LOGIN MANAGEMENT
# ==========================================
SAKEC_DEPARTMENTS = [
    "Computer Engineering",
    "Information Technology",
    "Artificial Intelligence & Data Science",
    "Electronics & Computer Science",
    "Cyber Security",
    "Electronics & Telecommunication Engineering (EXTC)",
    "Humanities & Applied Sciences (First Year / FE)",
    "Electronics Engg (VLSI Design & Technology)",
    "Electronics & Comm (Adv Communication Technology)",
    "Master of Computer Applications (MCA)",
    "B.Voc Cyber Security",
    "B.Voc AI & Data Science",
    "Other Department"
]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

def render_login_screen():
    st.markdown('<div class="main-title">🔐 EV Simulator Portal Sign In</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Sign in to access interactive EV simulations, submit technical reflections, and record accredited learning outcomes.</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1.2, 1])
    with c1:
        st.markdown("#### Enter College Credentials")
        login_id = st.text_input("College Email ID or Roll Number *", placeholder="e.g. rahul.sharma@sakec.ac.in or 23AIDS102").strip()
        login_pass = st.text_input("Password *", type="password", placeholder="Enter your password").strip()

        st.caption("ℹ️ **Access Policy:** Only students and faculty enrolled by the administrator can access the platform. Default initial password is `firstname@123` (e.g. `rahul@123`). Contact the administrator if you need an account.")

        if st.button("🚀 Sign In to EV Simulator", type="primary", use_container_width=True):
            if not login_id or not login_pass:
                st.error("Please enter both Email/Roll Number and Password.")
            else:
                # Lookup by email or roll number
                users = load_users()
                target_email = login_id.lower()
                
                # Check if user entered roll number instead of email
                for em, u in users.items():
                    if u.get("roll", "").upper() == login_id.upper():
                        target_email = em
                        break
                
                auth_res = authenticate_user(target_email, login_pass)
                if auth_res["ok"]:
                    st.session_state.logged_in = True
                    st.session_state.user = auth_res["user"]
                    st.success(f"Welcome, {auth_res['user']['name']}! Loading simulation modules...")
                    st.rerun()
                else:
                    st.error(auth_res["error"])

        st.markdown("---")
        st.markdown("**Institutional Single Sign-On (SSO):**")
        st.caption("College Microsoft 365 accounts allow direct authentication and automated OneDrive report sync.")
        if st.button("🔑 Sign in with Microsoft 365 (@sakec.ac.in)", use_container_width=True):
            if onedrive_sync.is_configured():
                st.info("Redirecting to Microsoft Entra ID college login...")
            else:
                st.info("Microsoft 365 Note: Once SAKEC IT admin configures MICROSOFT_CLIENT_ID on Render, 1-click SSO will activate. In the meantime, sign in with your college credentials above.")

    with c2:
        st.info("""
        **🎓 Student Simulation Workflow:**
        1. **Sign In:** Use your college credentials enrolled by the administrator.
        2. **Run Simulations:** Test vehicle parameters (speed, mass, drag, motor, battery).
        3. **Reflect:** Submit your technical reflection explaining physical trade-offs.
        4. **Complete Simulation:** Click *'Simulation Completed'* to trigger the 5-Question Understanding Check.
        5. **Pass Requirement:** Must score **at least 3 out of 5 (>= 60%)** to earn completion credit. If you score < 3, you must re-run the simulation and retry.
        6. **Track Progress:** Observe your verified completion records in *'My Profile'*.
        """)

if not st.session_state.logged_in:
    render_login_screen()
    st.markdown('<div class="footer">Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai<br>Developed by <b>Dr. Rohan Borgalli</b></div>', unsafe_allow_html=True)
    st.stop()

# ==========================================
# SIDEBAR NAVIGATION & ROLE RESTRICTIONS
# ==========================================
user = st.session_state.user
is_admin = (user.get("role") == "admin")

user_badge = ("👨‍🎓 " + user["name"]) if user.get("role") == "student" else ("🛡️ " + user["name"] + " (Admin)")
dept_badge = user.get("roll", "Faculty") + " · " + user.get("dept", "SAKEC")

st.sidebar.markdown(f"""
<div style="background:#F1F5F9; border:1px solid #CBD5E1; border-radius:10px; padding:12px; margin-bottom:14px;">
    <div style="font-size:0.75rem; text-transform:uppercase; color:#64748B; font-weight:700;">Signed In Profile</div>
    <div style="font-size:0.95rem; font-weight:700; color:#1E293B;">{user_badge}</div>
    <div style="font-size:0.8rem; color:#475569;">{dept_badge}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("🚪 Sign Out", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.title("EV Module Navigator")

# Strictly filter navigation options by role
if user.get("role") == "student":
    # Students ONLY see simulations and their own profile
    lecture_options = [
        "1️⃣ Module 1: Vehicle Dynamics & Tractive Force",
        "2️⃣ Module 2: Electric Traction Motors & Drives",
        "3️⃣ Module 3: Battery Chemistries & Range Sizing",
        "4️⃣ Module 4: Regenerative Braking & Energy Flow",
        "5️⃣ Module 5: EV Charging Infrastructure & CC-CV",
        "6️⃣ Module 6: Well-to-Wheel (WTW) Decarbonization",
        "7️⃣ Module 7: Total Cost of Ownership (TCO)",
        "👤 My Learning Progress & Portfolio"
    ]
else:
    # Admin / Faculty sees all simulations, profile, and Admin Dashboard
    lecture_options = [
        "📌 Course Overview & EV Architecture",
        "1️⃣ Module 1: Vehicle Dynamics & Tractive Force",
        "2️⃣ Module 2: Electric Traction Motors & Drives",
        "3️⃣ Module 3: Battery Chemistries & Range Sizing",
        "4️⃣ Module 4: Regenerative Braking & Energy Flow",
        "5️⃣ Module 5: EV Charging Infrastructure & CC-CV",
        "6️⃣ Module 6: Well-to-Wheel (WTW) Decarbonization",
        "7️⃣ Module 7: Total Cost of Ownership (TCO)",
        "👤 My Learning Progress & Portfolio",
        "🛡️ Admin Dashboard & User Management"
    ]

selected_lecture = st.sidebar.selectbox("Select Learning Module:", lecture_options)

st.sidebar.markdown("---")
st.sidebar.subheader("Classroom Preset Vehicles")
preset_choice = st.sidebar.radio(
    "Load Reference EV Data:",
    ["Custom Configuration", "Tata Nexon EV (Compact SUV)", "Ather 450X (Electric 2W)", "Olectra e-Bus (Commercial Transit)"]
)

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


# ==========================================
# POST-SIMULATION REFLECTION & 5-QUESTION CHECK
# (Pass Threshold: >= 3/5 Correct Required)
# ==========================================
def render_post_simulation_block(module_key, module_title, tested_params):
    st.markdown('<div class="reflection-box">', unsafe_allow_html=True)
    st.markdown(f'<h3 style="color:#1E3A8A; margin-top:0;">📝 Simulation Completion &amp; Assessment: {module_title}</h3>', unsafe_allow_html=True)

    mod_data = EV_MODULES_DATA.get(module_key, {})
    prof = get_student_profile(user["email"]) or {}
    comp_data = prof.get("completed_modules", {}).get(module_key, {})
    is_already_completed = comp_data.get("completed", False)
    attempts = comp_data.get("attempts", 0)
    best_score = comp_data.get("best_score", comp_data.get("quiz_score", 0))

    if is_already_completed:
        st.markdown(f'<span class="pass-badge">✓ COMPLETED (Score: {best_score}/5 | {attempts} {"attempt" if attempts==1 else "attempts"})</span>', unsafe_allow_html=True)
        st.caption(f"Completed on {time.strftime('%d %b %Y, %I:%M %p', time.localtime(comp_data.get('last_attempt_at', time.time())))}. You can re-attempt below to improve your score.")
    elif attempts > 0:
        st.markdown(f'<span class="fail-badge">⚠️ NOT COMPLETED: RETRY REQUIRED (Last Score: {comp_data.get("quiz_score", 0)}/5 | {attempts} {"attempt" if attempts==1 else "attempts"})</span>', unsafe_allow_html=True)
        st.warning("You did not reach the minimum threshold of 3/5 correct answers on your previous attempt. Please re-run the simulation, observe parameter changes, and retry.")
    else:
        st.caption("Rule: You must test the simulation, enter your engineering reflection, and answer **at least 3 of 5 questions correctly (>= 60%)** to earn completion credit.")

    # 1. Technical Reflection
    st.markdown("#### 1. Engineering Reflection & Parameter Observation")
    st.info(f"**Guided Reflection Prompt:** {mod_data.get('reflection_prompt', 'Describe your engineering observations when varying vehicle parameters.')}")

    prev_ref = comp_data.get("reflection", "")
    reflection_text = st.text_area(
        "Enter your engineering reflection (explain observed trade-offs, curves, and physical reasoning):",
        value=prev_ref,
        height=130,
        placeholder="Explain how changing speed, weight, frontal area, or battery capacity affected tractive power demand and efficiency based on your simulation runs...",
        key=f"ref_text_{module_key}"
    )

    # Trigger to show 5 questions
    quiz_session_key = f"quiz_active_{module_key}"
    if quiz_session_key not in st.session_state:
        st.session_state[quiz_session_key] = False

    if not is_already_completed and not st.session_state[quiz_session_key]:
        if st.button("✅ Simulation Completed — Start 5-Question Understanding Check", type="primary", key=f"btn_complete_{module_key}"):
            if not reflection_text or len(reflection_text.strip()) < 20:
                st.error("Please provide a thorough technical reflection (at least 20 characters) before taking the assessment.")
            else:
                st.session_state[quiz_session_key] = True
                st.rerun()

    # 2. Render 5 Understanding Questions
    if is_already_completed or st.session_state.get(quiz_session_key, False):
        st.markdown("#### 2. Understanding Verification Check (5 Questions — Pass: 3/5)")
        questions = mod_data.get("questions", [])
        total_q = len(questions)
        user_choices = {}

        for q_idx, q in enumerate(questions):
            st.markdown(f'<div class="quiz-card"><b>Question {q_idx+1} of {total_q}:</b> {q["q"]}</div>', unsafe_allow_html=True)
            ans = st.radio(
                "Select your answer:",
                q["options"],
                key=f"quiz_opt_{module_key}_{q_idx}",
                label_visibility="collapsed"
            )
            user_choices[q_idx] = q["options"].index(ans)

        if st.button(f"Submit 5 Questions for Grading", type="primary", key=f"btn_grade_{module_key}"):
            if not reflection_text or len(reflection_text.strip()) < 20:
                st.error("Please enter your engineering reflection above before submitting.")
                return

            score = 0
            st.markdown("---")
            st.markdown("##### Detailed Assessment Feedback:")
            for q_idx, q in enumerate(questions):
                is_correct = (user_choices[q_idx] == q["correct"])
                if is_correct:
                    score += 1
                    st.success(f"**Q{q_idx+1} Correct:** {q['options'][q['correct']]} — {q['explain']}")
                else:
                    st.error(f"**Q{q_idx+1} Incorrect:** You chose '{q['options'][user_choices[q_idx]]}'. Correct Answer: **{q['options'][q['correct']]}**. — {q['explain']}")

            # Check Pass / Fail Condition (>= 3 of 5)
            passed = complete_simulation(
                user["email"], user["name"], user.get("roll", "—"),
                user.get("dept", "SAKEC"), user.get("division", ""),
                module_key, reflection_text, score, total_q, tested_params
            )

            if passed:
                st.balloons()
                st.success(f"🎉 **CONGRATULATIONS! You scored {score}/5 (PASSED).** This simulation is now permanently marked as **COMPLETED** in your official SAKEC student learning profile.")
            else:
                st.error(f"⚠️ **MINIMUM SCORE NOT MET:** You scored **{score}/5**. A minimum of 3 correct answers (60%) is required to earn completion credit. You must review the simulation curves, check the physics explanations above, and retry.")
                if st.button("🔄 Try Again", key=f"retry_{module_key}"):
                    st.session_state[quiz_session_key] = True
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

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


# ==========================================
# MODULE 8: INTERACTIVE CLASSROOM QUIZ
# ==========================================
elif selected_lecture == "📝 Lecture 8: Classroom Interactive Concept Check":
    st.markdown('<div class="lecture-badge">MODULE 8</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">Comprehensive EV Concept Check</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Test Your Mastery Across All 7 EV Physics & Engineering Modules</div>', unsafe_allow_html=True)

    score = 0
    q1 = st.radio("1. What component dominates power consumption at speeds >80 km/h?", ["Aerodynamic drag (scales with v³)", "Rolling resistance", "Tire pressure", "Cabin stereo"])
    if q1 == "Aerodynamic drag (scales with v³)": score += 1

    q2 = st.radio("2. What motor type is most common in passenger EVs for maximum efficiency?", ["PMSM", "Brushed DC", "Stepper Motor", "Single-phase Induction"])
    if q2 == "PMSM": score += 1

    q3 = st.radio("3. Why does DC fast charging slow down above 80% SOC?", ["Constant Voltage (CV) mode protects battery chemistry", "Charger overheats", "Grid goes offline", "Electric motors switch off"])
    if q3 == "Constant Voltage (CV) mode protects battery chemistry": score += 1

    if st.button("Submit Comprehensive Assessment", type="primary"):
        st.write(f"### Final Score: {score} / 3")
        if score == 3:
            st.success("🌟 Outstanding Engineering Mastery! You demonstrated clear command of EV dynamics, powertrains, and charging physics.")
        else:
            st.info("Good effort! Review the simulation modules to deepen your physical intuition.")


# ==========================================
# STUDENT PROFILE & LEARNING PORTFOLIO VIEW
# ==========================================
elif selected_lecture == "👤 My Learning Progress & Portfolio":
    st.markdown('<div class="main-title">👤 Student Learning Profile &amp; EV Portfolio</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Official Laboratory Record · Shah &amp; Anchor Kutchhi Engineering College</div>', unsafe_allow_html=True)

    prof = get_student_profile(user["email"]) or {
        "name": user["name"],
        "roll": user.get("roll", "—"),
        "dept": user.get("dept", "—"),
        "division": user.get("division", "—"),
        "completed_modules": {}
    }

    comp_dict = prof.get("completed_modules", {})
    completed_count = len([m for m in comp_dict.values() if m.get("completed") is True])
    scores = [m.get("quiz_score", 0) for m in comp_dict.values() if m.get("completed") is True]
    avg_score = round((sum(scores) / (len(scores)*5)) * 100, 1) if scores else 0.0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Student Name", prof.get("name", user["name"]))
    c2.metric("Roll Number", prof.get("roll", "—"))
    c3.metric("Simulations Completed", f"{completed_count} / 7")
    c4.metric("Avg Pass Score", f"{avg_score}%")

    st.progress(completed_count / 7.0, text=f"Overall Lab Completion Progress: {int((completed_count/7)*100)}%")

    st.markdown("### Module Status & Dossier")
    for m_key, m_info in EV_MODULES_DATA.items():
        data = comp_dict.get(m_key, {})
        is_done = data.get("completed", False)
        attempts = data.get("attempts", 0)
        
        status_badge = "✓ COMPLETED" if is_done else ("⚠️ RETRY REQUIRED" if attempts > 0 else "⏳ PENDING")
        score_text = f"Score: {data.get('quiz_score', 0)}/5 ({data.get('quiz_percentage', 0)}%)" if attempts > 0 else "Not Attempted"
        
        with st.expander(f"{m_info['title']} — {status_badge} ({score_text})", expanded=is_done):
            if is_done:
                t_str = time.strftime('%d %b %Y, %I:%M %p', time.localtime(data.get('last_attempt_at', time.time())))
                st.markdown(f"**Completion Status:** <span class='pass-badge'>PASSED (Attempts: {attempts})</span>", unsafe_allow_html=True)
                st.caption(f"Last Attempt: {t_str}")
                st.markdown(f"**Submitted Technical Reflection:**")
                st.write(data.get("reflection", "No reflection text provided."))
                if data.get("parameters"):
                    st.caption(f"Tested Parameters: {data['parameters']}")
            elif attempts > 0:
                st.markdown(f"<span class='fail-badge'>RETRY REQUIRED (Score: {data.get('quiz_score', 0)}/5 | Attempts: {attempts})</span>", unsafe_allow_html=True)
                st.warning("Minimum 3/5 required to pass. Please re-run the simulation and retry.")
            else:
                st.info("Simulation not yet completed. Select this module from the sidebar to begin.")


# ==========================================
# ADMIN DASHBOARD & USER ROSTER MANAGEMENT
# (Only Admin Can Access)
# ==========================================
elif selected_lecture == "🛡️ Admin Dashboard & User Management":
    if not is_admin:
        st.error("Access Restricted: Only college administrators can access the User Management & Master Progress Portal.")
        st.stop()

    st.markdown('<div class="main-title">🛡️ Administrator Portal &amp; Student Progress</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Continuous Internal Assessment (NBA Criterion 2.2.1) · Student Roster &amp; Password Management</div>', unsafe_allow_html=True)

    tab_overview, tab_users, tab_reflections = st.tabs([
        "📊 Master Progress Register",
        "👥 User & Password Management",
        "📝 Student Reflections Dossier"
    ])

    all_students = get_all_students_progress()
    total_st = len(all_students)
    total_sims_done = sum(s["completed_count"] for s in all_students)
    class_avg = round(sum(s["average_score"] for s in all_students) / total_st, 1) if total_st > 0 else 0.0

    with tab_overview:
        m1, m2, m3 = st.columns(3)
        m1.metric("Enrolled Students", total_st)
        m2.metric("Total Completed Modules", total_sims_done)
        m3.metric("Class Average Score", f"{class_avg}%")

        st.markdown("### Class Completion Matrix (Pass Rule: >= 3/5)")
        if total_st == 0:
            st.info("No students enrolled yet. Go to the 'User & Password Management' tab to add students or bulk-upload a CSV roster.")
        else:
            table_rows = []
            for s in all_students:
                row = {
                    "Roll No": s["roll"],
                    "Student Name": s["name"],
                    "Department": s["dept"],
                    "Division": s["division"],
                    "Completed": f"{s['completed_count']} / 7",
                    "Progress": f"{s['completion_pct']}%",
                    "Avg Score": f"{s['average_score']}%",
                }
                for i in range(1, 8):
                    m_k = f"module_{i}"
                    m_d = s["modules"].get(m_k, {})
                    if m_d.get("completed"):
                        row[f"M{i}"] = f"✓ ({m_d.get('quiz_score',0)}/5)"
                    elif m_d.get("attempts", 0) > 0:
                        row[f"M{i}"] = f"✗ Retry ({m_d.get('quiz_score',0)}/5)"
                    else:
                        row[f"M{i}"] = "—"
                table_rows.append(row)

            df_matrix = pd.DataFrame(table_rows)
            st.dataframe(df_matrix, use_container_width=True)

            excel_path = "/tmp/SAKEC_EV_Master_Progress_Register.xlsx"
            export_master_excel(excel_path)
            with open(excel_path, "rb") as f:
                st.download_button(
                    label="⬇ Download Master Progress Register & Reflections (.xlsx)",
                    data=f,
                    file_name="SAKEC_EV_Master_Progress_Register.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary"
                )

    with tab_users:
        st.subheader("Enroll Students & Faculty (Admin Only)")
        st.caption("Only administrators can add students, assign default passwords, and reset credentials.")

        u_tab1, u_tab2, u_tab3 = st.tabs(["➕ Add Single User", "📤 Bulk CSV Upload", "🔑 Change / Reset Passwords"])
        
        with u_tab1:
            u_c1, u_c2 = st.columns(2)
            with u_c1:
                new_name = st.text_input("Full Name *", key="new_u_name")
                new_roll = st.text_input("Roll Number (for students) *", key="new_u_roll")
                new_role = st.selectbox("Role *", ["student", "faculty"], key="new_u_role")
            with u_c2:
                new_email = st.text_input("College Email ID (@sakec.ac.in) *", key="new_u_email")
                new_dept = st.selectbox("Department *", SAKEC_DEPARTMENTS, key="new_u_dept")
                new_div = st.text_input("Division / Batch", key="new_u_div")
            
            custom_p = st.text_input("Initial Password (leave blank for default firstname@123)", type="password", key="new_u_pass")

            if st.button("Enroll User", type="primary"):
                if new_name.strip() and new_email.strip():
                    u_rec, gen_p = add_user(new_name, new_roll, new_email, new_role, new_dept, new_div, custom_p or None)
                    st.success(f"User {new_name} ({new_email}) enrolled successfully! Initial password: {gen_p}")
                else:
                    st.error("Name and Email are required.")

        with u_tab2:
            st.markdown("#### Bulk Enroll Students via CSV")
            csv_text = st.text_area(
                "Paste CSV Roster (Format: Roll No, Full Name, Email ID, Department, Division)",
                placeholder="23AIDS101,Aarav Patil,aarav.patil@sakec.ac.in,Artificial Intelligence & Data Science,Div A\n23AIDS102,Diya Shah,diya.shah@sakec.ac.in,Artificial Intelligence & Data Science,Div A",
                height=150
            )
            if st.button("Process & Enroll Roster", type="primary"):
                if csv_text.strip():
                    created_count, details = bulk_upload_users_csv(csv_text, default_role="student")
                    st.success(f"Successfully processed {created_count} student accounts with default password firstname@123.")
                    st.dataframe(pd.DataFrame(details))
                else:
                    st.error("Please paste CSV data.")

        with u_tab3:
            st.markdown("#### Change / Reset Password for Any User")
            all_users = load_users()
            user_emails = sorted(list(all_users.keys()))
            sel_email = st.selectbox("Select User Account:", user_emails)
            
            curr_u = all_users[sel_email]
            st.write(f"**Name:** {curr_u.get('name')} | **Roll:** {curr_u.get('roll')} | **Role:** {curr_u.get('role').upper()}")
            
            new_pass_input = st.text_input("New Password (leave blank to reset to default firstname@123)", type="password", key="pwd_reset_inp")
            if st.button("Update / Reset Password"):
                new_p, err = reset_user_password(sel_email, new_pass_input or None)
                if not err:
                    st.success(f"Password for {sel_email} updated successfully! New password: {new_p}")
                else:
                    st.error(err)

            if sel_email != "admin@sakec.ac.in":
                if st.button("🗑 Delete User Account", type="secondary"):
                    delete_user(sel_email)
                    st.warning(f"User {sel_email} deleted.")
                    st.rerun()

    with tab_reflections:
        st.subheader("Student Qualitative Reflections Dossier")
        st.caption("Inspect individual student observations and physical reasoning across simulation modules.")
        
        student_emails = [s["email"] for s in all_students if s["completed_count"] > 0]
        if not student_emails:
            st.info("No student reflections submitted yet.")
        else:
            sel_st_email = st.selectbox("Select Student to Audit:", student_emails)
            st_prof = get_student_profile(sel_st_email) or {}
            
            st.write(f"### Student: {st_prof.get('name')} ({st_prof.get('roll')}) — {st_prof.get('dept')}")
            for m_k, m_d in st_prof.get("completed_modules", {}).items():
                m_title = EV_MODULES_DATA.get(m_k, {}).get("title", m_k)
                with st.expander(f"{m_title} — Status: {m_d.get('status')} (Score: {m_d.get('quiz_score')}/5)"):
                    st.write(f"**Reflection:** {m_d.get('reflection', '—')}")
                    st.caption(f"Tested Parameters: {m_d.get('parameters', {})}")


# Footer
st.markdown('<div class="footer">Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai<br>Developed by <b>Dr. Rohan Borgalli</b> · Autonomous Institute Affiliated to University of Mumbai</div>', unsafe_allow_html=True)
