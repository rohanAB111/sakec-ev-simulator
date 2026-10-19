# SAKEC EV Simulation Platform — Version 4.0 Changelog

**Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai**  
*Course: Introduction to Electric Vehicles (T26104.3) · Continuous Internal Assessment (NBA Criterion 2.2.1)*  
**Developed by Dr. Rohan Borgalli**

---

### 1. Self-Registration & Account Creation for Students & Staff
- Added a **'Create New Account (Students & Staff)'** tab alongside the **'Sign In'** tab on the login screen.
- Supports registration as either **Student** (Roll Number / Student ID, Department, Division) or **Faculty / Staff** (Employee ID / Designation, Department).
- Instant login upon registration with secure salted SHA-256 password hashing.
- Dual-login capability: users can log in using either their email ID or their Roll Number / Employee ID.

### 2. Simulation Module & Post-Simulation Questions Visibility Fix
- **Module Dispatch Fix:** Replaced fragile string matching with keyword-resilient dispatch ('Module 1' / 'Dynamics', etc.), resolving the bug where simulations and post-simulation questions were completely blank.
- **Post-Simulation Block Integration:** Linked render_post_simulation_block to all 7 modules with live slider parameters passed to tested_params.
- **5-Question Verification & Pass Rule:** Requires reflection (>=20 characters) and at least 3/5 correct answers (>=60%) to pass. Scoring <3 requires re-attempt.
- **Faculty / Admin Solution Preview:** Teachers have an in-place expander with verified answers and physical explanations.

### 3. Commercial Vehicle Slider Bounds Protection
- Extended slider upper bounds (mass up to 18,000 kg, motor up to 350 kW, torque up to 1,500 Nm, battery up to 300 kWh) for heavy vehicles like the Olectra e-Bus.
