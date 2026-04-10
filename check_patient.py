from app import app
from models import Patient

with app.app_context():
    p = Patient.query.filter_by(patient_id='PAT001').first()
    if not p:
        print('Patient PAT001 not found')
    else:
        print('Found:', p.patient_id)
        print('Phone:', p.phone)
        print('Status:', p.status)
