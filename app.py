import streamlit as st
import pandas as pd
import time

# Page configuration
st.set_page_config(
    page_title="Student Grade Portal",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        padding: 1rem;
    }
    
    /* Header style */
    .header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 30px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(30,60,114,0.3);
    }
    
    .header h1 {
        font-size: 2.8rem;
        margin: 0;
        font-weight: 800;
    }
    
    .header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Card styles */
    .card {
        background: white;
        padding: 2.5rem;
        border-radius: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
    }
    
    /* Success message */
    .success-message {
        background: #10b981;
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(16,185,129,0.2);
    }
    
    /* Warning message */
    .warning-message {
        background: #f59e0b;
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(245,158,11,0.2);
    }
    
    /* Info message */
    .info-message {
        background: #3b82f6;
        color: white;
        padding: 1.2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(59,130,246,0.2);
    }
    
    /* Grade card */
    .grade-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        padding: 3rem;
        border-radius: 40px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 30px 60px rgba(30,60,114,0.4);
    }
    
    .grade-card .grade-label {
        font-size: 1.3rem;
        opacity: 0.9;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    .grade-card .grade-value {
        font-size: 9rem;
        font-weight: 800;
        line-height: 1;
        margin: 1rem 0;
        text-shadow: 4px 4px 12px rgba(0,0,0,0.3);
    }
    
    .grade-card .student-name {
        font-size: 1.8rem;
        font-weight: 500;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        flex: 1;
        background: white;
        padding: 1.8rem;
        border-radius: 25px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
    }
    
    .metric-card .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1e3c72;
    }
    
    .metric-card .metric-label {
        font-size: 1rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        padding: 0.8rem 2rem;
        border: none;
        border-radius: 60px;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 10px 20px rgba(30,60,114,0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(30,60,114,0.3);
    }
    
    /* Secondary button */
    .secondary-btn > button {
        background: white;
        color: #1e3c72;
        border: 2px solid #1e3c72;
        box-shadow: none;
    }
    
    .secondary-btn > button:hover {
        background: #f8fafc;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border: 2px solid #e2e8f0;
        border-radius: 60px;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 4px rgba(30,60,114,0.1);
    }
    
    /* Password requirements box */
    .password-box {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0;
    }
    
    .password-box h4 {
        color: #1e3c72;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .password-box ul {
        color: #475569;
        margin-left: 1.5rem;
    }
    
    .password-box li {
        margin: 0.5rem 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid #e2e8f0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ==================== DATABASE SIMULATION ====================
# In a real app, this would be a real database
# For demo, we'll store passwords in session state

if 'user_passwords' not in st.session_state:
    st.session_state.user_passwords = {}

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('grades.csv', dtype=str)
    df['ID Number'] = df['ID Number'].fillna('').str.strip()
    df['First Name'] = df['First Name'].fillna('').str.strip()
    df['Father Name'] = df['Father Name'].fillna('').str.strip()
    df['Total Marks'] = pd.to_numeric(df['Total Marks'], errors='coerce')
    df['Grade'] = df['Grade'].fillna('N/A')
    return df

df = load_data()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student = None
    st.session_state.page = 'login'
    st.session_state.message = None
    st.session_state.message_type = None
    st.session_state.temp_id = None

# ==================== HELPER FUNCTIONS ====================
def set_message(msg, type='success'):
    st.session_state.message = msg
    st.session_state.message_type = type

def clear_message():
    st.session_state.message = None
    st.session_state.message_type = None

def check_password(student_id, password):
    """Check if password is correct"""
    # If user has changed password, check stored password
    if student_id in st.session_state.user_passwords:
        return password == st.session_state.user_passwords[student_id]
    # Otherwise, default password is 1234
    return password == "1234"

def update_password(student_id, new_password):
    """Update user's password"""
    st.session_state.user_passwords[student_id] = new_password
    return True

# ==================== MESSAGE DISPLAY ====================
def show_message():
    if st.session_state.message:
        if st.session_state.message_type == 'success':
            st.markdown(f'<div class="success-message">✅ {st.session_state.message}</div>', unsafe_allow_html=True)
        elif st.session_state.message_type == 'warning':
            st.markdown(f'<div class="warning-message">⚠️ {st.session_state.message}</div>', unsafe_allow_html=True)
        elif st.session_state.message_type == 'info':
            st.markdown(f'<div class="info-message">ℹ️ {st.session_state.message}</div>', unsafe_allow_html=True)
        clear_message()

# ==================== PAGE ROUTING ====================
if st.session_state.page == 'login':
    # ========== LOGIN PAGE ==========
    st.markdown("""
    <div class="header">
        <h1>🎓 Student Grade Portal</h1>
        <p>Secure access to your academic results</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_message()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Student Login")
            st.info("First time? Use password: **1234**")
            
            student_id = st.text_input(
                "📋 ID Number",
                placeholder="Enter your ID number"
            )
            password = st.text_input(
                "🔑 Password",
                type="password",
                placeholder="Enter your password"
            )
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                student_id = student_id.strip()
                password = password.strip()
                
                # Find student
                student = df[df['ID Number'].astype(str) == student_id]
                
                if not student.empty:
                    # Check password
                    if check_password(student_id, password):
                        st.session_state.student = student.iloc[0]
                        
                        # If using default password, go to change password page
                        if password == "1234" and student_id not in st.session_state.user_passwords:
                            st.session_state.temp_id = student_id
                            st.session_state.page = 'change_password'
                            set_message("For security, please create a new password", 'warning')
                        else:
                            st.session_state.logged_in = True
                            st.session_state.page = 'grades'
                            set_message(f"Welcome back, {student.iloc[0]['First Name']}!", 'success')
                        
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password")
                else:
                    st.error("❌ ID Number not found")

elif st.session_state.page == 'change_password':
    # ========== CHANGE PASSWORD PAGE ==========
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #1e3c72;">🔐 Create Your Password</h2>
        <p style="color: #64748b;">Please set a new password for your account</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("change_password_form"):
            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Enter new password"
            )
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm new password"
            )
            
            # Password requirements
            st.markdown("""
            <div class="password-box">
                <h4>📋 Password Requirements</h4>
                <ul>
                    <li>At least 6 characters long</li>
                    <li>Use a mix of letters and numbers</li>
                    <li>Don't use common passwords</li>
                    <li>Never share your password</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                back = st.form_submit_button("← Back to Login", use_container_width=True)
            with col2:
                change = st.form_submit_button("✅ Create Password", use_container_width=True, type="primary")
            
            if change:
                if len(new_password) < 6:
                    st.error("Password must be at least 6 characters")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Save new password
                    update_password(st.session_state.temp_id, new_password)
                    
                    # Clear temp data and go back to login
                    st.session_state.temp_id = None
                    st.session_state.page = 'login'
                    set_message("✅ Password created successfully! Please login with your new password.", 'success')
                    st.rerun()
            
            if back:
                st.session_state.temp_id = None
                st.session_state.page = 'login'
                st.rerun()

elif st.session_state.page == 'grades':
    # ========== GRADES PAGE ==========
    student = st.session_state.student
    
    # Header with logout
    col1, col2, col3 = st.columns([5, 1, 1])
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
                    color: white; padding: 1rem 2rem; border-radius: 60px; 
                    margin-bottom: 2rem;">
            <span style="font-weight: 600;">👋 Welcome, {student['First Name']} {student['Father Name']}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout", key="logout"):
            st.session_state.logged_in = False
            st.session_state.page = 'login'
            st.session_state.student = None
            st.rerun()
    
    show_message()
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if pd.notna(student['Total Marks']):
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{student['Total Marks']:.1f}%</div>
                <div class="metric-label">Total Marks</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{student['Grade']}</div>
            <div class="metric-label">Grade</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if pd.notna(student['Total Marks']):
            status = "PASS" if student['Total Marks'] >= 50 else "FAIL"
            color = "#10b981" if student['Total Marks'] >= 50 else "#ef4444"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value" style="color: {color};">{status}</div>
                <div class="metric-label">Status</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main grade display
    st.markdown(f"""
    <div class="grade-card">
        <div class="grade-label">Your Grade</div>
        <div class="grade-value">{student['Grade']}</div>
        <div class="student-name">{student['First Name']} {student['Father Name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    if pd.notna(student['Total Marks']):
        st.markdown("### 📈 Performance Overview")
        st.progress(float(student['Total Marks']) / 100)
    
    # Additional details
    with st.expander("📋 View Complete Details"):
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 2rem; border-radius: 20px;">
            <table style="width: 100%;">
                <tr><td style="padding: 12px; font-weight: 600;">First Name:</td><td>{student['First Name']}</td></tr>
                <tr><td style="padding: 12px; font-weight: 600;">Father Name:</td><td>{student['Father Name']}</td></tr>
                <tr><td style="padding: 12px; font-weight: 600;">ID Number:</td><td><code>{student['ID Number']}</code></td></tr>
                <tr><td style="padding: 12px; font-weight: 600;">Total Marks:</td><td>{student['Total Marks']:.1f}%</td></tr>
                <tr><td style="padding: 12px; font-weight: 600;">Grade:</td><td><b>{student['Grade']}</b></td></tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Secure Student Portal • Each student can only see their own grades</p>
    <p style="font-size: 0.8rem;">© 2026 Gabisa's Student Grade Management System | Version 1.0</p>
</div>
""", unsafe_allow_html=True)
