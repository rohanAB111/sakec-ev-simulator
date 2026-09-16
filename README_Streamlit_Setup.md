# How to Run the 15-Lecture Streamlit Classroom Simulation Platform

### Option A: Run Locally or on Classroom Lab PCs
1. Open Terminal or Command Prompt in this folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the web application:
   ```bash
   streamlit run app.py
   ```
   Your default web browser will automatically open with the platform!

### Option B: Local Network / Wi-Fi Classroom Host (All Students Connect via Phones/Laptops)
1. On the instructor's computer, execute:
   ```bash
   streamlit run app.py --server.address 0.0.0.0 --server.port 8501
   ```
2. Note your computer's local IP address (e.g., `192.168.1.50`).
3. Have students connect to the classroom Wi-Fi and open `http://192.168.1.50:8501` in their mobile browsers.

### Option C: Free Public Web Deployment (Streamlit Community Cloud)
1. Create a free GitHub repository (e.g., `sakec-ev-simulator`) and push `app.py` and `requirements.txt`.
2. Visit [share.streamlit.io](https://share.streamlit.io) and deploy the repository.
3. Share the permanent public URL (e.g., `https://sakec-ev.streamlit.app`) or display a QR code on the classroom projector screen. 60+ students can use it simultaneously with zero software installation!
