"""LangChain agent for parsing rental request emails."""

import json
from typing import Optional
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel

from .prompts import EMAIL_PARSER_SYSTEM_PROMPT, ACCEPTANCE_DETECTION_PROMPT
from .email_templates import generate_missing_info_html, generate_missing_info_plain_text


class ExtractedData(BaseModel):
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    client_vat: Optional[str] = None
    client_phone: Optional[str] = None
    pickup_date: Optional[str] = None
    return_date: Optional[str] = None
    pickup_location: Optional[str] = None
    return_location: Optional[str] = None
    vehicle_type: Optional[str] = None
    special_requests: Optional[str] = None
    driver_name: Optional[str] = None
    artist_project_event: Optional[str] = None
    destination_cities: Optional[str] = None


class ParseResult(BaseModel):
    complete: bool
    extracted_data: ExtractedData
    missing_fields: list[str]
    confidence: float
    summary: str
    is_rental_request: bool = True  # Is this actually a van rental request?


class AcceptanceResult(BaseModel):
    is_acceptance: bool
    confidence: float
    modifications_requested: list[str]
    questions: list[str]
    summary: str


class EmailParserAgent:
    def __init__(self, openai_api_key: str, model: str = "gpt-5.2"):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model=model,
            temperature=0.1,
        )

    def parse_rental_request(
        self,
        email_body: str,
        email_subject: str,
        from_address: str,
        from_name: str = "",
    ) -> ParseResult:
        """Parse a rental request email and extract information."""

        user_message = f"""Please analyze this rental request email and extract all relevant information.

IMPORTANT: The email body below may contain MULTIPLE messages from the same client (separated by ---). You MUST combine information from ALL messages to build the complete picture. If a field was mentioned in ANY message, it is NOT missing.

From: {from_name} <{from_address}>
Subject: {email_subject}

Email Body:
{email_body}

Today's date is: {datetime.now().strftime("%Y-%m-%d")}

Return a JSON object with the extracted information.
"""

        messages = [
            SystemMessage(content=EMAIL_PARSER_SYSTEM_PROMPT),
            HumanMessage(content=user_message),
        ]

        response = self.llm.invoke(messages)
        content = response.content

        # Parse JSON from response
        try:
            # Try to extract JSON from the response
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            data = json.loads(json_str)

            # Override email with the actual from address
            if data.get("extracted_data"):
                data["extracted_data"]["client_email"] = from_address
                if not data["extracted_data"].get("client_name") and from_name:
                    data["extracted_data"]["client_name"] = from_name

                # Convert any list fields to comma-separated strings
                for field in ["destination_cities", "special_requests"]:
                    val = data["extracted_data"].get(field)
                    if isinstance(val, list):
                        data["extracted_data"][field] = ", ".join(str(v) for v in val)

            return ParseResult(
                complete=data.get("complete", False),
                extracted_data=ExtractedData(**data.get("extracted_data", {})),
                missing_fields=data.get("missing_fields", []),
                confidence=data.get("confidence", 0.5),
                summary=data.get("summary", ""),
                is_rental_request=data.get("is_rental_request", True),
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing LLM response: {e}")
            # Return a minimal result with just the email
            return ParseResult(
                complete=False,
                extracted_data=ExtractedData(
                    client_email=from_address,
                    client_name=from_name or None,
                ),
                missing_fields=["pickup_date", "return_date", "pickup_location"],
                confidence=0.0,
                summary="Failed to parse email automatically",
                is_rental_request=False,
            )

    def generate_missing_info_email(
        self,
        original_email: str,
        missing_fields: list[str],
        client_name: Optional[str],
        company_email: str,
    ) -> tuple[str, Optional[str]]:
        """Generate an email requesting missing information.

        Returns: (plain_text, html_text)
        """

        plain_text = generate_missing_info_plain_text(
            client_name=client_name or "",
            missing_fields=missing_fields,
        )

        html_text = generate_missing_info_html(
            client_name=client_name or "",
            missing_fields=missing_fields,
        )

        return plain_text, html_text

    def detect_acceptance(self, email_body: str, email_subject: str) -> AcceptanceResult:
        """Detect if an email is accepting a proposal."""

        user_message = f"""Please analyze this email response to determine if the client is accepting a rental proposal.

Subject: {email_subject}

Email Body:
{email_body}

Return a JSON object with your analysis.
"""

        messages = [
            SystemMessage(content=ACCEPTANCE_DETECTION_PROMPT),
            HumanMessage(content=user_message),
        ]

        response = self.llm.invoke(messages)
        content = response.content

        try:
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()

            data = json.loads(json_str)

            return AcceptanceResult(
                is_acceptance=data.get("is_acceptance", False),
                confidence=data.get("confidence", 0.5),
                modifications_requested=data.get("modifications_requested", []),
                questions=data.get("questions", []),
                summary=data.get("summary", ""),
            )
        except (json.JSONDecodeError, KeyError):
            return AcceptanceResult(
                is_acceptance=False,
                confidence=0.0,
                modifications_requested=[],
                questions=[],
                summary="Failed to analyze response",
            )
