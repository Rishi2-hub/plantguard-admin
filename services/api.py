import os
from typing import Any

import requests


BASE_URL = os.getenv(
    "PLANTGUARD_API_URL",
    "http://localhost:8000/api/v1",
)

USE_MOCK_API = True
REQUEST_TIMEOUT = 15


class APIError(Exception):
    """Raised when a PlantGuard API request fails."""


# ------------------------------------------------------------------
# Shared request helpers
# ------------------------------------------------------------------

def get_headers(access_token: str | None = None) -> dict[str, str]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    return headers


def parse_response(response: requests.Response) -> Any:
    try:
        data = response.json()
    except ValueError:
        data = None

    if response.ok:
        return data

    if isinstance(data, dict):
        message = data.get("detail", "The request failed.")
    else:
        message = (
            response.text.strip()
            or f"Request failed with status {response.status_code}."
        )

    raise APIError(message)


def request_api(
    method: str,
    endpoint: str,
    access_token: str | None = None,
    payload: dict[str, Any] | None = None,
    params: dict[str, Any] | None = None,
) -> Any:
    try:
        response = requests.request(
            method=method,
            url=f"{BASE_URL}{endpoint}",
            json=payload,
            params=params,
            headers=get_headers(access_token),
            timeout=REQUEST_TIMEOUT,
        )

        return parse_response(response)

    except requests.ConnectionError as exc:
        raise APIError(
            "Could not connect to the PlantGuard backend. "
            "Make sure FastAPI is running on port 8000."
        ) from exc

    except requests.Timeout as exc:
        raise APIError(
            "The backend took too long to respond."
        ) from exc

    except requests.RequestException as exc:
        raise APIError(
            f"Backend request failed: {exc}"
        ) from exc


# ------------------------------------------------------------------
# Authentication
# ------------------------------------------------------------------

def login_admin(email: str, password: str) -> dict[str, Any]:
    if USE_MOCK_API:
        if (
            email.lower() == "admin@plantguard.com"
            and password == "admin123"
        ):
            return {
                "access_token": "temporary-access-token",
                "refresh_token": "temporary-refresh-token",
                "role": "admin",
                "is_super_admin": True,
                "name": "Rishi Kumar",
                "email": email,
            }

        raise APIError("Invalid email or password.")

    return request_api(
        method="POST",
        endpoint="/auth/login",
        payload={
            "email": email,
            "password": password,
        },
    )


def logout_admin(access_token: str) -> dict[str, Any]:
    if USE_MOCK_API:
        return {"message": "Logged out successfully"}

    return request_api(
        method="POST",
        endpoint="/auth/logout",
        access_token=access_token,
    )


# ------------------------------------------------------------------
# Mock records
# ------------------------------------------------------------------

MOCK_TREATMENTS = [
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
]

MOCK_FARMERS = [
    {
        "id": 1,
        "name": "Ram Bahadur",
        "email": "ram@example.com",
        "joined": "2026-06-20",
        "language": "Nepali",
        "status": "Active",
    },
    {
        "id": 2,
        "name": "Sita Maya",
        "email": "sita@example.com",
        "joined": "2026-06-22",
        "language": "Nepali",
        "status": "Active",
    },
    {
        "id": 3,
        "name": "Hari Prasad",
        "email": "hari@example.com",
        "joined": "2026-06-25",
        "language": "English",
        "status": "Inactive",
    },
]

MOCK_AUDIT_LOGS = [
    {
        "id": 1,
        "event": "Treatment Updated",
        "user": "Rishi Kumar",
        "ip_address": "192.168.1.10",
        "detail": "Updated Tomato Late Blight dosage",
        "timestamp": "2026-07-11 18:35",
        "level": "Info",
    },
    {
        "id": 2,
        "event": "Failed Login",
        "user": "Unknown",
        "ip_address": "103.22.45.12",
        "detail": "Invalid administrator credentials",
        "timestamp": "2026-07-11 16:48",
        "level": "Danger",
    },
]


# ------------------------------------------------------------------
# Treatments
# ------------------------------------------------------------------

def get_treatments(access_token: str) -> list[dict[str, Any]]:
    if USE_MOCK_API:
        return MOCK_TREATMENTS.copy()

    return request_api(
        method="GET",
        endpoint="/admin/treatments",
        access_token=access_token,
    )


def update_treatment(
    treatment_id: int,
    changed_fields: dict[str, Any],
    access_token: str,
) -> dict[str, Any]:
    if USE_MOCK_API:
        for treatment in MOCK_TREATMENTS:
            if treatment["id"] == treatment_id:
                treatment.update(changed_fields)
                return treatment.copy()

        raise APIError("Treatment record was not found.")

    return request_api(
        method="PUT",
        endpoint=f"/admin/treatments/{treatment_id}",
        access_token=access_token,
        payload=changed_fields,
    )


def delete_treatment(
    treatment_id: int,
    access_token: str,
) -> dict[str, Any]:
    if USE_MOCK_API:
        for treatment in MOCK_TREATMENTS:
            if treatment["id"] == treatment_id:
                treatment["status"] = "Inactive"

                return {
                    "message": "Treatment deactivated successfully"
                }

        raise APIError("Treatment record was not found.")

    return request_api(
        method="DELETE",
        endpoint=f"/admin/treatments/{treatment_id}",
        access_token=access_token,
    )


# ------------------------------------------------------------------
# Farmers
# ------------------------------------------------------------------

def get_farmers(access_token: str) -> list[dict[str, Any]]:
    if USE_MOCK_API:
        return MOCK_FARMERS.copy()

    return request_api(
        method="GET",
        endpoint="/admin/users",
        access_token=access_token,
    )


def deactivate_farmer(
    farmer_id: int,
    access_token: str,
) -> dict[str, Any]:
    if USE_MOCK_API:
        for farmer in MOCK_FARMERS:
            if farmer["id"] == farmer_id:
                farmer["status"] = "Inactive"

                return {
                    "message": "Farmer deactivated successfully"
                }

        raise APIError("Farmer record was not found.")

    return request_api(
        method="PATCH",
        endpoint=f"/admin/users/{farmer_id}/deactivate",
        access_token=access_token,
    )


def reactivate_farmer(
    farmer_id: int,
    access_token: str,
) -> dict[str, Any]:
    if USE_MOCK_API:
        for farmer in MOCK_FARMERS:
            if farmer["id"] == farmer_id:
                farmer["status"] = "Active"

                return {
                    "message": "Farmer reactivated successfully"
                }

        raise APIError("Farmer record was not found.")

    return request_api(
        method="PATCH",
        endpoint=f"/admin/users/{farmer_id}/reactivate",
        access_token=access_token,
    )


# ------------------------------------------------------------------
# Audit logs
# ------------------------------------------------------------------

def get_audit_logs(
    access_token: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    if USE_MOCK_API:
        return MOCK_AUDIT_LOGS[:limit]

    return request_api(
        method="GET",
        endpoint="/admin/audit-logs",
        access_token=access_token,
        params={"limit": limit},
    )


# ------------------------------------------------------------------
# Add administrator
# ------------------------------------------------------------------

def create_admin(
    name: str,
    email: str,
    password: str,
    access_token: str,
) -> dict[str, Any]:
    if USE_MOCK_API:
        return {
            "message": "Administrator created successfully",
            "admin": {
                "name": name,
                "email": email,
                "role": "admin",
            },
        }

    return request_api(
        method="POST",
        endpoint="/admin/create-admin",
        access_token=access_token,
        payload={
            "name": name,
            "email": email,
            "password": password,
        },
    )