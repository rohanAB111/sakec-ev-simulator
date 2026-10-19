"""
SAKEC Electric Vehicle Engineering Simulation Platform
Backend Data Persistence, Assessment Analytics, and Excel Report Engine
Developed by Dr. Rohan Borgalli for Shah & Anchor Kutchhi Engineering College
"""

import os
import json
import time
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RECORDS_FILE = os.path.join(DATA_DIR, "ev_student_records.json")

def load_records():
    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print("Error loading records:", e)
    return {
        "students": {},
        "metadata": {
            "college": "Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai",
            "faculty": "Dr. Rohan Borgalli"
        }
    }

def save_records(records):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

def register_or_get_student(name, roll, email, dept, division=""):
    records = load_records()
    email_key = email.strip().lower()
    if email_key not in records["students"]:
        records["students"][email_key] = {
            "name": name.strip(),
            "roll": roll.strip().upper(),
            "email": email_key,
            "dept": dept.strip(),
            "division": division.strip(),
            "registered_at": time.time(),
            "last_active": time.time(),
            "completed_modules": {}
        }
        save_records(records)
    else:
        st_data = records["students"][email_key]
        if name: st_data["name"] = name.strip()
        if roll: st_data["roll"] = roll.strip().upper()
        if dept: st_data["dept"] = dept.strip()
        if division: st_data["division"] = division.strip()
        st_data["last_active"] = time.time()
        save_records(records)
    return records["students"][email_key]

def complete_simulation(email, name, roll, dept, division, module_id, reflection, score, total_q, params=None):
    records = load_records()
    email_key = email.strip().lower()
    if email_key not in records["students"]:
        register_or_get_student(name, roll, email_key, dept, division)
        records = load_records()

    st_data = records["students"][email_key]
    st_data["completed_modules"][module_id] = {
        "completed": True,
        "completed_at": time.time(),
        "reflection": reflection.strip(),
        "quiz_score": int(score),
        "quiz_total": int(total_q),
        "quiz_percentage": round((score / total_q) * 100, 1) if total_q > 0 else 100.0,
        "parameters": params or {}
    }
    st_data["last_active"] = time.time()
    save_records(records)
    return True

def get_student_profile(email):
    records = load_records()
    return records["students"].get(email.strip().lower(), None)

def get_all_students_progress():
    records = load_records()
    students_list = []
    for email, s in records["students"].items():
        comp = s.get("completed_modules", {})
        total_completed = len([m for m in comp.values() if m.get("completed")])
        scores = [m.get("quiz_percentage", 0) for m in comp.values() if m.get("completed")]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        students_list.append({
            "roll": s.get("roll", "—"),
            "name": s.get("name", "—"),
            "email": email,
            "dept": s.get("dept", "—"),
            "division": s.get("division", "—"),
            "completed_count": total_completed,
            "total_modules": 7,
            "completion_pct": round((total_completed / 7) * 100, 1),
            "average_score": avg_score,
            "last_active": s.get("last_active", 0),
            "modules": comp
        })
    students_list.sort(key=lambda x: x["roll"])
    return students_list

def export_master_excel(output_path):
    students = get_all_students_progress()
    wb = openpyxl.Workbook()

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    green_fill = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")
    title_font = Font(name="Calibri", size=15, bold=True, color="1B365D")
    sub_font = Font(name="Calibri", size=10, italic=True, color="555555")
    bold_font = Font(name="Calibri", size=11, bold=True)
    normal_font = Font(name="Calibri", size=10)
    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )

    ws1 = wb.active
    ws1.title = "EV_Progress_Register"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "SHAH & ANCHOR KUTCHHI ENGINEERING COLLEGE, CHEMBUR, MUMBAI"
    ws1["A1"].font = title_font
    ws1["A2"] = "Electric Vehicle Engineering Simulation Platform — Continuous Assessment (CCE / NBA Criterion 2.2.1)"
    ws1["A2"].font = bold_font
    ws1["A3"] = "Developed by Dr. Rohan Borgalli · Consolidated Student Progress Register"
    ws1["A3"].font = sub_font

    headers = [
        "Roll No", "Student Name", "Department", "Division",
        "Mod 1 (Dynamics)", "Mod 2 (Motors)", "Mod 3 (Battery)",
        "Mod 4 (Regen)", "Mod 5 (Charging)", "Mod 6 (Decarbon)",
        "Mod 7 (TCO)", "Completed / 7", "Avg Score (%)", "Status"
    ]

    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=5, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    row_num = 6
    module_keys = [f"module_{i}" for i in range(1, 8)]

    for st in students:
        ws1.cell(row=row_num, column=1, value=st["roll"]).font = bold_font
        ws1.cell(row=row_num, column=2, value=st["name"]).font = normal_font
        ws1.cell(row=row_num, column=3, value=st["dept"]).font = normal_font
        ws1.cell(row=row_num, column=4, value=st["division"]).font = normal_font

        for m_idx, m_key in enumerate(module_keys, 5):
            comp_data = st["modules"].get(m_key, {})
            is_comp = comp_data.get("completed", False)
            score = comp_data.get("quiz_percentage", 0)
            cell = ws1.cell(row=row_num, column=m_idx)
            if is_comp:
                cell.value = f"✓ ({score}%)"
                cell.fill = green_fill
                cell.font = Font(name="Calibri", size=9, color="0F5132")
            else:
                cell.value = "—"
                cell.font = Font(name="Calibri", size=9, color="888888")
            cell.alignment = Alignment(horizontal="center")

        ws1.cell(row=row_num, column=12, value=f"{st['completed_count']} / 7").alignment = Alignment(horizontal="center")
        ws1.cell(row=row_num, column=13, value=f"{st['average_score']}%").alignment = Alignment(horizontal="center")
        
        status_cell = ws1.cell(row=row_num, column=14)
        if st["completed_count"] == 7:
            status_cell.value = "ALL COMPLETED"
            status_cell.fill = green_fill
        elif st["completed_count"] >= 4:
            status_cell.value = "IN PROGRESS"
        else:
            status_cell.value = "PENDING"
        status_cell.alignment = Alignment(horizontal="center")

        for c in range(1, 15):
            ws1.cell(row=row_num, column=c).border = thin_border
        row_num += 1

    for col in ws1.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = max(max_len + 3, 12)

    # SHEET 2: Student Technical Reflections Dossier
    ws2 = wb.create_sheet(title="Reflections_Dossier")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "STUDENT SIMULATION REFLECTION DOSSIER"
    ws2["A1"].font = title_font
    ws2["A2"] = "Qualitative Engineering Observations & Physical Reasoning per Module"
    ws2["A2"].font = sub_font

    ref_headers = ["Roll No", "Student Name", "Module", "Score (%)", "Submitted Engineering Reflection"]
    for col_idx, h in enumerate(ref_headers, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    ref_row = 5
    for st in students:
        for m_key, m_data in st["modules"].items():
            if m_data.get("completed"):
                ws2.cell(row=ref_row, column=1, value=st["roll"]).font = bold_font
                ws2.cell(row=ref_row, column=2, value=st["name"]).font = normal_font
                ws2.cell(row=ref_row, column=3, value=m_key.replace("module_", "Simulation ")).font = normal_font
                ws2.cell(row=ref_row, column=4, value=f"{m_data.get('quiz_percentage', 0)}%").alignment = Alignment(horizontal="center")
                ref_cell = ws2.cell(row=ref_row, column=5, value=m_data.get("reflection", "—"))
                ref_cell.alignment = Alignment(wrap_text=True)
                for c in range(1, 6):
                    ws2.cell(row=ref_row, column=c).border = thin_border
                ref_row += 1

    ws2.column_dimensions["A"].width = 14
    ws2.column_dimensions["B"].width = 22
    ws2.column_dimensions["C"].width = 16
    ws2.column_dimensions["D"].width = 12
    ws2.column_dimensions["E"].width = 80

    wb.save(output_path)
    return output_path
