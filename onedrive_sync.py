"""
SAKEC Electric Vehicle Simulation Platform — Microsoft 365 & OneDrive Sync Engine
Handles Microsoft Entra ID (Azure AD) OAuth 2.0 and Microsoft Graph API OneDrive Sync
Developed by Dr. Rohan Borgalli for Shah & Anchor Kutchhi Engineering College
"""

import os
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

MS_CLIENT_ID = os.getenv("MICROSOFT_CLIENT_ID", "")
MS_CLIENT_SECRET = os.getenv("MICROSOFT_CLIENT_SECRET", "")
MS_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID", "common")

GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"
OAUTH_AUTHORIZE_URL = f"https://login.microsoftonline.com/{MS_TENANT_ID}/oauth2/v2.0/authorize"
OAUTH_TOKEN_URL = f"https://login.microsoftonline.com/{MS_TENANT_ID}/oauth2/v2.0/token"

SCOPES = [
    "openid",
    "profile",
    "email",
    "User.Read",
    "Files.ReadWrite",
    "offline_access"
]

def is_configured():
    return bool(MS_CLIENT_ID and MS_CLIENT_SECRET)

def get_auth_url(redirect_uri):
    if not is_configured():
        return None
    scope_str = "%20".join(SCOPES)
    return (
        f"{OAUTH_AUTHORIZE_URL}?client_id={MS_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={requests.utils.quote(redirect_uri, safe='')}"
        f"&response_mode=query"
        f"&scope={scope_str}"
    )

def get_token_from_code(code, redirect_uri):
    if not is_configured():
        return None
    data = {
        "client_id": MS_CLIENT_ID,
        "client_secret": MS_CLIENT_SECRET,
        "code": code,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code",
        "scope": " ".join(SCOPES)
    }
    res = requests.post(OAUTH_TOKEN_URL, data=data)
    if res.status_code == 200:
        return res.json()
    return None

def get_user_profile(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(f"{GRAPH_API_ENDPOINT}/me", headers=headers)
    if res.status_code == 200:
        return res.json()
    return None

def upload_file_to_onedrive(access_token, file_bytes, filename, folder="SAKEC_EV_Lab"):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/octet-stream"
    }
    url = f"{GRAPH_API_ENDPOINT}/me/drive/root:/{folder}/{filename}:/content"
    res = requests.put(url, headers=headers, data=file_bytes)
    if res.status_code in [200, 201]:
        return {
            "success": True,
            "data": res.json(),
            "web_url": res.json().get("webUrl")
        }
    return {
        "success": False,
        "error": res.text,
        "status_code": res.status_code
    }
