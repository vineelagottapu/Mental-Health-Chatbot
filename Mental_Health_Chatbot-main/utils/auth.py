import streamlit as st
import hashlib
import json
import os
from datetime import datetime

class AuthManager:
    """Simple authentication system for MindfulChat"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except:
                self.users = {}
        else:
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username, email, password):
        """Register a new user"""
        if username in self.users:
            return False, "Username already exists"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # Check if email is already registered
        for user_data in self.users.values():
            if user_data['email'] == email:
                return False, "Email already registered"
        
        self.users[username] = {
            'email': email,
            'password': self.hash_password(password),
            'created_at': datetime.now().isoformat(),
            'chat_history': []
        }
        
        self.save_users()
        return True, "Account created successfully!"
    
    def login_user(self, username, password):
        """Authenticate user login"""
        if username not in self.users:
            return False, "Username not found"
        
        if self.users[username]['password'] != self.hash_password(password):
            return False, "Incorrect password"
        
        return True, "Login successful!"
    
    def get_user_data(self, username):
        """Get user data"""
        return self.users.get(username, {})
    
    def save_chat_history(self, username, messages):
        """Save user's chat history"""
        if username in self.users:
            self.users[username]['chat_history'] = messages
            self.save_users()
    
    def load_chat_history(self, username):
        """Load user's chat history"""
        if username in self.users:
            return self.users[username].get('chat_history', [])
        return []
    
    def logout_user(self):
        """Clear session state for logout"""
        for key in list(st.session_state.keys()):
            if str(key).startswith('auth_') or key == 'messages':
                del st.session_state[key]

def show_login_form():
    """Display login form"""
    st.markdown("### 🔐 Login to MindfulChat")
    st.markdown("*Welcome back! Sign in to continue your mental health journey.*")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login", use_container_width=True)
        
        if login_button:
            if username and password:
                auth_manager = AuthManager()
                success, message = auth_manager.login_user(username, password)
                
                if success:
                    st.session_state.auth_logged_in = True
                    st.session_state.auth_username = username
                    # Load user's chat history
                    chat_history = auth_manager.load_chat_history(username)
                    st.session_state.messages = chat_history
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please fill in all fields")

def show_signup_form():
    """Display signup form"""
    st.markdown("### 📝 Create Your MindfulChat Account")
    st.markdown("*Join our supportive community. Your mental health journey starts here.*")
    
    with st.form("signup_form"):
        username = st.text_input("Choose a Username")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        signup_button = st.form_submit_button("Create Account", use_container_width=True)
        
        if signup_button:
            if username and email and password and confirm_password:
                if password != confirm_password:
                    st.error("Passwords don't match")
                elif "@" not in email:
                    st.error("Please enter a valid email address")
                else:
                    auth_manager = AuthManager()
                    success, message = auth_manager.register_user(username, email, password)
                    
                    if success:
                        st.success(message)
                        st.info("You can now login with your new account!")
                        # Switch to login view
                        st.session_state.auth_show_signup = False
                        st.rerun()
                    else:
                        st.error(message)
            else:
                st.error("Please fill in all fields")

def show_auth_page():
    """Display authentication page with login/signup tabs"""
    st.set_page_config(
        page_title="MindfulChat - Login",
        page_icon="🧠",
        layout="centered"
    )
    
    # Header
    st.title("🧠 MindfulChat")
    st.markdown("### Your AI Mental Health Companion")
    st.markdown("*A safe space to share your feelings and get support*")
    
    # Add some spacing
    st.markdown("---")
    
    # Initialize session state for form switching
    if 'auth_show_signup' not in st.session_state:
        st.session_state.auth_show_signup = False
    
    # Create columns for centering the forms
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Toggle buttons
        login_tab, signup_tab = st.columns(2)
        
        with login_tab:
            if st.button("Login", use_container_width=True, 
                        type="primary" if not st.session_state.auth_show_signup else "secondary"):
                st.session_state.auth_show_signup = False
                st.rerun()
        
        with signup_tab:
            if st.button("Sign Up", use_container_width=True,
                        type="primary" if st.session_state.auth_show_signup else "secondary"):
                st.session_state.auth_show_signup = True
                st.rerun()
        
        st.markdown("---")
        
        # Show appropriate form
        if st.session_state.auth_show_signup:
            show_signup_form()
        else:
            show_login_form()
    
    # Footer information
    st.markdown("---")
    st.markdown("#### 🆘 Crisis Resources")
    st.markdown("""
    **If you're in crisis, please reach out immediately:**
    - **Emergency**: 911
    - **Crisis Text Line**: Text HOME to 741741
    - **National Suicide Prevention Lifeline**: 988
    """)

def is_logged_in():
    """Check if user is logged in"""
    return st.session_state.get('auth_logged_in', False)

def get_current_user():
    """Get current logged in username"""
    return st.session_state.get('auth_username', '')

def require_auth(func):
    """Decorator to require authentication"""
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            show_auth_page()
            return
        return func(*args, **kwargs)
    return wrapper