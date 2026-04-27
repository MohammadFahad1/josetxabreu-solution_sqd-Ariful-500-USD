"""Google Sheets integration for logging."""

import json
from datetime import datetime
from typing import Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build


class SheetsService:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    # Column headers for the rental log sheet
    HEADERS = [
        "Request ID",
        "Client Name",
        "Client Email",
        "Client VAT",
        "Pickup Date",
        "Return Date",
        "Pickup Location",
        "Return Location",
        "Vehicle Type",
        "Partner",
        "Price",
        "Status",
        "Invoice Number",
        "Created At",
        "Updated At",
    ]

    def __init__(self, spreadsheet_id: str, service_account_json: str):
        self.spreadsheet_id = spreadsheet_id
        self.service_account_json = service_account_json
        self._service = None

    @property
    def service(self):
        """Lazy initialization of the Sheets service."""
        if self._service is None:
            if self.service_account_json.startswith("{"):
                # JSON string
                creds_info = json.loads(self.service_account_json)
            else:
                # File path
                with open(self.service_account_json) as f:
                    creds_info = json.load(f)

            credentials = service_account.Credentials.from_service_account_info(
                creds_info, scopes=self.SCOPES
            )
            self._service = build("sheets", "v4", credentials=credentials)

        return self._service

    def _ensure_headers(self, sheet_name: str = "Rentals"):
        """Ensure the sheet has headers."""
        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1:O1")
                .execute()
            )

            values = result.get("values", [])
            if not values or values[0] != self.HEADERS:
                # Add headers
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{sheet_name}!A1:O1",
                    valueInputOption="RAW",
                    body={"values": [self.HEADERS]},
                ).execute()
        except Exception:
            # Sheet might not exist, try to add headers anyway
            try:
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"{sheet_name}!A1:O1",
                    valueInputOption="RAW",
                    body={"values": [self.HEADERS]},
                ).execute()
            except Exception as e:
                print(f"Failed to set headers: {e}")

    def log_request(
        self,
        request_id: str,
        client_name: Optional[str],
        client_email: str,
        client_vat: Optional[str],
        pickup_date: Optional[str],
        return_date: Optional[str],
        pickup_location: Optional[str],
        return_location: Optional[str],
        vehicle_type: Optional[str],
        partner: Optional[str],
        price: Optional[float],
        status: str,
        invoice_number: Optional[str] = None,
        sheet_name: str = "Rentals",
    ) -> bool:
        """Log a rental request to the sheet."""
        try:
            self._ensure_headers(sheet_name)

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

            row = [
                request_id,
                client_name or "",
                client_email,
                client_vat or "",
                pickup_date or "",
                return_date or "",
                pickup_location or "",
                return_location or "",
                vehicle_type or "",
                partner or "",
                str(price) if price else "",
                status,
                invoice_number or "",
                now,
                now,
            ]

            self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A:O",
                valueInputOption="RAW",
                insertDataOption="INSERT_ROWS",
                body={"values": [row]},
            ).execute()

            return True

        except Exception as e:
            print(f"Failed to log request: {e}")
            return False

    def update_request_status(
        self,
        request_id: str,
        status: str,
        partner: Optional[str] = None,
        price: Optional[float] = None,
        invoice_number: Optional[str] = None,
        sheet_name: str = "Rentals",
    ) -> bool:
        """Update an existing request in the sheet."""
        try:
            # Find the row with this request ID
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A:O")
                .execute()
            )

            values = result.get("values", [])

            for i, row in enumerate(values):
                if row and row[0] == request_id:
                    # Found the row, update it
                    row_num = i + 1
                    print(f"📊 Updating sheet row {row_num} for request {request_id[:8]}...")

                    # Update status (column L = 12)
                    updates = [(f"{sheet_name}!L{row_num}", [[status]])]

                    if partner:
                        updates.append((f"{sheet_name}!J{row_num}", [[partner]]))
                    if price is not None:
                        updates.append((f"{sheet_name}!K{row_num}", [[str(price)]]))
                    if invoice_number:
                        updates.append((f"{sheet_name}!M{row_num}", [[invoice_number]]))

                    # Update timestamp
                    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    updates.append((f"{sheet_name}!O{row_num}", [[now]]))

                    # Batch update
                    batch_data = [
                        {"range": r, "values": v} for r, v in updates
                    ]

                    self.service.spreadsheets().values().batchUpdate(
                        spreadsheetId=self.spreadsheet_id,
                        body={"valueInputOption": "RAW", "data": batch_data},
                    ).execute()

                    print(f"  → Sheet updated: status={status}, partner={partner}, price={price}")
                    return True

            print(f"⚠️ Request {request_id[:8]} not found in sheet - cannot update")
            return False

        except Exception as e:
            print(f"Failed to update request: {e}")
            return False
