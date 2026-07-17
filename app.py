from pathlib import Path

import streamlit as st

from components.navbar import navbar
from components.sidebar import sidebar
from login import initialize_auth_state, login_page
from pages.add_admin import add_admin_page
from pages.audit_logs import audit_logs_page
from pages.dashboard import dashboard
from pages.farmers import farmers_page
from pages.settings import settings_page
from pages.treatments import treatments_page


st.set_page_config(
    page_title="PlantGuard Admin",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load CSS
css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )
else:
    st.error("assets/style.css was not found.")


# Authentication
initialize_auth_state()

if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()


# Navigation
page = sidebar()
navbar(page)


# Pages
if page == "Dashboard":
    dashboard()

elif page == "Treatments":
    treatments_page()

elif page == "Farmers":
    farmers_page()

elif page == "Audit Logs":
    audit_logs_page()

elif page == "Add Admin":
    if st.session_state.get("is_super_admin", False):
        add_admin_page()
    else:
        st.error("Only the Super Admin can access this page.")

elif page == "Settings":
    settings_page()