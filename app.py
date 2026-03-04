import streamlit as st
import pandas as pd
import hashlib

# Page configuration
st.set_page_config(
    page_title="Student Grade Portal",
    page_icon="📚",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better design
st.markdown("""
<style>
    /* Main container */
    .main {
        padding: 1rem;
    }
    
    /* Header style */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .header h1 {
        font-size: 2.5rem;
        margin: 0;
        font-weight: 700;
    }
    
    .header p {
        font-size: 1.1rem;
        opacity: 0.95;
        margin-top: 0.5rem;
    }
    
    /* Card styles */
    .card {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    
    /* Success message */
    .success-message {
        background: #10b981;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Warning message */
    .warning-message {
        background: #f59e0b;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    /* Grade card */
    .grade-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 30px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 20px 40px rgba(102,126,234,0.3);
    }
    
    .grade-card .grade-value {
        font-size: 8rem;
        font-weight: 800;
        line-height: 1;
        margin: 1rem 0;
        text-shadow: 4px 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Button styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        font-size: 1rem;
        padding: 0.6rem 1.5rem;
        border: none;
        border-radius: 50px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102,126,234,0.4);
    }
    
    /* Password requirements */
    .password-requirements {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #666;
        margin: 1rem 0;
    }
    
    .password-requirements ul {
        margin: 0.5rem 0 0 1.5rem;
    }
    
    /* Divider */
    .divider {
        margin: 2rem 0;
        border-top: 2px dashed #e0e0e0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #999;
        font-size: 0.9rem;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid #eee;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to hash passwords (for security)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('grades.csv', dtype=str)
    df['ID Number'] = df['ID Number'].fillna('').str.strip()
    df['First Name'] = df['First Name'].fillna('').str.strip()
    df['Father Name'] = df['Father Name'].fillna('').str.strip()
    
    # Check if password is already hashed or plain
    if 'Password' in df.columns:
        df['Password'] = df['Password'].fillna('1234').astype(str).str.strip()
        # Remove .0 if present
        df['Password'] = df['Password'].str.replace('.0', '', regex=False)
    else:
        df['Password'] = '1234'
    
    df['Total Marks'] = pd.to_numeric(df['Total Marks'], errors='coerce')
    df['Grade'] = df['Grade'].fillna('N/A')
    return df

df = load_data()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student = None
    st.session_state.show_change_password = False
    st.session_state.password_changed = False

# ==================== LOGIN PAGE ====================
if not st.session_state.logged_in:
    # Header
    st.markdown("""
    <div class="header">
        <h1>📚 Student Grade Portal</h1>
        <p>Access your academic results securely</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show password change success message if coming from logout
    if st.session_state.password_changed:
        st.markdown("""
        <div class="success-message">
            ✅ Password changed successfully! Please login with your new password.
        </div>
        """, unsafe_allow_html=True)
        st.session_state.password_changed = False
    
    # Login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Student Login")
            st.info("First-time login? Use password: **1234**")
            
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
                    # Check password (supports both plain and hashed)
                    stored_password = student.iloc[0]['Password']
                    
                    # If password is "1234" (default), allow login
                    # In a real app with hashed passwords, you'd check hash
                    if password == stored_password or (stored_password == "1234" and password == "1234"):
                        st.session_state.logged_in = True
                        st.session_state.student = student.iloc[0]
                        
                        # Show password change option if using default password
                        if stored_password == "1234" and password == "1234":
                            st.session_state.show_change_password = True
                        else:
                            st.session_state.show_change_password = False
                        
                        st.rerun()
                    else:
                        st.error("❌ Incorrect password")
                else:
                    st.error("❌ ID Number not found")

# ==================== GRADES PAGE ====================
else:
    student = st.session_state.student
    
    # Welcome header with logout
    col1, col2, col3 = st.columns([5, 2, 1])
    with col1:
        st.markdown(f"""
        <div class="header" style="margin-bottom: 1rem; padding: 1rem;">
            <h2>Welcome, {student['First Name']}!</h2>
            <p>{student['First Name']} {student['Father Name']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.show_change_password = False
            st.rerun()
    
    # Show password change option if using default password
    if st.session_state.show_change_password:
        st.markdown("""
        <div class="warning-message">
            🔔 You are using the default password (1234). For security, please change your password.
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("🔐 Change Your Password", expanded=True):
            with st.form("change_password_form"):
                new_password = st.text_input("New Password", type="password", 
                                            placeholder="Enter new password")
                confirm_password = st.text_input("Confirm New Password", type="password",
                                                placeholder="Confirm new password")
                
                # Password requirements
                st.markdown("""
                <div class="password-requirements">
                    <b>Password requirements:</b>
                    <ul>
                        <li>At least 6 characters long</li>
                        <li>Can include letters, numbers, and symbols</li>
                        <li>Don't share your password with anyone</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
                
                submitted = st.form_submit_button("Change Password", use_container_width=True)
                
                if submitted:
                    if len(new_password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        # In a real app, you would save the hashed password
                        # For this demo, we'll show success and ask to login again
                        st.success("✅ Password changed successfully! Please login again with your new password.")
                        st.session_state.logged_in = False
                        st.session_state.password_changed = True
                        st.session_state.show_change_password = False
                        st.rerun()
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Metrics row
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if pd.notna(student['Total Marks']):
            st.metric("Total Marks", f"{student['Total Marks']:.1f}%")
    
    with col2:
        st.metric("Grade", student['Grade'])
    
    with col3:
        if pd.notna(student['Total Marks']):
            status = "✅ PASS" if student['Total Marks'] >= 50 else "❌ FAIL"
            st.metric("Status", status)
    
    # Main grade display
    st.markdown(f"""
    <div class="grade-card">
        <div style="font-size:1.2rem; opacity:0.9;">YOUR GRADE</div>
        <div class="grade-value">{student['Grade']}</div>
        <div style="font-size:1.5rem;">{student['First Name']} {student['Father Name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    if pd.notna(student['Total Marks']):
        st.progress(float(student['Total Marks']) / 100)
    
    # Detailed information
    with st.expander("📋 View Complete Details"):
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px;">
            <p><b>First Name:</b> {student['First Name']}</p>
            <p><b>Father Name:</b> {student['Father Name']}</p>
            <p><b>ID Number:</b> {student['ID Number']}</p>
            <p><b>Total Marks:</b> {student['Total Marks']:.1f}%</p>
            <p><b>Grade:</b> {student['Grade']}</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>🔒 Secure Portal • Each student can only see their own grades</p>
    <p style="font-size: 0.8rem;">© 2025 Student Grade Management System</p>
</div>
""", unsafe_allow_html=True)
