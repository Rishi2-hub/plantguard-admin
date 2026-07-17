import pandas as pd
import streamlit as st


def initialize_treatments() -> None:
    if "treatments_data" not in st.session_state:
        st.session_state.treatments_data = [
            {
                "id": 1,
                "disease": "Tomato Late Blight",
                "crop": "Tomato",
                "severity": "High",
                "pesticide": "Mancozeb",
                "dosage": "2.5 g/L",
                "status": "Active",
            },
            {
                "id": 2,
                "disease": "Tomato Early Blight",
                "crop": "Tomato",
                "severity": "Medium",
                "pesticide": "Chlorothalonil",
                "dosage": "2 ml/L",
                "status": "Active",
            },
            {
                "id": 3,
                "disease": "Potato Late Blight",
                "crop": "Potato",
                "severity": "High",
                "pesticide": "Metalaxyl",
                "dosage": "2 g/L",
                "status": "Active",
            },
            {
                "id": 4,
                "disease": "Bacterial Spot",
                "crop": "Bell Pepper",
                "severity": "Medium",
                "pesticide": "Copper Fungicide",
                "dosage": "3 g/L",
                "status": "Active",
            },
            {
                "id": 5,
                "disease": "Spider Mites",
                "crop": "Tomato",
                "severity": "Low",
                "pesticide": "Neem Oil",
                "dosage": "5 ml/L",
                "status": "Inactive",
            },
        ]


def treatments_page() -> None:
    initialize_treatments()

    st.html(
        """
<div class="page-heading">
    <div>
        <div class="page-title">Treatment Management</div>
        <div class="page-subtitle">
            View, update, and deactivate disease-treatment records.
        </div>
    </div>

    <div class="page-badge">
        💊 Treatment Records
    </div>
</div>
"""
    )

    treatments = pd.DataFrame(st.session_state.treatments_data)

    # Filters
    search_col, crop_col, status_col = st.columns(
        [2, 1, 1],
        gap="medium",
    )

    with search_col:
        search_text = st.text_input(
            "Search treatments",
            placeholder="Search disease, pesticide, crop, or dosage...",
        )

    with crop_col:
        crop_options = ["All"] + sorted(
            treatments["crop"].unique().tolist()
        )

        selected_crop = st.selectbox(
            "Crop",
            crop_options,
        )

    with status_col:
        selected_status = st.selectbox(
            "Status",
            ["All", "Active", "Inactive"],
        )

    filtered = treatments.copy()

    if search_text.strip():
        search_value = search_text.strip().lower()

        filtered = filtered[
            filtered.apply(
                lambda row: search_value
                in " ".join(row.astype(str)).lower(),
                axis=1,
            )
        ]

    if selected_crop != "All":
        filtered = filtered[
            filtered["crop"] == selected_crop
        ]

    if selected_status != "All":
        filtered = filtered[
            filtered["status"] == selected_status
        ]

    # Summary cards
    total_count = len(treatments)

    active_count = len(
        treatments[treatments["status"] == "Active"]
    )

    inactive_count = len(
        treatments[treatments["status"] == "Inactive"]
    )

    summary1, summary2, summary3 = st.columns(
        3,
        gap="medium",
    )

    with summary1:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-blue">💊</div>
    <div>
        <div class="summary-label">Total Treatments</div>
        <div class="summary-value">{total_count}</div>
    </div>
</div>
"""
        )

    with summary2:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-green">✓</div>
    <div>
        <div class="summary-label">Active Treatments</div>
        <div class="summary-value">{active_count}</div>
    </div>
</div>
"""
        )

    with summary3:
        st.html(
            f"""
<div class="summary-card">
    <div class="summary-icon summary-red">×</div>
    <div>
        <div class="summary-label">Inactive Treatments</div>
        <div class="summary-value">{inactive_count}</div>
    </div>
</div>
"""
        )

    st.html(
        """
<div class="section-panel-heading">
    <div class="panel-title">Treatment Records</div>
    <div class="panel-subtitle">
        Use the filters above to find a treatment.
    </div>
</div>
"""
    )

    display_data = filtered.rename(
        columns={
            "id": "ID",
            "disease": "Disease",
            "crop": "Crop",
            "severity": "Severity",
            "pesticide": "Pesticide",
            "dosage": "Dosage",
            "status": "Status",
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )

    if filtered.empty:
        st.warning("No treatment records match your filters.")
        return

    # Edit treatment
    st.html(
        """
<div class="section-panel-heading form-heading">
    <div class="panel-title">Edit Treatment</div>
    <div class="panel-subtitle">
        Select a record and modify its details.
    </div>
</div>
"""
    )

    treatment_options = {
        f"{row['disease']} — {row['crop']} (ID {row['id']})": row["id"]
        for _, row in filtered.iterrows()
    }

    selected_label = st.selectbox(
        "Select treatment",
        list(treatment_options.keys()),
    )

    selected_id = treatment_options[selected_label]

    selected_record = next(
        item
        for item in st.session_state.treatments_data
        if item["id"] == selected_id
    )

    crop_values = ["Tomato", "Potato", "Bell Pepper"]
    severity_values = ["Low", "Medium", "High"]
    status_values = ["Active", "Inactive"]

    with st.form(
        f"edit_treatment_{selected_id}",
        clear_on_submit=False,
    ):
        disease = st.text_input(
            "Disease",
            value=selected_record["disease"],
        )

        crop = st.selectbox(
            "Crop",
            crop_values,
            index=crop_values.index(
                selected_record["crop"]
            ),
        )

        severity = st.selectbox(
            "Severity",
            severity_values,
            index=severity_values.index(
                selected_record["severity"]
            ),
        )

        pesticide = st.text_input(
            "Pesticide",
            value=selected_record["pesticide"],
        )

        dosage = st.text_input(
            "Dosage",
            value=selected_record["dosage"],
        )

        status = st.selectbox(
            "Status",
            status_values,
            index=status_values.index(
                selected_record["status"]
            ),
        )

        save_clicked = st.form_submit_button(
            "Save Treatment Changes",
            use_container_width=True,
        )

        if save_clicked:
            if not disease.strip():
                st.error("Disease name is required.")

            elif not pesticide.strip():
                st.error("Pesticide name is required.")

            elif not dosage.strip():
                st.error("Dosage is required.")

            else:
                selected_record.update(
                    {
                        "disease": disease.strip(),
                        "crop": crop,
                        "severity": severity,
                        "pesticide": pesticide.strip(),
                        "dosage": dosage.strip(),
                        "status": status,
                    }
                )

                st.success("Treatment updated successfully.")
                st.rerun()

    # Deactivation
    st.html(
        """
<div class="danger-panel">
    <div class="danger-title">Deactivate Treatment</div>
    <div class="danger-description">
        This performs a soft deletion and keeps the record in the system.
    </div>
</div>
"""
    )

    confirmation = st.checkbox(
        "I confirm that I want to deactivate this treatment.",
        key=f"treatment_confirmation_{selected_id}",
        disabled=selected_record["status"] == "Inactive",
    )

    if st.button(
        "🚫 Deactivate Treatment",
        use_container_width=True,
        key=f"deactivate_treatment_{selected_id}",
        disabled=(
            selected_record["status"] == "Inactive"
            or not confirmation
        ),
    ):
        selected_record["status"] = "Inactive"

        st.success("Treatment deactivated successfully.")
        st.rerun()

    if selected_record["status"] == "Inactive":
        st.info("This treatment is already inactive.")