#!/usr/bin/env python3
"""
In-process tests using Flask's test client. This avoids needing the HTTP server to be bound to a port.
"""
import json
from app import app

print("=" * 70)
print("CareSync AI Assistant - Discharged Patient Portal (test client)")
print("=" * 70)

app.testing = True

with app.test_client() as client:
    # Test 1: home
    print("\n[1] GET / (home)")
    resp = client.get("/")
    print(f"    Status: {resp.status_code}")

    # Test 2: login form
    print("\n[2] GET /discharged-portal (login form)")
    resp = client.get("/discharged-portal")
    print(f"    Status: {resp.status_code}")
    if resp.status_code == 200:
        body = resp.get_data(as_text=True)
        if "Patient ID" in body or "phone" in body.lower():
            print("    OK - Login form contains expected fields")

    # Test 3: POST login (use seeded patient and follow redirects)
    print("\n[3] POST /discharged-portal (login)")
    login_resp = client.post(
        "/discharged-portal",
        data={"patient_id": "PAT000001", "phone": "555-688-7693"},
        follow_redirects=True,
    )
    print(f"    Status (after redirects): {login_resp.status_code}")

    # Check session store for discharged_patient_id
    with client.session_transaction() as sess:
        dp = sess.get('discharged_patient_id')
        print(f"    Session discharged_patient_id: {dp}")

    # Test 4: GET dashboard
    print("\n[4] GET /discharged-dashboard")
    d = client.get("/discharged-dashboard")
    print(f"    Status: {d.status_code}")
    if d.status_code == 200:
        b = d.get_data(as_text=True)
        if "CareSync" in b or "message" in b.lower():
            print("    OK - Dashboard contains chat UI")

    # Test 5: POST chat
    print("\n[5] POST /api/discharged/chat")
    chat = client.post(
        "/api/discharged/chat",
        json={"message": "Hello, how are you today?", "language": "en"},
    )
    print(f"    Status: {chat.status_code}")
    try:
        data = chat.get_json()
        print(f"    Response JSON keys: {list(data.keys()) if isinstance(data, dict) else type(data)}")
        if isinstance(data, dict) and "message" in data:
            print(f"    AI response (truncated): {data.get('message')[:150]}")
        elif isinstance(data, dict) and "error" in data:
            print(f"    Error: {data.get('error')}")
    except Exception:
        print(f"    Non-JSON response (len={len(chat.get_data())})")

print("\n" + "=" * 70)
print("In-process test complete")
print("=" * 70)
