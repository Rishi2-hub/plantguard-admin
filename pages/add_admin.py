import re

import streamlit as st


def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def initialize_admins() -> None:
    if "admins_data" not in st.session_state:
        st.session_state.admins_data = [
            {
                "id": 1,
                "name": "Ritik Budhathoki",
                "email": "ritik@plantguard.com",
                "role": "Super Admin",
                "status": "Active",
            }
        ]


def add_admin_page() -> None:
    initialize_admins()

    if not st.session_state.get("is_super_admin", False):
        st.error("Only the Super Admin can create administrator accounts.")
        return

    st.html(
        """
<div class="page-heading">
    <div>
        <div class="page-title">Add Administrator</div>
        <div class="page-subtitle">
            Create and manage authorised PlantGuard administrator accounts.
        </div>
    </div>

    <div class="page-badge">
        🛡️ Super Admin Only
    </div>
</div>
"""
    )

    left, right = st.columns(
        [1.45, 1],
        gap="large",
    )

    with left:
        st.html(
            """
<div class="section-panel-heading form-heading">
    <div class="panel-title">Administrator Details</div>
    <div class="panel-subtitle">
        Enter the new administrator's information below.
    </div>
</div>
"""
        )

        with st.form(
            "add_admin_form",
            clear_on_submit=True,
        ):
            full_name = st.text_input(
                "Full Name",
                placeholder="Enter administrator name",
            )

            email = st.text_input(
                "Email Address",
                placeholder="admin@plantguard.com",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Minimum 8 characters",
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Re-enter password",
            )

            role = st.selectbox(
                "Role",
                ["Admin"],
                disabled=True,
            )

            authorised = st.checkbox(
                "I confirm that this person is authorised to access PlantGuard."
            )

            submitted = st.form_submit_button(
                "Create Administrator",
                use_container_width=True,
            )

            if submitted:
                errors = []

                clean_name = full_name.strip()
                clean_email = email.strip().lower()

                if not clean_name:
                    errors.append("Full name is required.")

                if not clean_email:
                    errors.append("Email address is required.")
                elif not is_valid_email(clean_email):
                    errors.append("Enter a valid email address.")

                existing_email = any(
                    admin["email"].lower() == clean_email
                    for admin in st.session_state.admins_data
                )

                if existing_email:
                    errors.append(
                        "An administrator with this email already exists."
                    )

                if len(password) < 8:
                    errors.append(
                        "Password must contain at least 8 characters."
                    )

                if password != confirm_password:
                    errors.append("Passwords do not match.")

                if not authorised:
                    errors.append(
                        "You must confirm that this administrator is authorised."
                    )

                if errors:
                    for error in errors:
                        st.error(error)

                else:
                    new_id = max(
                        admin["id"]
                        for admin in st.session_state.admins_data
                    ) + 1

                    st.session_state.admins_data.append(
                        {
                            "id": new_id,
                            "name": clean_name,
                            "email": clean_email,
                            "role": role,
                            "status": "Active",
                        }
                    )

                    st.success(
                        f"Administrator account for {clean_name} was created successfully."
                    )

    with right:
        st.html(
            """
<div class="admin-info-card">
    <div class="admin-info-icon">🛡️</div>

    <div class="admin-info-title">
        Administrator Access
    </div>

    <div class="admin-info-text">
        Administrators can manage treatment records, farmer accounts,
        audit logs, and PlantGuard operations.
    </div>

    <div class="admin-info-divider"></div>

    <div class="admin-rule-item">
        <span>✓</span>
        <div>Use a unique work email address.</div>
    </div>

    <div class="admin-rule-item">
        <span>✓</span>
        <div>Use a strong password with at least eight characters.</div>
    </div>

    <div class="admin-rule-item">
        <span>✓</span>
        <div>Every administrator must use an individual account.</div>
    </div>

    <div class="admin-rule-item">
        <span>✓</span>
        <div>Administrator activity is stored in audit logs.</div>
    </div>
</div>
"""
        )

        st.html(
            """
<div class="security-warning-card">
    <div class="security-warning-title">
        ⚠ Security Reminder
    </div>

    <div class="security-warning-text">
        Never share administrator credentials or create accounts
        for unauthorised users.
    </div>
</div>
"""
        )

    st.html(
        """
<div class="section-panel-heading admin-list-heading">
    <div class="panel-title">Existing Administrators</div>
    <div class="panel-subtitle">
        Current administrator accounts in the temporary session.
    </div>
</div>
"""
    )

    st.dataframe(
        st.session_state.admins_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "id": st.column_config.NumberColumn(
                "ID",
                width="small",
            ),
            "name": st.column_config.TextColumn(
                "Name",
                width="large",
            ),
            "email": st.column_config.TextColumn(
                "Email",
                width="large",
            ),
            "role": st.column_config.TextColumn(
                "Role",
                width="medium",
            ),
            "status": st.column_config.TextColumn(
                "Status",
                width="small",
            ),
        },
    )