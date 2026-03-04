import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Student Grade Portal",
    page_icon="📚",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main { padding: 1rem; }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .header h1 { font-size: 2.5rem; margin: 0; }
    .grade-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 30px;
        text-align: center;
        margin: 2rem 0;
    }
    .grade-card .grade-value {
        font-size: 8rem;
        font-weight: 800;
        line-height: 1;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border-radius: 50px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('grades.csv', dtype=str)
    df['ID Number'] = df['ID Number'].fillna('').str.strip()
    df['First Name'] = df['First Name'].fillna('').str.strip()
    df['Father Name'] = df['Father Name'].fillna('').str.strip()
    df['Password'] = df['Password'].fillna('1234').astype(str).str.strip()
    df['Password'] = df['Password'].str.replace('.0', '', regex=False)
    df['Total Marks'] = pd.to_numeric(df['Total Marks'], errors='coerce')
    df['Grade'] = df['Grade'].fillna('N/A')
    return df

df = load_data()

# Session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.student = None

# Login Page
if not st.session_state.logged_in:
    st.markdown("""
    <div class="header">
        <h1>📚 Student Grade Portal</h1>
        <p>Access your academic results securely</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        with st.form("login_form"):
            st.markdown("### 🔐 Login")
            student_id = st.text_input("📋 ID Number", placeholder="Enter your ID")
            password = st.text_input("🔑 Password", type="password", placeholder="Enter 1234")
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                student_id = student_id.strip()
                password = password.strip()
                student = df[(df['ID Number'] == student_id) & (df['Password'] == password)]
                
                if not student.empty:
                    st.session_state.logged_in = True
                    st.session_state.student = student.iloc[0]
                    st.rerun()
                else:
                    st.error("❌ Invalid ID or Password")

# Grades Page
else:
    student = st.session_state.student
    st.markdown(f"""
    <div class="header">
        <h1>Welcome, {student['First Name']}!</h1>
        <p>{student['First Name']} {student['Father Name']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([5,1])
    with col2:
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.rerun()
    
    st.markdown(f"""
    <div class="grade-card">
        <div style="font-size:1.2rem;">YOUR GRADE</div>
        <div class="grade-value">{student['Grade']}</div>
        <div style="font-size:1.5rem;">{student['First Name']} {student['Father Name']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    if pd.notna(student['Total Marks']):
        st.metric("Total Marks", f"{student['Total Marks']:.1f}%")
        st.progress(float(student['Total Marks'])/100)
    
    with st.expander("📋 Details"):
        st.write(f"**ID Number:** {student['ID Number']}")
        st.write(f"**Full Name:** {student['First Name']} {student['Father Name']}")
        st.write(f"**Total Marks:** {student['Total Marks']:.1f}%")
        st.write(f"**Grade:** {student['Grade']}")

st.markdown("---")
st.markdown("🔒 Secure Portal - Each student sees only their own grades")
