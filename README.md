# SAKEC Electric Vehicle Engineering Simulation Platform

**Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai**  
*An Autonomous Institute Affiliated to University of Mumbai · NAAC 'A' Grade · Approved by AICTE*  
**Course:** Introduction to Electric Vehicles (T26104.3)  
**Developed by Dr. Rohan Borgalli**

---

## ⚡ Overview

The **SAKEC EV Simulation Platform** is an accredited interactive simulation and laboratory learning portal designed for engineering students. It unites Newtonian vehicle dynamics, electric traction machines, battery electrochemistry, regenerative braking, CC-CV charging curves, life-cycle decarbonization, and total cost of ownership (TCO) with quantitative simulation sliders, guided qualitative reflections, and rigorous auto-graded concept testing. All results are tracked in a centralized institutional progress register compliant with **NBA Criterion 2.2.1** and SAKEC Continuous Internal Evaluation (CCE).

---

## 🌟 Key Features & Architecture

### 1. Dual Authentication: Self-Registration & Administrative Roster
* **Student & Staff Self-Registration:** Students and faculty can register instantly via the **"Create New Account"** tab using their college email (`@sakec.ac.in`), Roll Number / Employee ID, Department, and Division. Accounts are active immediately with salted SHA-256 password hashing.
* **Dual Login:** Users can sign in using either their email address or their Roll Number / Employee ID.
* **Administrative Control:** Faculty and admins can still add single users, batch enroll students via CSV roster, reset default passwords (`firstname@123`), and manage class access.
* **Microsoft 365 SSO Ready:** Integrated scaffolding for direct Microsoft Entra ID authentication and OneDrive for Business report synchronization.

### 2. Seven Interactive EV Engineering Simulation Modules
1. **Module 1: Vehicle Dynamics & Tractive Effort Sizing** (Aerodynamic drag scaling with $v^3$, rolling resistance, gradient force, acceleration power demand).
2. **Module 2: Electric Traction Motors & Drives** (PMSM, BLDC, and Induction Motor torque-speed envelopes, stall torque, base speed, field-weakening constant power regime).
3. **Module 3: Battery Chemistries & Range Sizing** (LFP vs. NMC vs. Lead-Acid comparison, DoD %, HVAC climate load impact, realistic driving range vs. speed curve).
4. **Module 4: Regenerative Braking & Energy Flow** (Kinetic energy recovery under urban vs. highway deceleration, brake blending, BMS overcharge cutoff at high SoC).
5. **Module 5: EV Charging Infrastructure & CC-CV Profile** (AC Level 1/2 vs. DC Fast Charging, Constant Current to Constant Voltage transition at 80% SoC, charging timeline).
6. **Module 6: Well-to-Wheel (WTW) Decarbonization** (Indian electricity grid 710 g $\text{CO}_2$/kWh baseline vs. petrol/diesel vehicle life-cycle emissions).
7. **Module 7: Total Cost of Ownership (TCO)** (CapEx premium vs. OpEx fuel savings, ₹/km running costs, fleet break-even mileage and payback years).
8. **Module 8: Comprehensive EV Concept Check** (Classroom-wide concept mastery test).

### 3. Student Qualitative Reflections & Strict Pass/Fail Grading
* **Post-Simulation Engineering Reflection:** Guided prompt for each module requiring students to document observed physical trade-offs (minimum 20 characters) before taking the assessment.
* **5-Question Understanding Check:** 5 parameter-grounded engineering questions per module (35 questions in total) testing physical reasoning.
* **Strict Pass Threshold (≥ 3/5 Correct):**
  - Scoring **≥ 3 out of 5 (≥ 60%)** marks the module as **COMPLETED** with celebratory balloons and permanent accreditation in the student's learning profile.
  - Scoring **< 3 out of 5** flags the module as **RETRY REQUIRED**, requiring students to re-run the simulation, observe parameter changes, and retry.
* **Faculty Solution Key:** Instructors and admins have an in-situ solution expander revealing answers and rationale for classroom guidance.

### 4. Student Learning Profile & Portfolio
* Real-time progress bar (e.g. 5 of 7 completed, 71%).
* Complete audit dossier of completed modules, submitted reflections, attempt counts, and scores.

### 5. Faculty & Administrator Dashboard
* **Master Progress Register:** Live matrix showing all enrolled students, Roll Numbers, Departments, module completion statuses (M1 through M7), and average scores.
* **Qualitative Reflections Dossier:** Audit individual student observations across simulation modules.
* **One-Click Excel (.xlsx) Export:** Instant generation of a formatted Master Register spreadsheet with complete student dossiers for NBA/NAAC Course Outcome (CO) records.

---

## 🚀 Running the Platform

### Local Development
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the Streamlit application
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### Default Credentials
* **Admin Login:** `admin@sakec.ac.in` / `admin@123`
* **Student Self-Registration:** Available directly on the login screen under **"Create New Account"**.
* **Pre-enrolled Default Password:** `firstname@123` (e.g., `rahul@123`).

---

Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai  
**Developed by Dr. Rohan Borgalli**
