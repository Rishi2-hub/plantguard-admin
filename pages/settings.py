import streamlit as st


def initialize_settings() -> None:
    defaults = {
        "profile_name": st.session_state.get(
            "admin_name",
            "Ritik Budhathoki",
        ),
        "profile_phone": "",
        "profile_language": "English",
        "notify_disease_alerts": True,
        "notify_failed_logins": True,
        "notify_new_farmers": True,
        "notify_treatment_updates": False,
        "notify_weekly_summary": True,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def settings_page() -> None:
    initialize_settings()

    st.html(
        """
<div class="page-heading">
    <div>
        <div class="page-title">Settings</div>
        <div class="page-subtitle">
            Manage your profile, notifications, and account security.
        </div>
    </div>

    <div class="page-badge">
        ⚙️ System Preferences
    </div>
</div>
"""
    )

    profile_tab, notification_tab, security_tab = st.tabs(
        [
            "👤 Profile",
            "🔔 Notifications",
            "🔐 Security",
        ]
    )

    with profile_tab:
        profile_settings()

    with notification_tab:
        notification_settings()

    with security_tab:
        security_settings()


def profile_settings() -> None:
    left, right = st.columns(
        [1.45, 1],
        gap="large",
    )

    with left:
        st.html(
            """
<div class="section-panel-heading form-heading">
    <div class="panel-title">Administrator Profile</div>
    <div class="panel-subtitle">
        Update your personal information and preferred language.
    </div>
</div>
"""
        )

        with st.form("profile_settings_form"):
            full_name = st.text_input(
                "Full Name",
                value=st.session_state.profile_name,
            )

            email = st.text_input(
                "Email Address",
                value=st.session_state.get(
                    "admin_email",
                    "admin@plantguard.com",
                ),
                disabled=True,
            )

            role = st.text_input(
                "Role",
                value=(
                    "Super Admin"
                    if st.session_state.get(
                        "is_super_admin",
                        False,
                    )
                    else "Admin"
                ),
                disabled=True,
            )

            phone = st.text_input(
                "Phone Number",
                value=st.session_state.profile_phone,
                placeholder="+977 98XXXXXXXX",
            )

            language_options = [
                "English",
                "Nepali",
            ]

            selected_language = (
                st.session_state.profile_language
                if st.session_state.profile_language
                in language_options
                else "English"
            )

            language = st.selectbox(
                "Preferred Language",
                language_options,
                index=language_options.index(
                    selected_language
                ),
            )

            save_profile = st.form_submit_button(
                "Save Profile Changes",
                use_container_width=True,
            )

            if save_profile:
                clean_name = full_name.strip()

                if not clean_name:
                    st.error("Full name is required.")

                else:
                    st.session_state.profile_name = clean_name
                    st.session_state.profile_phone = phone.strip()
                    st.session_state.profile_language = language
                    st.session_state.admin_name = clean_name

                    st.success(
                        "Profile settings saved successfully."
                    )

    with right:
        admin_name = st.session_state.profile_name

        initials = "".join(
            part[0].upper()
            for part in admin_name.split()[:2]
            if part
        )

        st.html(
            f"""
<div class="settings-profile-card">
    <div class="settings-profile-avatar">
        {initials or "AD"}
    </div>

    <div class="settings-profile-name">
        {admin_name}
    </div>

    <div class="settings-profile-role">
        {
            "Super Admin"
            if st.session_state.get("is_super_admin", False)
            else "Admin"
        }
    </div>

    <div class="settings-divider"></div>

    <div class="settings-detail-row">
        <span>Account Status</span>
        <strong class="settings-active">Active</strong>
    </div>

    <div class="settings-detail-row">
        <span>Email</span>
        <strong>
            {st.session_state.get("admin_email", "admin@plantguard.com")}
        </strong>
    </div>

    <div class="settings-detail-row">
        <span>Language</span>
        <strong>{st.session_state.profile_language}</strong>
    </div>
</div>
"""
        )


def notification_settings() -> None:
    st.html(
        """
<div class="section-panel-heading form-heading">
    <div class="panel-title">Notification Preferences</div>
    <div class="panel-subtitle">
        Choose which PlantGuard events should notify you.
    </div>
</div>
"""
    )

    with st.form("notification_settings_form"):
        disease_alerts = st.toggle(
            "Disease outbreak alerts",
            value=st.session_state.notify_disease_alerts,
            help="Notify when disease detections increase.",
        )

        failed_logins = st.toggle(
            "Failed login alerts",
            value=st.session_state.notify_failed_logins,
            help="Notify about suspicious administrator login attempts.",
        )

        new_farmers = st.toggle(
            "New farmer registrations",
            value=st.session_state.notify_new_farmers,
        )

        treatment_updates = st.toggle(
            "Treatment updates",
            value=st.session_state.notify_treatment_updates,
        )

        weekly_summary = st.toggle(
            "Weekly activity summary",
            value=st.session_state.notify_weekly_summary,
        )

        notification_methods = st.multiselect(
            "Notification Methods",
            [
                "Admin Dashboard",
                "Email",
            ],
            default=["Admin Dashboard"],
        )

        save_notifications = st.form_submit_button(
            "Save Notification Settings",
            use_container_width=True,
        )

        if save_notifications:
            if not notification_methods:
                st.error(
                    "Select at least one notification method."
                )

            else:
                st.session_state.notify_disease_alerts = (
                    disease_alerts
                )

                st.session_state.notify_failed_logins = (
                    failed_logins
                )

                st.session_state.notify_new_farmers = (
                    new_farmers
                )

                st.session_state.notify_treatment_updates = (
                    treatment_updates
                )

                st.session_state.notify_weekly_summary = (
                    weekly_summary
                )

                st.success(
                    "Notification preferences saved successfully."
                )


def security_settings() -> None:
    left, right = st.columns(
        [1.45, 1],
        gap="large",
    )

    with left:
        st.html(
            """
<div class="section-panel-heading form-heading">
    <div class="panel-title">Change Password</div>
    <div class="panel-subtitle">
        Use a strong and unique administrator password.
    </div>
</div>
"""
        )

        with st.form("change_password_form"):
            current_password = st.text_input(
                "Current Password",
                type="password",
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                placeholder="Minimum 8 characters",
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
            )

            change_password = st.form_submit_button(
                "Change Password",
                use_container_width=True,
            )

            if change_password:
                errors = []

                if not current_password:
                    errors.append(
                        "Current password is required."
                    )

                if len(new_password) < 8:
                    errors.append(
                        "New password must contain at least 8 characters."
                    )

                if new_password != confirm_password:
                    errors.append(
                        "New passwords do not match."
                    )

                if (
                    current_password
                    and current_password == new_password
                ):
                    errors.append(
                        "New password must be different from the current password."
                    )

                if errors:
                    for error in errors:
                        st.error(error)

                else:
                    st.success(
                        "Password validation passed. "
                        "The backend update will be connected later."
                    )

    with right:
        st.html(
            """
<div class="security-status-card">
    <div class="security-status-icon">
        🔐
    </div>

    <div class="security-status-title">
        Security Status
    </div>

    <div class="security-status-badge">
        Strong
    </div>

    <div class="security-item">
        <span>✓</span>
        Strong password enabled
    </div>

    <div class="security-item">
        <span>✓</span>
        Account is active
    </div>

    <div class="security-item">
        <span>✓</span>
        Login activity is monitored
    </div>

    <div class="security-item security-warning-item">
        <span>!</span>
        Two-factor authentication is not configured
    </div>
</div>
"""
        )