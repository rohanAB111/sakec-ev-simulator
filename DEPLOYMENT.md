# SAKEC EV Simulation Platform — Cloud & Campus Deployment Guide

**Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai**  
*Developed by Dr. Rohan Borgalli*

---

## 🌐 Deployment Options

### Option 1: Render (Cloud PaaS with Public HTTPS) ⭐ *Recommended*

Deploying to Render takes ~5 minutes and provides a free public HTTPS URL (e.g. `https://sakec-ev-simulation.onrender.com`) accessible from smartphones on 4G/5G mobile networks.

1. **Push code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial release of SAKEC EV Simulation Platform"
   git branch -M main
   git remote add origin https://github.com/<your-username>/sakec-ev-platform.git
   git push -u origin main
   ```
2. **Deploy on Render:**
   * Go to [Render Dashboard](https://dashboard.render.com) and click **New +** → **Web Service**.
   * Connect your GitHub repository.
   * Configure settings:
     * **Environment:** `Python 3`
     * **Build Command:** `pip install -r requirements.txt`
     * **Start Command:** `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false`
   * Click **Create Web Service**.

---

### Option 2: Streamlit Community Cloud (Free & Direct)

1. Push your repository to GitHub.
2. Sign in to [share.streamlit.io](https://share.streamlit.io) using GitHub.
3. Click **New app**, select your repository, branch (`main`), and main file path (`app.py`).
4. Click **Deploy!** It will be live at `https://<your-app-name>.streamlit.app` in under 2 minutes.

---

### Option 3: SAKEC Campus Server / Lab Desktop (Local LAN & Wi-Fi)

1. On a campus lab machine (Ubuntu/Debian or Windows):
   ```bash
   git clone https://github.com/sakec/ev-platform.git /opt/sakec-ev
   cd /opt/sakec-ev
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Start Streamlit on campus port 8501:
   ```bash
   streamlit run app.py --server.port 8501 --server.address 0.0.0.0
   ```
3. Ask campus IT to point a DNS record (e.g., `ev-simulator.sakec.ac.in`) to the server IP.

---

## 🏢 Microsoft 365 & OneDrive Integration Setup (SAKEC IT Admin)

To enable automatic OneDrive report synchronization and Microsoft 365 Single Sign-On using your college subscription:

1. **Log in to [Microsoft Entra Admin Center](https://entra.microsoft.com)** with SAKEC administrator credentials.
2. Navigate to **Applications** → **App registrations** → **New registration**:
   * **Name:** `SAKEC EV Simulation Platform`
   * **Supported Account Types:** `Accounts in this organizational directory only (Single Tenant - SAKEC)`
   * **Redirect URI (Web):** `https://sakec-ev-simulation.onrender.com/` (or your production URL)
3. Under **API Permissions**, add Microsoft Graph delegated permissions:
   * `User.Read` (Sign in and read student/faculty profile)
   * `Files.ReadWrite` (Create folders and auto-save student portfolios and faculty reports to OneDrive)
   * `offline_access` (Maintain background sync access)
   * Click **Grant admin consent for SAKEC**.
4. Under **Certificates & secrets**, generate a new **Client Secret** and copy the value.
5. In your **Render Dashboard** (or server environment), set:
   * `MICROSOFT_CLIENT_ID` = `[Application (client) ID from Azure]`
   * `MICROSOFT_CLIENT_SECRET` = `[Client Secret Value]`
   * `MICROSOFT_TENANT_ID` = `[Directory (tenant) ID or common]`
6. **Result:**
   * Students and faculty can click **Sign in with Microsoft 365**.
   * Completed portfolios automatically back up to:
     `OneDrive / SAKEC_EV_Lab / My_EV_Simulation_Portfolio.pdf`
   * Faculty master progress gradebook automatically backs up to:
     `OneDrive / SAKEC_EV_Lab / SAKEC_EV_Simulation_Master_Register.xlsx`

---

Shah & Anchor Kutchhi Engineering College, Chembur, Mumbai  
**Developed by Dr. Rohan Borgalli**
