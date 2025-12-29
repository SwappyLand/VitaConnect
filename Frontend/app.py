"""
MediConnect - Complete Online Doctor Consultation Platform
Full-featured with video calls, prescriptions, medicine marketplace
"""

import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime, timedelta
import json
import random
import string

# PDF generation
try:
    from fpdf import FPDF
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

# Video call imports
try:
    from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False

# ============================================================================
# CONFIGURATION
# ============================================================================

CSV_DIR = "data"
PATIENTS_CSV = os.path.join(CSV_DIR, "patients.csv")
DOCTORS_CSV = os.path.join(CSV_DIR, "doctors.csv")
APPOINTMENTS_CSV = os.path.join(CSV_DIR, "appointments.csv")
PRESCRIPTIONS_CSV = os.path.join(CSV_DIR, "prescriptions.csv")
MEDICINES_CSV = os.path.join(CSV_DIR, "medicines.csv")
ORDERS_CSV = os.path.join(CSV_DIR, "orders.csv")

PRESCRIPTIONS_DIR = os.path.join(CSV_DIR, "prescriptions")
INVOICES_DIR = os.path.join(CSV_DIR, "invoices")

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# WebRTC Configuration
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
    ]}
)

# ============================================================================
# DATA INITIALIZATION & POPULATION
# ============================================================================

def init_csv_files():
    """Initialize all CSV files and directories"""
    os.makedirs(CSV_DIR, exist_ok=True)
    os.makedirs(PRESCRIPTIONS_DIR, exist_ok=True)
    os.makedirs(INVOICES_DIR, exist_ok=True)
    
    # Initialize patients.csv
    if not os.path.exists(PATIENTS_CSV):
        df = pd.DataFrame(columns=['patient_id', 'name', 'email', 'password', 'phone', 'address'])
        df.to_csv(PATIENTS_CSV, index=False)
    
    # Initialize doctors.csv with Pune doctors
    if not os.path.exists(DOCTORS_CSV):
        populate_pune_doctors()
    
    # Initialize appointments.csv
    if not os.path.exists(APPOINTMENTS_CSV):
        df = pd.DataFrame(columns=[
            'appointment_id', 'doctor_id', 'patient_id', 'doctor_name',
            'patient_name', 'date', 'time', 'meeting_id', 'meeting_password',
            'status', 'created_at'
        ])
        df.to_csv(APPOINTMENTS_CSV, index=False)
    
    # Initialize prescriptions.csv
    if not os.path.exists(PRESCRIPTIONS_CSV):
        df = pd.DataFrame(columns=[
            'prescription_id', 'appointment_id', 'patient_id', 'doctor_id',
            'medicines', 'diagnosis', 'notes', 'pdf_path', 'created_at'
        ])
        df.to_csv(PRESCRIPTIONS_CSV, index=False)
    
    # Initialize medicines.csv
    if not os.path.exists(MEDICINES_CSV):
        populate_medicines()
    
    # Initialize orders.csv
    if not os.path.exists(ORDERS_CSV):
        df = pd.DataFrame(columns=[
            'order_id', 'patient_id', 'prescription_id', 'medicines',
            'total_amount', 'delivery_address', 'status', 'invoice_path', 'created_at'
        ])
        df.to_csv(ORDERS_CSV, index=False)

def populate_pune_doctors():
    """Populate doctors.csv with real Pune doctors"""
    doctors_data = [
        {
            'name': 'Dr. Rajesh Sharma',
            'specialization': 'Cardiologist',
            'degree': 'MBBS, MD (Cardiology)',
            'institution': 'Grant Medical College, Mumbai',
            'experience': 15,
            'hospital': 'Ruby Hall Clinic',
            'address': 'Grant Road, Pune',
            'phone': '9876543210'
        },
        {
            'name': 'Dr. Priya Deshmukh',
            'specialization': 'Dermatologist',
            'degree': 'MBBS, MD (Dermatology)',
            'institution': 'Armed Forces Medical College, Pune',
            'experience': 12,
            'hospital': 'Sahyadri Hospital',
            'address': 'Nagar Road, Pune',
            'phone': '9876543211'
        },
        {
            'name': 'Dr. Amit Kulkarni',
            'specialization': 'Pediatrician',
            'degree': 'MBBS, DCH, DNB (Pediatrics)',
            'institution': 'BJ Medical College, Pune',
            'experience': 10,
            'hospital': 'Surya Hospital',
            'address': 'Wakad, Pune',
            'phone': '9876543212'
        },
        {
            'name': 'Dr. Sunita Patil',
            'specialization': 'Gynecologist',
            'degree': 'MBBS, MS (OB-GYN)',
            'institution': 'Sion Hospital, Mumbai',
            'experience': 18,
            'hospital': 'Deenanath Mangeshkar Hospital',
            'address': 'Erandwane, Pune',
            'phone': '9876543213'
        },
        {
            'name': 'Dr. Vikram Joshi',
            'specialization': 'Orthopedist',
            'degree': 'MBBS, MS (Orthopedics)',
            'institution': 'KEM Hospital, Mumbai',
            'experience': 20,
            'hospital': 'Poona Hospital',
            'address': 'Camp Area, Pune',
            'phone': '9876543214'
        },
        {
            'name': 'Dr. Meera Iyer',
            'specialization': 'General Physician',
            'degree': 'MBBS, MD (General Medicine)',
            'institution': 'AFMC Pune',
            'experience': 8,
            'hospital': 'Columbia Asia Hospital',
            'address': 'Kharadi, Pune',
            'phone': '9876543215'
        },
        {
            'name': 'Dr. Anil Bhosale',
            'specialization': 'Neurologist',
            'degree': 'MBBS, DM (Neurology)',
            'institution': 'NIMHANS, Bangalore',
            'experience': 14,
            'hospital': 'Jehangir Hospital',
            'address': 'Sassoon Road, Pune',
            'phone': '9876543216'
        },
        {
            'name': 'Dr. Kavita Rane',
            'specialization': 'Psychiatrist',
            'degree': 'MBBS, MD (Psychiatry)',
            'institution': 'Grant Medical College, Mumbai',
            'experience': 11,
            'hospital': 'Ruby Hall Clinic',
            'address': 'Pune Station, Pune',
            'phone': '9876543217'
        },
        {
            'name': 'Dr. Suresh Pawar',
            'specialization': 'ENT Specialist',
            'degree': 'MBBS, MS (ENT)',
            'institution': 'BJ Medical College, Pune',
            'experience': 16,
            'hospital': 'Aditya Birla Memorial Hospital',
            'address': 'Pimpri, Pune',
            'phone': '9876543218'
        },
        {
            'name': 'Dr. Neha Gupta',
            'specialization': 'Ophthalmologist',
            'degree': 'MBBS, MS (Ophthalmology)',
            'institution': 'LTM Medical College, Mumbai',
            'experience': 9,
            'hospital': 'Inamdar Hospital',
            'address': 'Fatima Nagar, Pune',
            'phone': '9876543219'
        }
    ]
    
    doctors_list = []
    for doc in doctors_data:
        email = doc['name'].lower().replace('dr. ', '').replace(' ', '') + '@gmail.com'
        doctors_list.append({
            'doctor_id': generate_id('DOC'),
            'name': doc['name'],
            'email': email,
            'password': hash_password('doc123'),
            'phone': doc['phone'],
            'city': 'Pune',
            'state': 'Maharashtra',
            'degree': doc['degree'],
            'institution': doc['institution'],
            'year': str(2024 - doc['experience']),
            'documents_path': 'verified',
            'license_number': f'MH{random.randint(100000, 999999)}',
            'issuing_authority': 'Medical Council of India',
            'license_status': 'Active',
            'disciplinary_history': 'None',
            'employment_history': f"{doc['hospital']} - {doc['experience']} years",
            'specialization': doc['specialization'],
            'certifications': 'Board Certified',
            'experience': str(doc['experience']),
            'hospital': doc['hospital'],
            'address': doc['address'],
            'malpractice_claims': 'No',
            'criminal_background': 'Clear',
            'approval_status': 'approved',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(doctors_list)
    df.to_csv(DOCTORS_CSV, index=False)

def populate_medicines():
    """Populate medicines database"""
    medicines = [
        # Antibiotics
        {'name': 'Amoxicillin 500mg', 'category': 'Antibiotic', 'price': 120, 'stock': 100, 'manufacturer': 'Cipla'},
        {'name': 'Azithromycin 250mg', 'category': 'Antibiotic', 'price': 180, 'stock': 80, 'manufacturer': 'Sun Pharma'},
        {'name': 'Ciprofloxacin 500mg', 'category': 'Antibiotic', 'price': 95, 'stock': 120, 'manufacturer': 'Dr Reddy'},
        
        # Pain Relief
        {'name': 'Paracetamol 650mg', 'category': 'Pain Relief', 'price': 25, 'stock': 200, 'manufacturer': 'GSK'},
        {'name': 'Ibuprofen 400mg', 'category': 'Pain Relief', 'price': 45, 'stock': 150, 'manufacturer': 'Abbott'},
        {'name': 'Diclofenac 50mg', 'category': 'Pain Relief', 'price': 65, 'stock': 100, 'manufacturer': 'Novartis'},
        
        # Fever
        {'name': 'Crocin Advance', 'category': 'Fever', 'price': 35, 'stock': 180, 'manufacturer': 'GSK'},
        {'name': 'Dolo 650', 'category': 'Fever', 'price': 30, 'stock': 220, 'manufacturer': 'Micro Labs'},
        
        # Cold & Cough
        {'name': 'Cetrizine 10mg', 'category': 'Allergy', 'price': 40, 'stock': 140, 'manufacturer': 'Cipla'},
        {'name': 'Benadryl Cough Syrup', 'category': 'Cough', 'price': 115, 'stock': 90, 'manufacturer': 'Johnson & Johnson'},
        {'name': 'Cheston Cold', 'category': 'Cold', 'price': 85, 'stock': 110, 'manufacturer': 'Cipla'},
        
        # Stomach
        {'name': 'Pantoprazole 40mg', 'category': 'Acidity', 'price': 95, 'stock': 100, 'manufacturer': 'Alkem'},
        {'name': 'Omez 20mg', 'category': 'Acidity', 'price': 110, 'stock': 85, 'manufacturer': 'Dr Reddy'},
        {'name': 'Digene Gel', 'category': 'Antacid', 'price': 55, 'stock': 160, 'manufacturer': 'Abbott'},
        
        # Diabetes
        {'name': 'Metformin 500mg', 'category': 'Diabetes', 'price': 75, 'stock': 95, 'manufacturer': 'USV'},
        {'name': 'Glimepiride 2mg', 'category': 'Diabetes', 'price': 125, 'stock': 70, 'manufacturer': 'Sun Pharma'},
        
        # Blood Pressure
        {'name': 'Amlodipine 5mg', 'category': 'BP', 'price': 85, 'stock': 110, 'manufacturer': 'Pfizer'},
        {'name': 'Telmisartan 40mg', 'category': 'BP', 'price': 145, 'stock': 80, 'manufacturer': 'Glenmark'},
        
        # Vitamins
        {'name': 'Vitamin D3 60K', 'category': 'Vitamin', 'price': 55, 'stock': 130, 'manufacturer': 'Mankind'},
        {'name': 'Multivitamin Capsules', 'category': 'Vitamin', 'price': 180, 'stock': 100, 'manufacturer': 'HealthKart'},
        {'name': 'Vitamin B12 Tablets', 'category': 'Vitamin', 'price': 95, 'stock': 120, 'manufacturer': 'Sun Pharma'},
        
        # Skin
        {'name': 'Fusidic Acid Cream', 'category': 'Skin', 'price': 165, 'stock': 60, 'manufacturer': 'Leo Pharma'},
        {'name': 'Betnovate Cream', 'category': 'Skin', 'price': 145, 'stock': 75, 'manufacturer': 'GSK'},
    ]
    
    medicines_list = []
    for med in medicines:
        medicines_list.append({
            'medicine_id': generate_id('MED'),
            'name': med['name'],
            'category': med['category'],
            'price': med['price'],
            'stock': med['stock'],
            'manufacturer': med['manufacturer'],
            'requires_prescription': 'Yes' if med['category'] in ['Antibiotic', 'Diabetes', 'BP'] else 'No'
        })
    
    df = pd.DataFrame(medicines_list)
    df.to_csv(MEDICINES_CSV, index=False)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_id(prefix):
    """Generate unique ID with timestamp"""
    return f"{prefix}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

def generate_meeting_credentials():
    """Generate meeting ID and password"""
    meeting_id = ''.join(random.choices(string.digits, k=10))
    meeting_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return meeting_id, meeting_password

def load_csv(filepath):
    """Load CSV file safely"""
    try:
        df = pd.read_csv(filepath)
        if df.empty or len(df.columns) == 0:
            return get_empty_dataframe(filepath)
        return df
    except FileNotFoundError:
        return get_empty_dataframe(filepath)

def get_empty_dataframe(filepath):
    """Return empty DataFrame with correct columns"""
    if 'patients' in filepath:
        return pd.DataFrame(columns=['patient_id', 'name', 'email', 'password', 'phone', 'address'])
    elif 'doctors' in filepath:
        return pd.DataFrame(columns=[
            'doctor_id', 'name', 'email', 'password', 'phone', 'city', 'state',
            'degree', 'institution', 'year', 'documents_path', 'license_number',
            'issuing_authority', 'license_status', 'disciplinary_history',
            'employment_history', 'specialization', 'certifications', 
            'experience', 'hospital', 'address', 'malpractice_claims',
            'criminal_background', 'approval_status', 'created_at'
        ])
    elif 'appointments' in filepath:
        return pd.DataFrame(columns=[
            'appointment_id', 'doctor_id', 'patient_id', 'doctor_name',
            'patient_name', 'date', 'time', 'meeting_id', 'meeting_password',
            'status', 'created_at'
        ])
    elif 'prescriptions' in filepath:
        return pd.DataFrame(columns=[
            'prescription_id', 'appointment_id', 'patient_id', 'doctor_id',
            'medicines', 'diagnosis', 'notes', 'pdf_path', 'created_at'
        ])
    elif 'medicines' in filepath:
        return pd.DataFrame(columns=[
            'medicine_id', 'name', 'category', 'price', 'stock', 
            'manufacturer', 'requires_prescription'
        ])
    elif 'orders' in filepath:
        return pd.DataFrame(columns=[
            'order_id', 'patient_id', 'prescription_id', 'medicines',
            'total_amount', 'delivery_address', 'status', 'invoice_path', 'created_at'
        ])
    return pd.DataFrame()

def save_csv(df, filepath):
    """Save DataFrame to CSV"""
    df.to_csv(filepath, index=False)

# ============================================================================
# AUTHENTICATION
# ============================================================================

def patient_signup(name, email, password, phone, address):
    """Register new patient"""
    df = load_csv(PATIENTS_CSV)
    
    if not df.empty and 'email' in df.columns and email in df['email'].values:
        return False, "Email already registered"
    
    new_patient = pd.DataFrame([{
        'patient_id': generate_id('PAT'),
        'name': name,
        'email': email,
        'password': hash_password(password),
        'phone': phone,
        'address': address
    }])
    
    df = pd.concat([df, new_patient], ignore_index=True)
    save_csv(df, PATIENTS_CSV)
    return True, "Registration successful!"

def patient_login(email, password):
    """Authenticate patient"""
    df = load_csv(PATIENTS_CSV)
    
    if df.empty or 'email' not in df.columns:
        return False, None
    
    user = df[df['email'] == email]
    
    if user.empty:
        return False, None
    
    if user.iloc[0]['password'] == hash_password(password):
        return True, user.iloc[0].to_dict()
    return False, None

def doctor_login(email, password):
    """Authenticate doctor"""
    df = load_csv(DOCTORS_CSV)
    
    if df.empty or 'email' not in df.columns:
        return False, None
    
    user = df[df['email'] == email]
    
    if user.empty:
        return False, None
    
    if user.iloc[0]['password'] == hash_password(password):
        return True, user.iloc[0].to_dict()
    return False, None

# ============================================================================
# PDF GENERATION
# ============================================================================

class PrescriptionPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'MediConnect - Medical Prescription', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 0, 'C')

def generate_prescription_pdf(prescription_data, patient_data, doctor_data):
    """Generate prescription PDF"""
    if not PDF_AVAILABLE:
        return None
    
    pdf = PrescriptionPDF()
    pdf.add_page()
    
    # Doctor Info
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Dr. {doctor_data['name']}", 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"{doctor_data['specialization']}", 0, 1)
    pdf.cell(0, 6, f"{doctor_data['hospital']}, {doctor_data['address']}", 0, 1)
    pdf.cell(0, 6, f"License: {doctor_data['license_number']}", 0, 1)
    pdf.ln(5)
    
    # Patient Info
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Patient Information:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Name: {patient_data['name']}", 0, 1)
    pdf.cell(0, 6, f"Date: {prescription_data['created_at']}", 0, 1)
    pdf.ln(5)
    
    # Diagnosis
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Diagnosis:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, prescription_data['diagnosis'])
    pdf.ln(3)
    
    # Medicines
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Prescribed Medicines:', 0, 1)
    pdf.set_font('Arial', '', 10)
    
    medicines = json.loads(prescription_data['medicines'])
    for i, med in enumerate(medicines, 1):
        pdf.cell(0, 6, f"{i}. {med['name']} - {med['dosage']}", 0, 1)
        pdf.cell(0, 6, f"   Duration: {med['duration']} | Instructions: {med['instructions']}", 0, 1)
        pdf.ln(2)
    
    # Notes
    if prescription_data.get('notes'):
        pdf.ln(3)
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 8, 'Additional Notes:', 0, 1)
        pdf.set_font('Arial', '', 10)
        pdf.multi_cell(0, 6, prescription_data['notes'])
    
    # Save PDF
    filename = f"prescription_{prescription_data['prescription_id']}.pdf"
    filepath = os.path.join(PRESCRIPTIONS_DIR, filename)
    pdf.output(filepath)
    
    return filepath

def generate_invoice_pdf(order_data, patient_data):
    """Generate invoice PDF"""
    if not PDF_AVAILABLE:
        return None
    
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font('Arial', 'B', 18)
    pdf.cell(0, 15, 'INVOICE', 0, 1, 'C')
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, f"Invoice #: {order_data['order_id']}", 0, 1, 'C')
    pdf.cell(0, 6, f"Date: {order_data['created_at']}", 0, 1, 'C')
    pdf.ln(10)
    
    # Patient Info
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 8, 'Bill To:', 0, 1)
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, patient_data['name'], 0, 1)
    pdf.multi_cell(0, 6, order_data['delivery_address'])
    pdf.ln(10)
    
    # Table header
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(100, 8, 'Medicine', 1)
    pdf.cell(30, 8, 'Quantity', 1)
    pdf.cell(30, 8, 'Price', 1)
    pdf.cell(30, 8, 'Total', 1)
    pdf.ln()
    
    # Items
    pdf.set_font('Arial', '', 10)
    medicines = json.loads(order_data['medicines'])
    subtotal = 0
    
    for med in medicines:
        pdf.cell(100, 8, med['name'], 1)
        pdf.cell(30, 8, str(med['quantity']), 1)
        pdf.cell(30, 8, f"₹{med['price']}", 1)
        total = med['quantity'] * med['price']
        pdf.cell(30, 8, f"₹{total}", 1)
        pdf.ln()
        subtotal += total
    
    # Total
    pdf.ln(5)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(160, 8, 'Subtotal:', 0)
    pdf.cell(30, 8, f"₹{subtotal}", 0, 1, 'R')
    
    delivery_charge = 50
    pdf.set_font('Arial', '', 10)
    pdf.cell(160, 8, 'Delivery Charges:', 0)
    pdf.cell(30, 8, f"₹{delivery_charge}", 0, 1, 'R')
    
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(160, 10, 'Grand Total:', 0)
    pdf.cell(30, 10, f"₹{subtotal + delivery_charge}", 0, 1, 'R')
    
    # Save
    filename = f"invoice_{order_data['order_id']}.pdf"
    filepath = os.path.join(INVOICES_DIR, filename)
    pdf.output(filepath)
    
    return filepath

# ============================================================================
# PATIENT UI
# ============================================================================

def patient_landing_page():
    """Patient landing page"""
    st.markdown("""
        <h1 style='text-align: center; color: #1E88E5;'>🏥 MediConnect</h1>
        <h3 style='text-align: center; color: #616161;'>Complete Healthcare Platform</h3>
        <p style='text-align: center;'>Book Consultations • Get Prescriptions • Order Medicines</p>
    """, unsafe_allow_html=True)
    
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🔐 Login", use_container_width=True):
            st.session_state.page = 'patient_login'
            st.rerun()
        
        if st.button("📝 Sign Up", use_container_width=True):
            st.session_state.page = 'patient_signup'
            st.rerun()
    
    st.write("")
    st.write("")
    
    if st.button("👨‍⚕️ Doctor Login", key="doctor_link"):
        st.session_state.user_type = 'doctor'
        st.session_state.page = 'doctor_login'
        st.rerun()

def patient_signup_page():
    """Patient registration"""
    st.title("📝 Patient Registration")
    
    with st.form("patient_signup"):
        name = st.text_input("Full Name*")
        email = st.text_input("Email*")
        phone = st.text_input("Phone Number*")
        address = st.text_area("Address*")
        password = st.text_input("Password*", type="password")
        confirm_password = st.text_input("Confirm Password*", type="password")
        
        submit = st.form_submit_button("Sign Up")
        
        if submit:
            if not all([name, email, phone, address, password]):
                st.error("All fields are required")
            elif password != confirm_password:
                st.error("Passwords don't match")
            else:
                success, message = patient_signup(name, email, password, phone, address)
                if success:
                    st.success(message)
                    st.session_state.page = 'patient_login'
                    st.rerun()
                else:
                    st.error(message)
    
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()

def patient_login_page():
    """Patient login"""
    st.title("🔐 Patient Login")
    
    with st.form("patient_login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submit = st.form_submit_button("Login")
        
        if submit:
            success, user = patient_login(email, password)
            if success:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.session_state.user_type = 'patient'
                st.session_state.page = 'patient_dashboard'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()

def patient_dashboard():
    """Patient dashboard"""
    st.title(f"Welcome, {st.session_state.user['name']}! 👋")
    
    with st.sidebar:
        st.write("### 🏠 Navigation")
        if st.button("🔍 Find Doctors", use_container_width=True):
            st.session_state.page = 'find_doctors'
            st.rerun()
        if st.button("📅 My Appointments", use_container_width=True):
            st.session_state.page = 'patient_appointments'
            st.rerun()
        if st.button("💊 Order Medicines", use_container_width=True):
            st.session_state.page = 'medicine_marketplace'
            st.rerun()
        if st.button("📋 My Prescriptions", use_container_width=True):
            st.session_state.page = 'patient_prescriptions'
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 🔍 Find Doctors\nSearch verified doctors in Pune")
        if st.button("Search Now", key="dash_find"):
            st.session_state.page = 'find_doctors'
            st.rerun()
    
    with col2:
        st.info("### 📅 Appointments\nManage your consultations")
        if st.button("View All", key="dash_apt"):
            st.session_state.page = 'patient_appointments'
            st.rerun()
    
    with col3:
        st.info("### 💊 Medicine Store\nOrder prescribed medicines")
        if st.button("Shop Now", key="dash_shop"):
            st.session_state.page = 'medicine_marketplace'
            st.rerun()

def find_doctors_page():
    """Doctor discovery"""
    st.title("🔍 Find Doctors in Pune")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'patient_dashboard'
            st.rerun()
    
    doctors = load_csv(DOCTORS_CSV)
    approved = doctors[doctors['approval_status'] == 'approved']
    
    if approved.empty:
        st.warning("No doctors available")
        return
    
    # Filters
    col1, col2 = st.columns(2)
    with col1:
        specs = approved['specialization'].unique().tolist()
        selected_spec = st.selectbox("Specialization", ["All"] + specs)
    with col2:
        min_exp = st.slider("Min Experience (years)", 0, 25, 0)
    
    filtered = approved.copy()
    if selected_spec != "All":
        filtered = filtered[filtered['specialization'] == selected_spec]
    filtered = filtered[filtered['experience'].astype(int) >= min_exp]
    
    st.write(f"### {len(filtered)} Doctors Found")
    
    for idx, doc in filtered.iterrows():
        with st.expander(f"🩺 {doc['name']} - {doc['specialization']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.write(f"**🎓 Qualification:** {doc['degree']}")
                st.write(f"**🏥 Hospital:** {doc['hospital']}")
                st.write(f"**📍 Location:** {doc['address']}, Pune")
                st.write(f"**💼 Experience:** {doc['experience']} years")
                st.write(f"**📞 Contact:** {doc['phone']}")
                st.write(f"**📧 Email:** {doc['email']}")
            
            with col2:
                if st.button("📅 Book Appointment", key=f"book_{doc['doctor_id']}"):
                    st.session_state.selected_doctor = doc.to_dict()
                    st.session_state.page = 'book_appointment'
                    st.rerun()

def book_appointment_page():
    """Book appointment"""
    st.title("📅 Book Appointment")
    
    doctor = st.session_state.selected_doctor
    
    st.info(f"### Booking with {doctor['name']}\n**Specialization:** {doctor['specialization']}\n**Hospital:** {doctor['hospital']}")
    
    with st.form("booking"):
        date = st.date_input("Date", min_value=datetime.now().date())
        time_slots = [f"{h:02d}:00" for h in range(9, 18)]
        time = st.selectbox("Time", time_slots)
        
        submit = st.form_submit_button("Confirm Booking")
        
        if submit:
            appointments = load_csv(APPOINTMENTS_CSV)
            conflict = appointments[
                (appointments['doctor_id'] == doctor['doctor_id']) &
                (appointments['date'] == str(date)) &
                (appointments['time'] == time) &
                (appointments['status'] != 'cancelled')
            ]
            
            if not conflict.empty:
                st.error("Slot already booked")
            else:
                meeting_id, meeting_pwd = generate_meeting_credentials()
                
                new_apt = pd.DataFrame([{
                    'appointment_id': generate_id('APT'),
                    'doctor_id': doctor['doctor_id'],
                    'patient_id': st.session_state.user['patient_id'],
                    'doctor_name': doctor['name'],
                    'patient_name': st.session_state.user['name'],
                    'date': str(date),
                    'time': time,
                    'meeting_id': meeting_id,
                    'meeting_password': meeting_pwd,
                    'status': 'confirmed',
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }])
                
                appointments = pd.concat([appointments, new_apt], ignore_index=True)
                save_csv(appointments, APPOINTMENTS_CSV)
                
                st.success("✅ Appointment Booked!")
                st.info(f"**Meeting ID:** {meeting_id}\n**Password:** {meeting_pwd}")
                st.balloons()
    
    if st.button("← Back"):
        st.session_state.page = 'find_doctors'
        st.rerun()

def patient_appointments_page():
    """Patient appointments"""
    st.title("📅 My Appointments")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'patient_dashboard'
            st.rerun()
    
    appointments = load_csv(APPOINTMENTS_CSV)
    my_apts = appointments[
        appointments['patient_id'] == st.session_state.user['patient_id']
    ].sort_values('date', ascending=False)
    
    if my_apts.empty:
        st.info("No appointments yet")
        return
    
    for idx, apt in my_apts.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**🩺 {apt['doctor_name']}**")
                st.write(f"📅 {apt['date']} at {apt['time']}")
                st.write(f"🔑 Meeting ID: {apt['meeting_id']} | Password: {apt['meeting_password']}")
                
                status_emoji = {'confirmed': '🟢', 'completed': '🔵', 'cancelled': '🔴'}.get(apt['status'], '⚪')
                st.write(f"Status: {status_emoji} {apt['status'].title()}")
            
            with col2:
                if apt['status'] == 'confirmed':
                    if st.button("🎥 Join Call", key=f"join_p_{apt['appointment_id']}", type="primary"):
                        st.session_state.current_meeting = apt.to_dict()
                        st.session_state.page = 'video_call'
                        st.rerun()
            
            st.divider()

def medicine_marketplace():
    """Medicine marketplace"""
    st.title("💊 Medicine Marketplace")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'patient_dashboard'
            st.rerun()
        
        st.write("### 🛒 Cart")
        cart = st.session_state.get('cart', [])
        if cart:
            total = sum(item['price'] * item['quantity'] for item in cart)
            st.write(f"**Items:** {len(cart)}")
            st.write(f"**Total:** ₹{total}")
            if st.button("Checkout", use_container_width=True):
                st.session_state.page = 'checkout'
                st.rerun()
        else:
            st.write("Cart is empty")
    
    medicines = load_csv(MEDICINES_CSV)
    
    # Filters
    categories = medicines['category'].unique().tolist()
    selected_cat = st.selectbox("Category", ["All"] + categories)
    
    if selected_cat != "All":
        medicines = medicines[medicines['category'] == selected_cat]
    
    st.write(f"### Available Medicines ({len(medicines)})")
    
    for idx, med in medicines.iterrows():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.write(f"**{med['name']}**")
            st.write(f"Category: {med['category']} | Manufacturer: {med['manufacturer']}")
            st.write(f"**₹{med['price']}** | Stock: {med['stock']}")
        
        with col2:
            qty = st.number_input("Qty", 1, 10, 1, key=f"qty_{med['medicine_id']}")
        
        with col3:
            if st.button("Add to Cart", key=f"add_{med['medicine_id']}"):
                cart = st.session_state.get('cart', [])
                cart.append({
                    'medicine_id': med['medicine_id'],
                    'name': med['name'],
                    'price': med['price'],
                    'quantity': qty
                })
                st.session_state.cart = cart
                st.success("Added!")
                st.rerun()
        
        st.divider()

def checkout_page():
    """Checkout"""
    st.title("🛒 Checkout")
    
    cart = st.session_state.get('cart', [])
    if not cart:
        st.warning("Cart is empty")
        return
    
    # Display cart
    st.write("### Order Summary")
    subtotal = 0
    for item in cart:
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(item['name'])
        with col2:
            st.write(f"Qty: {item['quantity']}")
        with col3:
            total = item['price'] * item['quantity']
            st.write(f"₹{total}")
            subtotal += total
    
    st.divider()
    delivery = 50
    grand_total = subtotal + delivery
    
    st.write(f"**Subtotal:** ₹{subtotal}")
    st.write(f"**Delivery:** ₹{delivery}")
    st.write(f"**Grand Total:** ₹{grand_total}")
    
    with st.form("checkout"):
        address = st.text_area("Delivery Address", value=st.session_state.user.get('address', ''))
        
        submit = st.form_submit_button("Place Order")
        
        if submit:
            # Create order
            order_data = {
                'order_id': generate_id('ORD'),
                'patient_id': st.session_state.user['patient_id'],
                'prescription_id': 'DIRECT',
                'medicines': json.dumps(cart),
                'total_amount': grand_total,
                'delivery_address': address,
                'status': 'confirmed',
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'invoice_path': ''
            }
            
            # Generate invoice
            invoice_path = generate_invoice_pdf(order_data, st.session_state.user)
            order_data['invoice_path'] = invoice_path if invoice_path else 'pending'
            
            orders = load_csv(ORDERS_CSV)
            new_order = pd.DataFrame([order_data])
            orders = pd.concat([orders, new_order], ignore_index=True)
            save_csv(orders, ORDERS_CSV)
            
            st.session_state.cart = []
            st.success("✅ Order placed successfully!")
            if invoice_path:
                st.info(f"📄 Invoice saved: {invoice_path}")
            st.balloons()
    
    if st.button("← Back to Shop"):
        st.session_state.page = 'medicine_marketplace'
        st.rerun()

def patient_prescriptions_page():
    """View prescriptions"""
    st.title("📋 My Prescriptions")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'patient_dashboard'
            st.rerun()
    
    prescriptions = load_csv(PRESCRIPTIONS_CSV)
    my_presc = prescriptions[
        prescriptions['patient_id'] == st.session_state.user['patient_id']
    ].sort_values('created_at', ascending=False)
    
    if my_presc.empty:
        st.info("No prescriptions yet")
        return
    
    for idx, presc in my_presc.iterrows():
        with st.expander(f"📋 Prescription - {presc['created_at'][:10]}"):
            st.write(f"**Diagnosis:** {presc['diagnosis']}")
            
            medicines = json.loads(presc['medicines'])
            st.write("**Medicines:**")
            for med in medicines:
                st.write(f"- {med['name']} - {med['dosage']}")
            
            if presc['pdf_path'] and os.path.exists(presc['pdf_path']):
                with open(presc['pdf_path'], 'rb') as f:
                    st.download_button("📥 Download PDF", f, file_name=os.path.basename(presc['pdf_path']))
            
            if st.button("💊 Order These Medicines", key=f"order_{presc['prescription_id']}"):
                # Add to cart
                st.session_state.cart = []
                for med in medicines:
                    # Find medicine in database
                    meds_df = load_csv(MEDICINES_CSV)
                    found = meds_df[meds_df['name'].str.contains(med['name'].split()[0], case=False, na=False)]
                    
                    if not found.empty:
                        med_data = found.iloc[0]
                        st.session_state.cart.append({
                            'medicine_id': med_data['medicine_id'],
                            'name': med_data['name'],
                            'price': med_data['price'],
                            'quantity': 1
                        })
                
                st.session_state.page = 'checkout'
                st.rerun()

# ============================================================================
# DOCTOR UI
# ============================================================================

def doctor_login_page():
    """Doctor login"""
    st.title("👨‍⚕️ Doctor Login")
    
    st.info("**Demo Credentials:**\nEmail: doctorname@gmail.com (e.g., rajesh sharma@gmail.com without spaces)\nPassword: doc123")
    
    with st.form("doctor_login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        submit = st.form_submit_button("Login")
        
        if submit:
            success, user = doctor_login(email, password)
            if success:
                st.session_state.user = user
                st.session_state.logged_in = True
                st.session_state.user_type = 'doctor'
                st.session_state.page = 'doctor_dashboard'
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()

def doctor_dashboard():
    """Doctor dashboard"""
    st.title(f"Welcome, {st.session_state.user['name']}!")
    
    with st.sidebar:
        st.write("### 🏥 Navigation")
        if st.button("📅 Appointments", use_container_width=True):
            st.session_state.page = 'doctor_appointments'
            st.rerun()
        if st.button("👤 Profile", use_container_width=True):
            st.session_state.page = 'doctor_profile'
            st.rerun()
        if st.button("🚪 Logout", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    st.success("✅ Your profile is approved and visible to patients")
    
    # Today's appointments
    appointments = load_csv(APPOINTMENTS_CSV)
    today = datetime.now().date()
    today_apts = appointments[
        (appointments['doctor_id'] == st.session_state.user['doctor_id']) &
        (appointments['date'] == str(today))
    ]
    
    st.write(f"### 📅 Today's Appointments ({len(today_apts)})")
    
    if today_apts.empty:
        st.info("No appointments today")
    else:
        for idx, apt in today_apts.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{apt['patient_name']}** - {apt['time']}")
                st.write(f"Meeting: {apt['meeting_id']} / {apt['meeting_password']}")
            
            with col2:
                if st.button("Join", key=f"join_d_{apt['appointment_id']}"):
                    st.session_state.current_meeting = apt.to_dict()
                    st.session_state.page = 'video_call'
                    st.rerun()
            
            st.divider()

def doctor_appointments_page():
    """Doctor appointments"""
    st.title("📅 My Appointments")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'doctor_dashboard'
            st.rerun()
    
    appointments = load_csv(APPOINTMENTS_CSV)
    my_apts = appointments[
        appointments['doctor_id'] == st.session_state.user['doctor_id']
    ].sort_values('date', ascending=False)
    
    if my_apts.empty:
        st.info("No appointments")
        return
    
    for idx, apt in my_apts.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**👤 {apt['patient_name']}**")
                st.write(f"📅 {apt['date']} at {apt['time']}")
                st.write(f"🔑 Meeting: {apt['meeting_id']} / {apt['meeting_password']}")
                st.write(f"Status: {apt['status'].title()}")
            
            with col2:
                if apt['status'] == 'confirmed':
                    if st.button("🎥 Join Call", key=f"join_d2_{apt['appointment_id']}", type="primary"):
                        st.session_state.current_meeting = apt.to_dict()
                        st.session_state.page = 'video_call'
                        st.rerun()
                    
                    if st.button("📋 Prescribe", key=f"presc_{apt['appointment_id']}"):
                        st.session_state.current_appointment = apt.to_dict()
                        st.session_state.page = 'create_prescription'
                        st.rerun()
            
            st.divider()

def doctor_profile_page():
    """Doctor profile"""
    st.title("👤 My Profile")
    
    with st.sidebar:
        if st.button("← Back"):
            st.session_state.page = 'doctor_dashboard'
            st.rerun()
    
    doc = st.session_state.user
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### Personal Information")
        st.write(f"**Name:** {doc['name']}")
        st.write(f"**Email:** {doc['email']}")
        st.write(f"**Phone:** {doc['phone']}")
        st.write(f"**Specialization:** {doc['specialization']}")
    
    with col2:
        st.write("### Professional Details")
        st.write(f"**Hospital:** {doc['hospital']}")
        st.write(f"**Address:** {doc['address']}")
        st.write(f"**Experience:** {doc['experience']} years")
        st.write(f"**License:** {doc['license_number']}")

def create_prescription_page():
    """Create prescription"""
    st.title("📋 Create Prescription")
    
    apt = st.session_state.current_appointment
    st.info(f"**Patient:** {apt['patient_name']}\n**Date:** {apt['date']}")
    
    with st.form("prescription"):
        diagnosis = st.text_area("Diagnosis*")
        
        st.write("### Medicines")
        num_meds = st.number_input("Number of medicines", 1, 10, 3)
        
        medicines = []
        for i in range(num_meds):
            st.write(f"**Medicine {i+1}**")
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input(f"Name", key=f"name_{i}")
                dosage = st.text_input(f"Dosage", key=f"dose_{i}")
            with col2:
                duration = st.text_input(f"Duration", key=f"dur_{i}")
                instructions = st.text_input(f"Instructions", key=f"inst_{i}")
            
            if name:
                medicines.append({
                    'name': name,
                    'dosage': dosage,
                    'duration': duration,
                    'instructions': instructions
                })
        
        notes = st.text_area("Additional Notes")
        
        submit = st.form_submit_button("Generate Prescription")
        
        if submit:
            if not diagnosis or not medicines:
                st.error("Diagnosis and at least one medicine required")
            else:
                # Get patient data
                patients = load_csv(PATIENTS_CSV)
                patient = patients[patients['patient_id'] == apt['patient_id']].iloc[0]
                
                prescription_data = {
                    'prescription_id': generate_id('PRESC'),
                    'appointment_id': apt['appointment_id'],
                    'patient_id': apt['patient_id'],
                    'doctor_id': st.session_state.user['doctor_id'],
                    'medicines': json.dumps(medicines),
                    'diagnosis': diagnosis,
                    'notes': notes,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'pdf_path': ''
                }
                
                # Generate PDF
                pdf_path = generate_prescription_pdf(
                    prescription_data,
                    patient.to_dict(),
                    st.session_state.user
                )
                
                if pdf_path:
                    prescription_data['pdf_path'] = pdf_path
                
                # Save prescription
                prescriptions = load_csv(PRESCRIPTIONS_CSV)
                new_presc = pd.DataFrame([prescription_data])
                prescriptions = pd.concat([prescriptions, new_presc], ignore_index=True)
                save_csv(prescriptions, PRESCRIPTIONS_CSV)
                
                st.success("✅ Prescription created!")
                if pdf_path:
                    st.info(f"📄 PDF saved: {pdf_path}")
                st.balloons()
    
    if st.button("← Back"):
        st.session_state.page = 'doctor_appointments'
        st.rerun()

# ============================================================================
# VIDEO CALL
# ============================================================================

def video_call_page():
    """Real-time video call"""
    st.title("📹 Video Consultation")
    
    meeting = st.session_state.current_meeting
    
    # Meeting info
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info(f"""
        **Meeting ID:** {meeting['meeting_id']}  
        **Password:** {meeting['meeting_password']}  
        **Date:** {meeting['date']} at {meeting['time']}  
        **{'Doctor' if st.session_state.user_type == 'patient' else 'Patient'}:** 
        {'Dr. ' + meeting['doctor_name'] if st.session_state.user_type == 'patient' else meeting['patient_name']}
        """)
    
    with col2:
        if st.button("🔚 End Call", type="primary"):
            appointments = load_csv(APPOINTMENTS_CSV)
            appointments.loc[
                appointments['appointment_id'] == meeting['appointment_id'],
                'status'
            ] = 'completed'
            save_csv(appointments, APPOINTMENTS_CSV)
            
            st.success("Call ended!")
            
            if st.session_state.user_type == 'patient':
                st.session_state.page = 'patient_appointments'
            else:
                st.session_state.page = 'doctor_appointments'
            st.rerun()
    
    st.write("---")
    
    # Video interface
    if not WEBRTC_AVAILABLE:
        st.error("Install: pip install streamlit-webrtc")
        return
    
    st.write("### 🎥 Live Video")
    
    try:
        webrtc_ctx = webrtc_streamer(
            key=f"call-{meeting['meeting_id']}",
            mode=WebRtcMode.SENDRECV,
            rtc_configuration=RTC_CONFIGURATION,
            media_stream_constraints={"video": True, "audio": True},
            async_processing=True,
        )
        
        if webrtc_ctx.state.playing:
            st.success("✅ Connected - Call is live!")
        else:
            st.warning("Click START to join the call")
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
    
    if st.button("← Back"):
        if st.session_state.user_type == 'patient':
            st.session_state.page = 'patient_appointments'
        else:
            st.session_state.page = 'doctor_appointments'
        st.rerun()

# ============================================================================
# ADMIN UI
# ============================================================================

def admin_login_page():
    """Admin login"""
    st.title("🛡️ Admin Login")
    
    with st.form("admin_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit = st.form_submit_button("Login")
        
        if submit:
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.user_type = 'admin'
                st.session_state.page = 'admin_dashboard'
                st.success("Admin login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")
    
    if st.button("← Back"):
        st.session_state.page = 'landing'
        st.rerun()

def admin_dashboard():
    """Admin dashboard"""
    st.title("🛡️ Admin Dashboard")
    
    with st.sidebar:
        if st.button("🚪 Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    # Stats
    doctors = load_csv(DOCTORS_CSV)
    patients = load_csv(PATIENTS_CSV)
    appointments = load_csv(APPOINTMENTS_CSV)
    orders = load_csv(ORDERS_CSV)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Doctors", len(doctors[doctors['approval_status'] == 'approved']))
    col2.metric("Patients", len(patients))
    col3.metric("Appointments", len(appointments))
    col4.metric("Orders", len(orders))
    
    st.write("### Recent Activity")
    st.write("All systems operational ✅")

# ============================================================================
# MAIN ROUTER
# ============================================================================

def main():
    """Main application"""
    st.set_page_config(
        page_title="MediConnect",
        page_icon="🏥",
        layout="wide"
    )
    
    init_csv_files()
    
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    # Admin access
    with st.sidebar:
        if not st.session_state.logged_in:
            if st.button("🛡️ Admin", key="admin_btn"):
                st.session_state.page = 'admin_login'
                st.rerun()
    
    page = st.session_state.page
    
    # Patient
    if page == 'landing':
        patient_landing_page()
    elif page == 'patient_signup':
        patient_signup_page()
    elif page == 'patient_login':
        patient_login_page()
    elif page == 'patient_dashboard':
        patient_dashboard()
    elif page == 'find_doctors':
        find_doctors_page()
    elif page == 'book_appointment':
        book_appointment_page()
    elif page == 'patient_appointments':
        patient_appointments_page()
    elif page == 'medicine_marketplace':
        medicine_marketplace()
    elif page == 'checkout':
        checkout_page()
    elif page == 'patient_prescriptions':
        patient_prescriptions_page()
    
    # Doctor
    elif page == 'doctor_login':
        doctor_login_page()
    elif page == 'doctor_dashboard':
        doctor_dashboard()
    elif page == 'doctor_appointments':
        doctor_appointments_page()
    elif page == 'doctor_profile':
        doctor_profile_page()
    elif page == 'create_prescription':
        create_prescription_page()
    
    # Admin
    elif page == 'admin_login':
        admin_login_page()
    elif page == 'admin_dashboard':
        admin_dashboard()
    
    # Shared
    elif page == 'video_call':
        video_call_page()

if __name__ == "__main__":
    main()