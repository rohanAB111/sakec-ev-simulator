"""
SAKEC Electric Vehicle Engineering Simulation Platform
Pedagogical Reflection Prompts and 5 Parameter-Grounded Concept Questions per Module
Pass Requirement: Minimum 3 of 5 correct (>= 60%) to earn Completion Credit
Developed by Dr. Rohan Borgalli for Shah & Anchor Kutchhi Engineering College
"""

EV_MODULES_DATA = {
    "module_1": {
        "title": "1️⃣ Vehicle Dynamics & Tractive Effort Sizing",
        "short_title": "Vehicle Dynamics",
        "reflection_prompt": (
            "What physical trade-offs did you observe when changing the vehicle speed from city driving "
            "(40 km/h) to highway cruising (100 km/h)? Specifically, explain which resistive force component "
            "(Rolling Resistance vs Aerodynamic Drag) dominated the power demand at each speed, and how "
            "vehicle mass impacts hill climbing vs flat road acceleration."
        ),
        "questions": [
            {
                "q": "How does aerodynamic drag power demand scale with vehicle speed (v)?",
                "options": [
                    "Linearly with speed (P ∝ v)",
                    "With the square of speed (P ∝ v²)",
                    "With the cube of speed (P ∝ v³)",
                    "Independent of vehicle speed"
                ],
                "correct": 2,
                "explain": "Aerodynamic drag force is proportional to v² (F_ad = 0.5 * rho * Cd * A * v²). Therefore, power (Force × Velocity) scales with v³."
            },
            {
                "q": "At lower urban speeds (< 45 km/h), which force component accounts for the majority of resistive power?",
                "options": [
                    "Rolling resistance and inertia (mass-dependent)",
                    "Aerodynamic drag",
                    "Coriolis effect",
                    "Battery internal heat radiation"
                ],
                "correct": 0,
                "explain": "Rolling resistance is proportional to vehicle weight (F_rr = Crr * m * g). At city speeds, aerodynamic drag is low, so vehicle mass and rolling friction dominate."
            },
            {
                "q": "If a vehicle's frontal area (A) is increased by 20% while keeping Cd constant, what is the impact on aerodynamic drag force at 100 km/h?",
                "options": [
                    "Increases by exactly 20%",
                    "Increases by 44%",
                    "Decreases by 20%",
                    "Remains completely unchanged"
                ],
                "correct": 0,
                "explain": "Drag force is directly proportional to frontal area (F_ad ∝ A). A 20% increase in A produces an exact 20% increase in drag force."
            },
            {
                "q": "When climbing a 10% road grade (approx. 5.7° incline), what is the primary component determining motor tractive force?",
                "options": [
                    "Hill-climbing resistance force F_hc = m * g * sin(θ)",
                    "Cabin air conditioning electrical power",
                    "Inverter capacitor leakage current",
                    "Tire aerodynamic wake turbulence"
                ],
                "correct": 0,
                "explain": "Hill-climbing resistance F_hc = m * g * sin(θ) directly opposes gravity. On steep gradients, it accounts for over 70% of peak motor tractive force demand."
            },
            {
                "q": "Why does adding a 500 kg battery pack to an EV create a greater energy consumption penalty in city driving than on steady highway cruising?",
                "options": [
                    "City driving involves repeated kinetic accelerations (F = m * a) and continuous rolling resistance (F = Crr * m * g)",
                    "Aerodynamic drag is directly proportional to vehicle weight",
                    "Motors shut down at higher weights",
                    "Battery voltage drops to zero when mass increases"
                ],
                "correct": 0,
                "explain": "In city driving with repeated stop-and-go cycles, inertial acceleration energy (0.5 * m * v²) and rolling friction depend directly on vehicle mass. Highway cruising is primarily aerodynamically limited."
            }
        ]
    },
    "module_2": {
        "title": "2️⃣ Electric Traction Motors & Drives",
        "short_title": "Motors & Drives",
        "reflection_prompt": (
            "Compare the operating characteristics of traction motors below base speed versus above base speed. "
            "Explain why Permanent Magnet Synchronous Motors (PMSM) are widely chosen for passenger cars (e.g. Tata Nexon EV) "
            "while Induction Motors or Switched Reluctance Motors are favored in commercial transit or cost-sensitive fleets."
        ),
        "questions": [
            {
                "q": "In an electric vehicle motor drive, what characterizes the operating region below base speed?",
                "options": [
                    "Constant Torque region (maximum acceleration capability)",
                    "Constant Power region (voltage saturation)",
                    "Field Weakening region",
                    "Negative slip generation"
                ],
                "correct": 0,
                "explain": "Below base speed, current is maintained at rated maximum while inverter voltage scales with speed, delivering constant peak torque."
            },
            {
                "q": "What happens when an EV traction motor operates above its rated base speed?",
                "options": [
                    "Motor torque drops inversely with speed to maintain Constant Power (Field Weakening)",
                    "Torque continues increasing indefinitely",
                    "Inverter frequency drops to zero",
                    "Motor operates in mechanical stall"
                ],
                "correct": 0,
                "explain": "Above base speed, inverter voltage reaches the battery pack limit. Field weakening is applied, causing torque to decrease as 1/v while power remains approximately constant."
            },
            {
                "q": "Why is Permanent Magnet Synchronous Motor (PMSM) technology widely adopted in passenger EVs?",
                "options": [
                    "Highest power density and efficiency across typical urban driving cycles",
                    "Lowest cost with zero rare-earth materials",
                    "Requires no motor controller or inverter",
                    "Operates strictly on single-phase AC utility supply"
                ],
                "correct": 0,
                "explain": "PMSM motors eliminate rotor copper losses via permanent magnets, yielding peak efficiencies exceeding 95% and high torque-to-weight ratios."
            },
            {
                "q": "If a traction motor produces 250 Nm of torque and the vehicle single-speed transmission has a gear ratio of 9:1 with 95% efficiency, what is the torque at the drive wheels?",
                "options": [
                    "2,137.5 Nm",
                    "250.0 Nm",
                    "27.7 Nm",
                    "22,500 Nm"
                ],
                "correct": 0,
                "explain": "Wheel Torque = Motor Torque * Gear Ratio * Efficiency = 250 * 9 * 0.95 = 2,137.5 Nm. Gear reduction multiplies motor torque into high launch force."
            },
            {
                "q": "In which quadrant of the motor drive operational envelope does regenerative braking occur?",
                "options": [
                    "Quadrant II (Forward speed with negative/braking torque)",
                    "Quadrant I (Forward motoring with positive torque)",
                    "Quadrant III (Reverse motoring with negative speed and torque)",
                    "Quadrant IV (Reverse braking only)"
                ],
                "correct": 0,
                "explain": "Regenerative braking while driving forward represents Quadrant II operation: vehicle rotation is positive (forward) while motor produces negative electromagnetic torque (generator mode)."
            }
        ]
    },
    "module_3": {
        "title": "3️⃣ Battery Chemistries & Range Sizing",
        "short_title": "Battery Sizing",
        "reflection_prompt": (
            "Discuss the trade-offs between Lithium Iron Phosphate (LFP) and Nickel Manganese Cobalt (NMC) chemistries. "
            "Explain how the battery internal resistance (R0) leads to terminal voltage sag during aggressive acceleration, "
            "and why sizing a larger battery pack has diminishing returns due to the weight penalty."
        ),
        "questions": [
            {
                "q": "Which lithium-ion battery chemistry is favored in tropical climates like India for its superior thermal stability (>270°C thermal runaway threshold) and cycle life (>3000 cycles)?",
                "options": [
                    "LFP (Lithium Iron Phosphate)",
                    "NMC 811 (Nickel Manganese Cobalt)",
                    "Lead-Acid",
                    "Nickel-Cadmium"
                ],
                "correct": 0,
                "explain": "LFP's strong phospho-olivine chemical bond prevents oxygen release at elevated temperatures, providing unmatched safety and longevity."
            },
            {
                "q": "Why does a battery pack's terminal voltage drop (sag) during heavy acceleration?",
                "options": [
                    "Ohmic voltage drop across the internal resistance (V_terminal = OCV - I * R_int)",
                    "Chemical decomposition of electrolyte",
                    "Coulombic efficiency exceeding 100%",
                    "Inverter capacitor discharging to zero"
                ],
                "correct": 0,
                "explain": "High discharge current (I) flowing through cell internal resistance (R_int) creates an immediate resistive IR drop, lowering terminal voltage."
            },
            {
                "q": "What is the primary engineering disadvantage of excessively oversizing an EV battery pack to achieve extreme range (>700 km)?",
                "options": [
                    "Severe vehicle weight penalty, which increases rolling resistance and reduces efficiency (Wh/km)",
                    "Motor torque becomes zero",
                    "Regenerative braking becomes impossible",
                    "Tire pressure drops automatically"
                ],
                "correct": 0,
                "explain": "Batteries have finite gravimetric energy density (~150-250 Wh/kg). Oversizing increases curb weight significantly, requiring more structural mass, suspension, and energy just to move the battery itself."
            },
            {
                "q": "Why do automotive battery management systems (BMS) enforce Depth of Discharge (DoD) buffers (e.g. limiting usable capacity to 10% - 90% SOC)?",
                "options": [
                    "To prevent accelerated chemical degradation, electrode micro-cracking, and copper dissolution at extreme low SOC",
                    "To reduce vehicle speed on highways",
                    "To allow Bluetooth communication to the dashboard",
                    "To prevent the radio from discharging the 12V auxiliary battery"
                ],
                "correct": 0,
                "explain": "Operating cells at extreme 0% or 100% states of charge induces high mechanical strain on electrode crystal lattices. Enforcing a 10-90% usable window significantly extends cycle life."
            },
            {
                "q": "In a 1st-order Thevenin Equivalent Circuit Model (ECM) of a lithium cell, what does the parallel R1-C1 branch represent?",
                "options": [
                    "Electrochemical charge-transfer resistance and double-layer diffusion polarization dynamics",
                    "Direct ohmic resistance of the metallic busbars",
                    "Coolant fluid pump flow rate",
                    "Mechanical chassis vibration absorption"
                ],
                "correct": 0,
                "explain": "The R1-C1 branch models transient electrochemical polarization—the delayed voltage recovery observed after a high-current load pulse ceases."
            }
        ]
    },
    "module_4": {
        "title": "4️⃣ Regenerative Braking & Energy Flow",
        "short_title": "Regenerative Braking",
        "reflection_prompt": (
            "Explain why regenerative braking recovers a significantly higher percentage of energy during stop-and-go urban driving "
            "compared to highway cruising. What safety constraints (friction blending, tire slip, battery SOC, and temperature) "
            "limit the maximum allowable regen power?"
        ),
        "questions": [
            {
                "q": "Under which driving profile does regenerative braking contribute the highest percentage of energy recovery?",
                "options": [
                    "Frequent urban stop-and-go driving with repeated decelerations",
                    "Constant 120 km/h highway cruising",
                    "Steep continuous uphill mountain climbing",
                    "Vehicle idling in traffic with zero motion"
                ],
                "correct": 0,
                "explain": "In city driving, frequent braking events allow kinetic energy to be recovered into the battery rather than dissipated as heat in brake friction pads."
            },
            {
                "q": "What happens to an EV's regenerative braking capability when the battery is at 100% State of Charge (SOC)?",
                "options": [
                    "Regen is severely limited or disabled to prevent battery overvoltage and cell damage",
                    "Regen power doubles automatically",
                    "Motor switches to reverse direction",
                    "Battery pack switches to AC generation"
                ],
                "correct": 0,
                "explain": "When fully charged, the battery cannot accept incoming charging current without dangerously exceeding cell voltage limits, so the Battery Management System (BMS) disables regen and relies solely on mechanical friction brakes."
            },
            {
                "q": "What system seamlessly combines electric regenerative braking and mechanical hydraulic friction brakes to ensure driver pedal feel and stability?",
                "options": [
                    "Brake Blending & Cooperative Braking System (Electro-Hydraulic)",
                    "Manual handbrake cable",
                    "Exhaust gas recirculation valve",
                    "Permanent magnet stator decoupling"
                ],
                "correct": 0,
                "explain": "Cooperative brake blending maximizes electric regen first, then seamlessly engages hydraulic friction calipers when deceleration demand exceeds motor torque limits."
            },
            {
                "q": "A 1,600 kg EV decelerates from 72 km/h (20 m/s) to a complete stop. What is the total kinetic energy that can theoretically be harvested before accounting for motor/battery losses?",
                "options": [
                    "320 kJ (approx. 0.089 kWh)",
                    "32 kJ",
                    "3,200 kJ",
                    "16 kJ"
                ],
                "correct": 0,
                "explain": "E_kinetic = 0.5 * m * v² = 0.5 * 1600 * (20)² = 0.5 * 1600 * 400 = 320,000 Joules = 320 kJ."
            },
            {
                "q": "During emergency panic braking on a wet road, why must the ABS system rapidly override regenerative braking?",
                "options": [
                    "Motor torque response can induce tire slip/lock-up on slippery surfaces faster than tire-road adhesion allows",
                    "Battery cells explode if charged during rain",
                    "Inverters are waterproof and cannot operate under moisture",
                    "Hydraulic brakes are completely disabled during emergency stops"
                ],
                "correct": 0,
                "explain": "Active vehicle dynamics safety (ABS/ESC) requires rapid, independent per-wheel brake pressure modulation (tens of milliseconds) to prevent wheel lockup, requiring immediate throttling of drive-axle regen torque."
            }
        ]
    },
    "module_5": {
        "title": "5️⃣ EV Charging Infrastructure & CC-CV Profile",
        "short_title": "EV Charging & CC-CV",
        "reflection_prompt": (
            "Analyze the two phases of lithium battery charging: Constant Current (CC) and Constant Voltage (CV). "
            "Explain why the charging rate slows dramatically once the battery reaches 80% SOC, and discuss "
            "the thermal management challenges during high-power DC Fast Charging (>50 kW)."
        ),
        "questions": [
            {
                "q": "During the initial fast charging phase (0% to ~80% SOC), how is energy delivered to the battery cells?",
                "options": [
                    "Constant Current (CC) phase with rising terminal voltage",
                    "Constant Voltage (CV) phase with rising current",
                    "Pulsed reverse AC waveform",
                    "Linear inductive resonance"
                ],
                "correct": 0,
                "explain": "In the CC phase, maximum safe charging current is supplied while cell voltage gradually rises toward the upper cutoff threshold (~3.65V for LFP, ~4.2V for NMC)."
            },
            {
                "q": "Why does fast charging taper off significantly during the Constant Voltage (CV) phase from 80% to 100% SOC?",
                "options": [
                    "Current must taper down to prevent cell overpotential, lithium plating, and electrolyte breakdown",
                    "Grid utility transformers turn off automatically",
                    "Inverter frequency decreases below 1 Hz",
                    "Electric vehicle tires lose electrical grounding"
                ],
                "correct": 0,
                "explain": "To prevent exceeding the upper voltage ceiling, current naturally decays exponentially as the open-circuit voltage approaches the applied charger voltage, preventing hazardous metallic lithium dendrite formation."
            },
            {
                "q": "What is the C-rate when a 40 kWh battery pack is charged at a steady rate of 80 kW?",
                "options": [
                    "2.0 C (Full charge in theoretical 0.5 hours)",
                    "0.5 C (Full charge in theoretical 2.0 hours)",
                    "4.0 C",
                    "0.2 C"
                ],
                "correct": 0,
                "explain": "C-rate = Power (or Current) / Capacity = 80 kW / 40 kWh = 2.0 C. A 1C charge theoretical duration is 1 hour; 2C is 30 minutes."
            },
            {
                "q": "What is the primary factor limiting ultra-fast charging (>150 kW) in tropical Indian ambient temperatures (>40°C)?",
                "options": [
                    "Internal Joule heating (I² * R) requiring aggressive active liquid coolant chilling to keep cell temperatures below 45°C",
                    "Lack of 3-phase alternating current",
                    "Inability of copper cables to carry DC power",
                    "Vehicle tire rubber melting from static electricity"
                ],
                "correct": 0,
                "explain": "At 150 kW, currents exceed 350-400 Amps. High I²R resistive heating creates severe thermal dissipation bottlenecks, necessitating active liquid chiller loops."
            },
            {
                "q": "What connector standard is mandated for DC Fast Charging passenger vehicles under Indian national standards (AIS-138 Part 2)?",
                "options": [
                    "Combined Charging System 2 (CCS-2)",
                    "Tesla NACS proprietary",
                    "CHAdeMO Type 1 only",
                    "Standard 3-pin 5A domestic plug"
                ],
                "correct": 0,
                "explain": "CCS-2 (Combined Charging System Type 2) is the standard adopted across Indian passenger EVs and commercial fast-charging networks."
            }
        ]
    },
    "module_6": {
        "title": "6️⃣ Well-to-Wheel (WTW) Decarbonization",
        "short_title": "Decarbonization (WTW)",
        "reflection_prompt": (
            "Evaluate the Well-to-Wheel (WTW) emissions of an EV powered by India's current thermal coal-dominated grid (~700 g CO2/kWh) "
            "versus a grid with high renewable integration (solar/wind). Under what circumstances and lifecycle mileage does an EV "
            "break even with a modern BS-VI internal combustion engine (ICE) vehicle?"
        ),
        "questions": [
            {
                "q": "What two sub-stages make up a comprehensive Well-to-Wheel (WTW) vehicle lifecycle emissions audit?",
                "options": [
                    "Well-to-Tank (upstream generation/fuel production) + Tank-to-Wheel (vehicle operational efficiency)",
                    "Factory-to-Dealership + Dealership-to-Customer",
                    "Engine-to-Muffler + Tire-to-Road",
                    "Inverter-to-Motor + Motor-to-Battery"
                ],
                "correct": 0,
                "explain": "WTW assesses the complete pathway: Well-to-Tank (fuel extraction, refining, transmission) and Tank-to-Wheel (conversion into mechanical motion at the vehicle)."
            },
            {
                "q": "Why do electric vehicles have higher 'embodied' manufacturing carbon emissions than conventional petrol/diesel cars before driving their first kilometer?",
                "options": [
                    "Energy-intensive mining, chemical refining, and high-temperature cathode processing for battery cells",
                    "Electric vehicle chassis require heavy cast iron",
                    "Copper wires emit greenhouse gases during manufacturing",
                    "Inverters require chemical coal burning inside the car"
                ],
                "correct": 0,
                "explain": "Extracting and refining battery materials (Lithium, Nickel, Cobalt) and manufacturing cell electrodes in dry rooms produces an upfront carbon debt of ~60-100 kg CO2 per kWh of battery capacity."
            },
            {
                "q": "Even on a coal-heavy electrical grid, why does an EV often produce lower lifecycle CO2 per km than an average petrol car in congested city traffic?",
                "options": [
                    "EV powertrain efficiency (~85-90%) combined with zero idle fuel burn and regenerative braking vastly outperforms ICE thermal efficiency (~18-25%)",
                    "Coal power plants generate zero carbon dioxide",
                    "Electric motors absorb atmospheric carbon during motion",
                    "Electric vehicles do not use any electricity in city traffic"
                ],
                "correct": 0,
                "explain": "Centralized utility thermal plants achieve higher thermodynamic efficiency (~38-42%) than small, throttle-choked urban ICE engines, and EVs waste zero energy at standstill while recovering energy during deceleration."
            },
            {
                "q": "If an EV consumes 130 Wh/km from a grid producing 700 g CO2/kWh, what is its direct operational Tank-to-Wheel + Well-to-Tank carbon emission rate?",
                "options": [
                    "91 g CO2 / km",
                    "130 g CO2 / km",
                    "700 g CO2 / km",
                    "9.1 g CO2 / km"
                ],
                "correct": 0,
                "explain": "Emissions = 0.130 kWh/km * 700 g CO2/kWh = 91 g CO2/km (compared to a typical BS-VI petrol car emitting 130-150 g CO2/km)."
            },
            {
                "q": "What happens to the lifecycle environmental parity break-even distance when an EV is charged primarily via rooftop solar PV?",
                "options": [
                    "Break-even distance drops to under 10,000 km, maximizing decarbonization",
                    "Break-even distance increases to 200,000 km",
                    "Battery pack degrades twice as fast",
                    "Solar charging emits more carbon than diesel generators"
                ],
                "correct": 0,
                "explain": "Rooftop solar has near-zero operational emissions (~20-40 g CO2/kWh lifecycle), rapidly offsetting the manufacturing carbon debt in a fraction of normal vehicle lifespan."
            }
        ]
    },
    "module_7": {
        "title": "7️⃣ Total Cost of Ownership (TCO) Sizing",
        "short_title": "TCO & Economics",
        "reflection_prompt": (
            "Analyze the economic viability of an electric vehicle by comparing Capital Expenditure (CapEx) against Operational Expenditure (OpEx). "
            "Explain why fleet vehicles (taxis, delivery two-wheelers, municipal buses) achieve a much faster financial payback "
            "compared to low-mileage personal cars."
        ),
        "questions": [
            {
                "q": "In Mumbai and Maharashtra urban conditions, what is the typical per-kilometer fuel/energy cost comparison between an electric car (home charging) and a petrol car?",
                "options": [
                    "EV costs ~₹1.2 to ₹1.8/km vs Petrol costs ~₹7.5 to ₹9.0/km (roughly 75-80% operational cost savings)",
                    "EV costs more per kilometer than petrol",
                    "EV and petrol have mathematically identical operating costs",
                    "Petrol costs ₹0.50/km and EV costs ₹5.00/km"
                ],
                "correct": 0,
                "explain": "With residential electricity at ₹7-9/unit and an EV efficiency of ~7-8 km/kWh, running cost is ~₹1.20-1.50/km compared to petrol at ~₹105/liter delivering 13-14 km/L (~₹7.50-8.00/km)."
            },
            {
                "q": "Which vehicle usage profile recovers the upfront EV purchase price premium (CapEx) in the shortest payback period?",
                "options": [
                    "High daily mileage commercial fleets (cabs, delivery bikes, city buses driving >100 km/day)",
                    "Weekend-only personal cars driving <15 km/week",
                    "Classic collector cars parked in a garage",
                    "Seasonal agricultural machinery used 2 weeks per year"
                ],
                "correct": 0,
                "explain": "Because the savings are realized per kilometer driven, high-utilization commercial vehicles accumulate massive OpEx fuel savings rapidly, offsetting the initial battery premium within 12-24 months."
            },
            {
                "q": "What component replacement reserve represents the largest variable in long-term (10-15 year) EV Total Cost of Ownership calculations?",
                "options": [
                    "Traction battery pack replacement / refurbishment",
                    "Electric motor copper rewind",
                    "Instrument cluster LCD replacement",
                    "Side-view mirror glass replacement"
                ],
                "correct": 0,
                "explain": "The traction battery pack accounts for ~30-40% of vehicle capital cost. Factoring potential battery degradation and replacement cycles is critical for long-term TCO modelling."
            },
            {
                "q": "If an EV costs ₹3,00,000 more upfront than an equivalent petrol car, but saves ₹6.00 per kilometer in running costs, what is the simple payback driving distance?",
                "options": [
                    "50,000 km",
                    "300,000 km",
                    "15,000 km",
                    "180,000 km"
                ],
                "correct": 0,
                "explain": "Payback Distance = Price Difference / Savings per km = 300,000 / 6.00 = 50,000 km. For a user driving 15,000 km/year, payback is achieved in ~3.3 years."
            },
            {
                "q": "Why do electric commercial buses (e.g. Olectra Greentech in BEST Mumbai fleets) have lower scheduled mechanical maintenance costs than diesel buses?",
                "options": [
                    "Elimination of engine oil changes, transmission fluids, fuel injectors, spark plugs, particulate filters, and reduced brake pad wear via regen",
                    "Electric buses do not use suspension springs or tires",
                    "Municipal drivers do not require salaries",
                    "Electric bus bodies do not require paint"
                ],
                "correct": 0,
                "explain": "An electric drivetrain possesses ~90% fewer moving parts than a complex diesel powertrain, eliminating exhaust systems, oil filters, timing belts, and radiators."
            }
        ]
    }
}
