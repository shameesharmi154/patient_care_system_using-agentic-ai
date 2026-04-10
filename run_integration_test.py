import requests, time
BASE='http://127.0.0.1:5000'
s = requests.Session()
print('Logging in as PAT000001')
r = s.post(f'{BASE}/discharged-portal', data={'patient_id':'PAT000001','phone':'5556887693'}, timeout=5, allow_redirects=False)
print('POST login ->', r.status_code, 'Location:', r.headers.get('Location'))
r2 = s.get(f'{BASE}/discharged-dashboard', timeout=5)
print('GET dashboard ->', r2.status_code)
print('\nCalling chat endpoint...')
start = time.time()
r3 = s.post(f'{BASE}/api/discharged/chat', json={'message':'Hello from integration test','language':'en'}, timeout=30)
print('POST chat ->', r3.status_code, 'Time:', time.time()-start)
try:
    print('Response:', r3.json())
except Exception:
    print('Response text (truncated):', r3.text[:1000])
