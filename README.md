# SAKEC Electric Vehicle Engineering Simulation Platform

**Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai**  
*An Autonomous Institute Affiliated to University of Mumbai · NAAC 'A' Grade · Approved by AICTE*  
**Developed by Dr. Rohan Borgalli**

---

## ⚡ Overview

The **SAKEC EV Simulation Platform** is an accredited laboratory and active-learning suite designed for engineering students. It bridges theoretical Newtonian vehicle mechanics, electrical machines, battery electrochemistry, and power electronics with interactive simulation, qualitative student reflections, auto-graded concept testing, and student portfolio progress tracking compliant with **NBA Criterion 2.2.1** and SAKEC Continuous Internal Evaluation (CCE).

---

## 🌟 Key Features

### 1. Role-Based Login & SAKEC Directory Integration
* **Student Portal:** Students enter their Name, Roll Number, Official College Email (`@sakec.ac.in`), Department, and Division.
* **Faculty/Admin Portal:** Faculty log in (`admin@sakec.ac.in` / `admin@123`) to access college-wide progress matrices and student reflection dossiers.
* **Institutional SSO:** Supports Microsoft 365 Entra ID Single Sign-On and direct OneDrive for Business synchronization.

### 2. Seven Interactive EV Engineering Simulation Modules
1. **Module 1: Vehicle Dynamics & Tractive Effort Sizing** (Aerodynamic drag scaling with v³, rolling resistance, gradient force, acceleration power demand).
2. **Module 2: Electric Traction Motors & Drives** (PMSM vs Induction motor torque-speed curves, base speed, field weakening region, drive sizing).
3. **Module 3: Battery Chemistries & Range Sizing** (LFP vs NMC comparative analysis, open circuit voltage curves, internal resistance R0 voltage sag, pack mass penalty).
4. **Module 4: Regenerative Braking & Energy Flow** (Kinetic energy recovery under urban vs highway cycles, brake blending, battery SOC cutoff).
5. **Module 5: EV Charging Infrastructure & CC-CV Profile** (Constant Current to Constant Voltage transition at 80% SOC, lithium plating prevention, thermal rise).
6. **Module 6: Well-to-Wheel (WTW) Decarbonization** (Thermal coal-heavy grid emissions vs renewable solar/wind grid lifecycle parity).
7. **Module 7: Total Cost of Ownership (TCO)** (CapEx premium vs OpEx fuel savings per km, fleet payback distance).

### 3. Student Qualitative Reflections & Concept Checks
* **Post-Simulation Engineering Reflection:** Guided prompt for each module requiring students to document observed physical trade-offs and sensitivity analysis.
* **Understanding Verification Quiz:** 3 auto-graded multiple-choice and numerical questions with immediate feedback and step-by-step physical explanations.
* **Mark as Completed:** Locks student submission, records tested parameters, reflection text, score, and timestamp to their student profile.

### 4. Student Profile & Learning Portfolio
* Real-time progress bar (e.g. 5 of 7 completed, 71%).
* Detailed dossier of all completed modules, reflection logs, and scores.

### 5. Faculty & Administrator Dashboard
* Live class progress register showing all enrolled students, Roll Numbers, Departments, module completion checkmarks (S1 through S7), and average scores.
* Reflection Dossier Viewer to audit student qualitative answers.
* One-click export to formatted **Excel (.xlsx)** for NBA/NAAC Course Outcome (CO) records.

### 6. Microsoft 365 & OneDrive Sync
* Automatically syncs student portfolios and faculty gradebooks to licensed SAKEC OneDrive storage via Microsoft Graph API.

---

## 🚀 Running the Platform Locally

1. Clone or extract the repository folder:
   ```bash
   cd sakec-ev-simulation-platform
   ```
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. Open your browser at `http://localhost:8501`.

---

Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai  
**Developed by Dr. Rohan Borgalli**
