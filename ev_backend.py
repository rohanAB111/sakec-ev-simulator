"""
SAKEC Electric Vehicle Engineering Simulation Platform
Backend Data Persistence, User Management (Admin Only), Assessment Analytics, and Excel Report Engine
Developed by Dr. Rohan Borgalli for Shah & Anchor Kutchhi Engineering College

Permanent Storage Engine (v4.2 — Hardened Supabase Sync):
- Stores all users (`ev_users`) and student progress (`ev_records`) permanently in Supabase via REST API.
- Handles both top-level and nested `[supabase]` Streamlit Secrets.
- Sanitizes NumPy/non-JSON types, normalizes email casing & role casing, and supports both `jsonb` and `text` columns.
- Surfaces cloud sync errors visibly in Streamlit instead of failing silently.
"""

import os
import json
import time
import hashlib
import urllib.parse
from datetime import datetime, timezone

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    import streamlit as st
except ImportError:
    st = None

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RECORDS_FILE = os.path.join(DATA_DIR, "ev_student_records.json")
USERS_FILE = os.path.join(DATA_DIR, "ev_users.json")

LAST_DB_ERROR = ""

# =========================================================================
# SUPABASE PERMANENT CLOUD STORAGE HELPERS
# =========================================================================

def _get_secret(key, alt_keys=()):
    for k in (key,) + tuple(alt_keys):
        val = os.getenv(k)
        if val and str(val).strip():
            return str(val).strip()
    if st is not None:
        try:
            for k in (key,) + tuple(alt_keys):
                if k in st.secrets:
                    return str(st.secrets[k]).strip()
            if "supabase" in st.secrets:
                sec = st.secrets["supabase"]
                for k in (key,) + tuple(alt_keys):
                    if k in sec:
                        return str(sec[k]).strip()
        except Exception:
            pass
    return ""

def _get_supabase_url():
    return _get_secret("SUPABASE_URL", ("supabase_url", "url", "URL")).rstrip("/")

def _get_supabase_key():
    return _get_secret("SUPABASE_KEY", ("supabase_key", "SUPABASE_SERVICE_ROLE_KEY", "key", "KEY"))

def is_cloud_db_enabled():
    return HAS_REQUESTS and bool(_get_supabase_url()) and bool(_get_supabase_key())

def _record_db_error(context, exc):
    global LAST_DB_ERROR
    msg = f"Supabase {context} failed: {exc}"
    LAST_DB_ERROR = msg
    print(msg)
    if st is not None:
        try:
            st.warning(f"⚠️ Cloud database sync issue ({context}): {exc}")
        except Exception:
            pass

def _sanitize_json(obj):
    """Ensure all nested values (including NumPy scalars) are pure JSON types."""
    return json.loads(json.dumps(obj, default=lambda x: float(x) if hasattr(x, "__float__") else str(x)))

def _parse_row_data(raw_data):
    if isinstance(raw_data, dict):
        return raw_data
    if isinstance(raw_data, str):
        try:
            parsed = json.loads(raw_data)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
    return None

def _sb_headers(prefer=None):
    key = _get_supabase_key()
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = prefer
    return headers

def _sb_url(table):
    return f"{_get_supabase_url()}/rest/v1/{table}"

def _sb_fetch_all(table):
    """Fetch all rows from a Supabase table (paginates past 1000-row PostgREST default)."""
    all_items = {}
    offset = 0
    page_size = 1000
    while True:
        headers = _sb_headers()
        headers["Range-Unit"] = "items"
        headers["Range"] = f"{offset}-{offset + page_size - 1}"
        res = requests.get(
            _sb_url(table),
            headers=headers,
            params={"select": "email,data"},
            timeout=12,
        )
        if not res.ok:
            raise RuntimeError(f"HTTP {res.status_code}: {res.text[:200]}")
        rows = res.json()
        if not isinstance(rows, list):
            break
        for row in rows:
            em = str(row.get("email", "")).strip().lower()
            parsed = _parse_row_data(row.get("data"))
            if em and parsed is not None:
                all_items[em] = parsed
        if len(rows) < page_size:
            break
        offset += page_size
    return all_items

def _sb_upsert_row(table, email_key, data_dict):
    clean_email = email_key.strip().lower()
    payload = {
        "email": clean_email,
        "data": _sanitize_json(data_dict),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    res = requests.post(
        _sb_url(table),
        headers=_sb_headers(prefer="resolution=merge-duplicates,return=minimal"),
        params={"on_conflict": "email"},
        json=payload,
        timeout=12,
    )
    if not res.ok:
        raise RuntimeError(f"HTTP {res.status_code}: {res.text[:200]}")

def _sb_upsert_many(table, mapping):
    if not mapping:
        return
    now_iso = datetime.now(timezone.utc).isoformat()
    payload = [
        {
            "email": str(k).strip().lower(),
            "data": _sanitize_json(v),
            "updated_at": now_iso,
        }
        for k, v in mapping.items()
        if str(k).strip()
    ]
    # Upsert in chunks of 200 to stay well within PostgREST payload limits
    for i in range(0, len(payload), 200):
        chunk = payload[i : i + 200]
        res = requests.post(
            _sb_url(table),
            headers=_sb_headers(prefer="resolution=merge-duplicates,return=minimal"),
            params={"on_conflict": "email"},
            json=chunk,
            timeout=20,
        )
        if not res.ok:
            raise RuntimeError(f"HTTP {res.status_code}: {res.text[:200]}")

def _sb_delete_row(table, email_key):
    encoded = urllib.parse.quote(email_key.strip().lower(), safe="")
    res = requests.delete(
        f"{_sb_url(table)}?email=eq.{encoded}",
        headers=_sb_headers(),
        timeout=12,
    )
    if not res.ok:
        raise RuntimeError(f"HTTP {res.status_code}: {res.text[:200]}")

# =========================================================================
# USER AUTHENTICATION & ADMIN ROSTER MANAGEMENT
# =========================================================================

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(16).hex()
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt

def verify_password(password, salt, hashed):
    test_hash = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return test_hash == hashed

def _default_admin_users():
    h, s = hash_password("admin@123")
    return {
        "admin@sakec.ac.in": {
            "name": "Dr. Rohan Borgalli",
            "roll": "ADMIN-01",
            "email": "admin@sakec.ac.in",
            "role": "admin",
            "dept": "EXTC Engineering",
            "division": "Admin",
            "hash": h,
            "salt": s,
            "created_at": time.time()
        }
    }

def _normalize_users_dict(raw_users):
    normalized = {}
    for k, u in (raw_users or {}).items():
        if not isinstance(u, dict):
            continue
        em = str(u.get("email") or k).strip().lower()
        if not em:
            continue
        u_copy = dict(u)
        u_copy["email"] = em
        u_copy["role"] = str(u_copy.get("role", "student")).strip().lower()
        normalized[em] = u_copy
    return normalized

def load_users():
    if is_cloud_db_enabled():
        try:
            cloud_users = _normalize_users_dict(_sb_fetch_all("ev_users"))
            if cloud_users:
                return cloud_users
            seed_users = None
            if os.path.exists(USERS_FILE):
                try:
                    with open(USERS_FILE, "r", encoding="utf-8") as f:
                        seed_users = _normalize_users_dict(json.load(f))
                except Exception:
                    seed_users = None
            if not seed_users:
                seed_users = _default_admin_users()
            _sb_upsert_many("ev_users", seed_users)
            return seed_users
        except Exception as e:
            _record_db_error("load_users", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                return _normalize_users_dict(json.load(f))
        except Exception as e:
            print("Error loading users:", e)

    default_users = _default_admin_users()
    save_users(default_users)
    return default_users

def save_users(users):
    clean_users = _normalize_users_dict(users)
    if is_cloud_db_enabled():
        try:
            _sb_upsert_many("ev_users", clean_users)
        except Exception as e:
            _record_db_error("save_users", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(clean_users, f, indent=2, ensure_ascii=False)

def authenticate_user(email, password):
    users = load_users()
    email_key = email.strip().lower()
    user = users.get(email_key)
    if not user:
        return {"ok": False, "error": "User account not found. Please contact the administrator to enroll you."}

    if not verify_password(password, user["salt"], user["hash"]):
        return {"ok": False, "error": "Incorrect password. Please contact the administrator to reset your password."}

    return {
        "ok": True,
        "user": {
            "name": user["name"],
            "roll": user.get("roll", "—"),
            "email": user["email"],
            "role": user.get("role", "student").lower(),
            "dept": user.get("dept", "SAKEC"),
            "division": user.get("division", "—")
        }
    }

def add_user(name, roll, email, role, dept, division="", custom_pass=None):
    users = load_users()
    email_key = email.strip().lower()

    if not custom_pass:
        first_name = name.strip().split()[0].lower() if name.strip() else "sakec"
        first_name = "".join(c for c in first_name if c.isalnum())
        custom_pass = f"{first_name}@123"

    h, s = hash_password(custom_pass)
    user_obj = {
        "name": name.strip(),
        "roll": roll.strip().upper(),
        "email": email_key,
        "role": role.strip().lower(),
        "dept": dept.strip(),
        "division": division.strip(),
        "hash": h,
        "salt": s,
        "default_password": custom_pass,
        "created_at": time.time()
    }
    users[email_key] = user_obj

    if is_cloud_db_enabled():
        try:
            _sb_upsert_row("ev_users", email_key, user_obj)
        except Exception as e:
            _record_db_error("add_user", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    return users[email_key], custom_pass

def reset_user_password(email, new_password=None):
    users = load_users()
    email_key = email.strip().lower()
    if email_key not in users:
        return None, "User not found."

    u = users[email_key]
    if not new_password:
        first_name = u["name"].strip().split()[0].lower() if u["name"].strip() else "sakec"
        first_name = "".join(c for c in first_name if c.isalnum())
        new_password = f"{first_name}@123"

    h, s = hash_password(new_password)
    u["hash"] = h
    u["salt"] = s
    u["default_password"] = new_password

    if is_cloud_db_enabled():
        try:
            _sb_upsert_row("ev_users", email_key, u)
        except Exception as e:
            _record_db_error("reset_user_password", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)

    return new_password, None

def delete_user(email):
    users = load_users()
    email_key = email.strip().lower()
    if email_key in users and email_key != "admin@sakec.ac.in":
        del users[email_key]
        if is_cloud_db_enabled():
            try:
                _sb_delete_row("ev_users", email_key)
            except Exception as e:
                _record_db_error("delete_user", e)
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)
        return True
    return False

def bulk_upload_users_csv(csv_text, default_role="student"):
    lines = csv_text.strip().split("\n")
    created = 0
    details = []
    users = load_users()
    new_batch = {}

    for line in lines:
        parts = [p.strip() for p in line.split(",") if p.strip()]
        if not parts or parts[0].lower() in ["email", "email id", "roll", "roll no"]:
            continue

        if len(parts) >= 3:
            if "@" in parts[0]:
                email = parts[0]
                name = parts[1]
                dept = parts[2]
                roll = parts[3] if len(parts) > 3 else "—"
                div = parts[4] if len(parts) > 4 else "—"
            else:
                roll = parts[0]
                name = parts[1]
                email = parts[2]
                dept = parts[3] if len(parts) > 3 else "SAKEC"
                div = parts[4] if len(parts) > 4 else "—"

            email_key = email.strip().lower()
            first_name = name.strip().split()[0].lower() if name.strip() else "sakec"
            first_name = "".join(c for c in first_name if c.isalnum())
            custom_pass = f"{first_name}@123"
            h, s = hash_password(custom_pass)

            user_obj = {
                "name": name.strip(),
                "roll": roll.strip().upper(),
                "email": email_key,
                "role": default_role.strip().lower(),
                "dept": dept.strip(),
                "division": div.strip(),
                "hash": h,
                "salt": s,
                "default_password": custom_pass,
                "created_at": time.time()
            }
            users[email_key] = user_obj
            new_batch[email_key] = user_obj
            created += 1
            details.append({"email": email_key, "name": name, "roll": roll, "pass": custom_pass})

    if new_batch:
        if is_cloud_db_enabled():
            try:
                _sb_upsert_many("ev_users", new_batch)
            except Exception as e:
                _record_db_error("bulk_upload_users_csv", e)
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    return created, details

# =========================================================================
# SIMULATION PROGRESS & ASSESSMENT ENGINE
# =========================================================================

def _empty_records():
    return {
        "students": {},
        "metadata": {
            "college": "Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai",
            "faculty": "Dr. Rohan Borgalli"
        }
    }

def _normalize_students_dict(raw_students):
    normalized = {}
    for k, st_rec in (raw_students or {}).items():
        if not isinstance(st_rec, dict):
            continue
        em = str(st_rec.get("email") or k).strip().lower()
        if not em:
            continue
        rec_copy = dict(st_rec)
        rec_copy["email"] = em
        if "completed_modules" not in rec_copy or not isinstance(rec_copy["completed_modules"], dict):
            rec_copy["completed_modules"] = {}
        normalized[em] = rec_copy
    return normalized

def load_records():
    if is_cloud_db_enabled():
        try:
            cloud_students = _normalize_students_dict(_sb_fetch_all("ev_records"))
            records = _empty_records()
            if cloud_students:
                records["students"] = cloud_students
                return records
            if os.path.exists(RECORDS_FILE):
                try:
                    with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                        local_rec = json.load(f)
                    local_students = _normalize_students_dict(local_rec.get("students", {}))
                    if local_students:
                        _sb_upsert_many("ev_records", local_students)
                        records["students"] = local_students
                        return records
                except Exception:
                    pass
            return records
        except Exception as e:
            _record_db_error("load_records", e)

    if os.path.exists(RECORDS_FILE):
        try:
            with open(RECORDS_FILE, "r", encoding="utf-8") as f:
                local_rec = json.load(f)
            local_rec["students"] = _normalize_students_dict(local_rec.get("students", {}))
            return local_rec
        except Exception as e:
            print("Error loading records:", e)
    return _empty_records()

def save_records(records):
    clean_students = _normalize_students_dict(records.get("students", {}))
    records["students"] = clean_students
    if is_cloud_db_enabled():
        try:
            _sb_upsert_many("ev_records", clean_students)
        except Exception as e:
            _record_db_error("save_records", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(_sanitize_json(records), f, indent=2, ensure_ascii=False)

def complete_simulation(email, name, roll, dept, division, module_id, reflection, score, total_q=5, params=None):
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

    st_data = records["students"][email_key]
    prev_module_data = st_data["completed_modules"].get(module_id, {})
    prev_attempts = prev_module_data.get("attempts", 0)
    prev_best_score = prev_module_data.get("best_score", 0)

    # STRICT PASS THRESHOLD: Must get >= 3 of 5 correct (>= 60%)
    passed = (score >= 3)
    best_score = max(prev_best_score, score)

    st_data["completed_modules"][module_id] = {
        "completed": passed,
        "status": "COMPLETED" if passed else "RETRY_REQUIRED",
        "last_attempt_at": time.time(),
        "reflection": reflection.strip(),
        "quiz_score": int(score),
        "quiz_total": int(total_q),
        "quiz_percentage": round((score / total_q) * 100, 1),
        "best_score": int(best_score),
        "attempts": prev_attempts + 1,
        "parameters": _sanitize_json(params or {})
    }
    st_data["last_active"] = time.time()

    if is_cloud_db_enabled():
        try:
            _sb_upsert_row("ev_records", email_key, st_data)
        except Exception as e:
            _record_db_error("complete_simulation", e)

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(RECORDS_FILE, "w", encoding="utf-8") as f:
        json.dump(_sanitize_json(records), f, indent=2, ensure_ascii=False)

    return passed

def get_student_profile(email):
    records = load_records()
    return records["students"].get(email.strip().lower(), None)

def get_all_students_progress():
    records = load_records()
    users = load_users()
    students_map = records.get("students", {})

    students_list = []
    seen_emails = set()

    # 1. Include all enrolled students from ev_users (case-insensitive role check)
    for email, u in users.items():
        if str(u.get("role", "student")).strip().lower() != "student":
            continue

        em_key = email.strip().lower()
        seen_emails.add(em_key)
        st_record = students_map.get(em_key, {})
        comp = st_record.get("completed_modules", {})

        completed_modules_count = len([m for m in comp.values() if m.get("completed") is True])
        scores = [m.get("quiz_percentage", 0) for m in comp.values() if m.get("completed") is True]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        students_list.append({
            "roll": u.get("roll", st_record.get("roll", "—")),
            "name": u.get("name", st_record.get("name", "—")),
            "email": em_key,
            "dept": u.get("dept", st_record.get("dept", "—")),
            "division": u.get("division", st_record.get("division", "—")),
            "completed_count": completed_modules_count,
            "total_modules": 7,
            "completion_pct": round((completed_modules_count / 7) * 100, 1),
            "average_score": avg_score,
            "last_active": st_record.get("last_active", u.get("created_at", 0)),
            "modules": comp
        })

    # 2. Also include any student present in ev_records even if missing from ev_users
    for em_key, st_record in students_map.items():
        if em_key in seen_emails:
            continue
        u_rec = users.get(em_key, {})
        if u_rec and str(u_rec.get("role", "")).strip().lower() in ("admin", "faculty"):
            continue
        comp = st_record.get("completed_modules", {})
        completed_modules_count = len([m for m in comp.values() if m.get("completed") is True])
        scores = [m.get("quiz_percentage", 0) for m in comp.values() if m.get("completed") is True]
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        students_list.append({
            "roll": st_record.get("roll", "—"),
            "name": st_record.get("name", em_key),
            "email": em_key,
            "dept": st_record.get("dept", "—"),
            "division": st_record.get("division", "—"),
            "completed_count": completed_modules_count,
            "total_modules": 7,
            "completion_pct": round((completed_modules_count / 7) * 100, 1),
            "average_score": avg_score,
            "last_active": st_record.get("last_active", 0),
            "modules": comp
        })

    students_list.sort(key=lambda x: str(x["roll"]))
    return students_list

def export_master_excel(output_path):
    students = get_all_students_progress()
    wb = openpyxl.Workbook()

    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    green_fill = PatternFill(start_color="D1E7DD", end_color="D1E7DD", fill_type="solid")
    orange_fill = PatternFill(start_color="FFF3CD", end_color="FFF3CD", fill_type="solid")
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
    ws1["A2"] = "Electric Vehicle Engineering Simulation Platform — Class Progress Register (NBA Criterion 2.2.1)"
    ws1["A2"].font = bold_font
    ws1["A3"] = "Developed by Dr. Rohan Borgalli · Pass Rule: Minimum 3 of 5 Correct Answers Required"
    ws1["A3"].font = sub_font

    headers = [
        "Roll No", "Student Name", "Department", "Division",
        "Mod 1 (Dynamics)", "Mod 2 (Motors)", "Mod 3 (Battery)",
        "Mod 4 (Regen)", "Mod 5 (Charging)", "Mod 6 (Decarbon)",
        "Mod 7 (TCO)", "Completed / 7", "Avg Score (%)", "Overall Status"
    ]

    for col_idx, h in enumerate(headers, 1):
        cell = ws1.cell(row=5, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    row_num = 6
    module_keys = [f"module_{i}" for i in range(1, 8)]

    for st_item in students:
        ws1.cell(row=row_num, column=1, value=st_item["roll"]).font = bold_font
        ws1.cell(row=row_num, column=2, value=st_item["name"]).font = normal_font
        ws1.cell(row=row_num, column=3, value=st_item["dept"]).font = normal_font
        ws1.cell(row=row_num, column=4, value=st_item["division"]).font = normal_font

        for m_idx, m_key in enumerate(module_keys, 5):
            comp_data = st_item["modules"].get(m_key, {})
            is_comp = comp_data.get("completed", False)
            score = comp_data.get("quiz_score", 0)
            attempts = comp_data.get("attempts", 0)
            cell = ws1.cell(row=row_num, column=m_idx)
            if is_comp:
                cell.value = f"✓ Pass ({score}/5)"
                cell.fill = green_fill
                cell.font = Font(name="Calibri", size=9, color="0F5132", bold=True)
            elif attempts > 0:
                cell.value = f"✗ Retry ({score}/5)"
                cell.fill = orange_fill
                cell.font = Font(name="Calibri", size=9, color="856404")
            else:
                cell.value = "—"
                cell.font = Font(name="Calibri", size=9, color="888888")
            cell.alignment = Alignment(horizontal="center")

        ws1.cell(row=row_num, column=12, value=f"{st_item['completed_count']} / 7").alignment = Alignment(horizontal="center")
        ws1.cell(row=row_num, column=13, value=f"{st_item['average_score']}%").alignment = Alignment(horizontal="center")

        status_cell = ws1.cell(row=row_num, column=14)
        if st_item["completed_count"] == 7:
            status_cell.value = "ALL COMPLETED"
            status_cell.fill = green_fill
            status_cell.font = Font(name="Calibri", size=9.5, bold=True, color="0F5132")
        elif st_item["completed_count"] >= 4:
            status_cell.value = "IN PROGRESS"
            status_cell.fill = orange_fill
        else:
            status_cell.value = "PENDING"
        status_cell.alignment = Alignment(horizontal="center")

        for c in range(1, 15):
            ws1.cell(row=row_num, column=c).border = thin_border
        row_num += 1

    for col in ws1.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = max(max_len + 3, 13)

    # SHEET 2: Student Reflections Dossier
    ws2 = wb.create_sheet(title="Student_Reflections")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "STUDENT TECHNICAL REFLECTION DOSSIER"
    ws2["A1"].font = title_font
    ws2["A2"] = "Qualitative Engineering Observations Submitted per Module"
    ws2["A2"].font = sub_font

    ref_headers = ["Roll No", "Student Name", "Module", "Score (/5)", "Attempts", "Status", "Submitted Reflection"]
    for col_idx, h in enumerate(ref_headers, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = navy_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    ref_row = 5
    for st_item in students:
        for m_key, m_data in st_item["modules"].items():
            ws2.cell(row=ref_row, column=1, value=st_item["roll"]).font = bold_font
            ws2.cell(row=ref_row, column=2, value=st_item["name"]).font = normal_font
            ws2.cell(row=ref_row, column=3, value=m_key.replace("module_", "Module ")).font = normal_font
            ws2.cell(row=ref_row, column=4, value=f"{m_data.get('quiz_score', 0)}/5").alignment = Alignment(horizontal="center")
            ws2.cell(row=ref_row, column=5, value=m_data.get("attempts", 1)).alignment = Alignment(horizontal="center")

            stat_c = ws2.cell(row=ref_row, column=6, value=m_data.get("status", "—"))
            stat_c.alignment = Alignment(horizontal="center")
            if m_data.get("completed"):
                stat_c.fill = green_fill
            else:
                stat_c.fill = orange_fill

            ref_c = ws2.cell(row=ref_row, column=7, value=m_data.get("reflection", "—"))
            ref_c.alignment = Alignment(wrap_text=True)
            for c in range(1, 8):
                ws2.cell(row=ref_row, column=c).border = thin_border
            ref_row += 1

    ws2.column_dimensions["A"].width = 14
    ws2.column_dimensions["B"].width = 22
    ws2.column_dimensions["C"].width = 16
    ws2.column_dimensions["D"].width = 12
    ws2.column_dimensions["E"].width = 12
    ws2.column_dimensions["F"].width = 16
    ws2.column_dimensions["G"].width = 80

    wb.save(output_path)
    return output_path