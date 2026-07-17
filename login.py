import streamlit as st

from services.api import APIError, login_admin, logout_admin


def initialize_auth_state() -> None:
    defaults = {
        "logged_in": False,
        "access_token": None,
        "refresh_token": None,
        "admin_name": None,
        "admin_email": None,
        "role": None,
        "is_super_admin": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def login_page() -> None:
    initialize_auth_state()

    _, center, _ = st.columns([0.8, 1.5, 0.8])

    with center:
        st.html(
            """
<div class="login-brand-panel">
    <div class="login-logo-box">
        🌿
    </div>

    <div>
        <div class="login-brand-title">
            PlantGuard
        </div>

        <div class="login-brand-console">
            Admin Console
        </div>
    </div>
</div>

<div class="login-card-header">
    <div class="login-title">
        Welcome back
    </div>

    <div class="login-subtitle">
        Sign in to your admin account to manage PlantGuard.
    </div>
</div>
"""
        )

        with st.form("login_form"):
            st.markdown(
                '<div class="login-label">Email Address</div>',
                unsafe_allow_html=True,
            )

            email = st.text_input(
                "Email Address",
                placeholder="admin@plantguard.com",
                label_visibility="collapsed",
                key="login_email",
            )

            st.markdown(
                '<div class="login-label password-label">Password</div>',
                unsafe_allow_html=True,
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                label_visibility="collapsed",
                key="login_password",
            )

            submitted = st.form_submit_button(
                "Sign in to Admin Console →",
                use_container_width=True,
            )

            if submitted:
                clean_email = email.strip().lower()

                if not clean_email or not password:
                    st.error(
                        "Please enter your email and password."
                    )
                    return

                try:
                    with st.spinner("Signing in..."):
                        result = login_admin(
                            email=clean_email,
                            password=password,
                        )

                    if result.get("role") != "admin":
                        st.error(
                            "Access denied. Only administrators can sign in."
                        )
                        return

                    st.session_state.logged_in = True
                    st.session_state.access_token = result.get(
                        "access_token"
                    )
                    st.session_state.refresh_token = result.get(
                        "refresh_token"
                    )
                    st.session_state.admin_name = result.get(
                        "name",
                        "Administrator",
                    )
                    st.session_state.admin_email = result.get(
                        "email",
                        clean_email,
                    )
                    st.session_state.role = result.get(
                        "role",
                        "admin",
                    )
                    st.session_state.is_super_admin = result.get(
                        "is_super_admin",
                        False,
                    )

                    st.rerun()

                except APIError as error:
                    st.error(str(error))

                except Exception as error:
                    st.error(
                        f"An unexpected login error occurred: {error}"
                    )

        st.html(
            """
<div class="login-authorised-note">
    This portal is for authorised PlantGuard administrators only.
</div>

<div class="login-helper">
    Temporary testing credentials<br><br>

    <strong>admin@plantguard.com</strong><br>
    <strong>admin123</strong>
</div>
"""
        )


def logout() -> None:
    access_token = st.session_state.get(
        "access_token"
    )

    if access_token:
        try:
            logout_admin(access_token)

        except APIError:
            pass

        except Exception:
            pass

    session_keys = [
        "logged_in",
        "access_token",
        "refresh_token",
        "admin_name",
        "admin_email",
        "role",
        "is_super_admin",
    ]

    for key in session_keys:
        st.session_state.pop(key, None)

    st.rerun()