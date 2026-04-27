"""LangChain agent for generating rental proposals."""

from datetime import date
from typing import Optional

from .email_templates import (
    generate_proposal_html,
    generate_proposal_plain_text,
    generate_confirmation_html,
    generate_confirmation_plain_text,
)


class ProposalGenerator:
    def __init__(self, openai_api_key: str, model: str = "gpt-5.1"):
        # Keep API key for potential future AI-generated content
        self.openai_api_key = openai_api_key
        self.model = model

    def generate_proposal(
        self,
        client_name: str,
        client_email: str,
        pickup_date: date,
        return_date: date,
        pickup_location: str,
        return_location: str,
        vehicle_type: str,
        partner_name: str,
        price: float,
        special_requests: Optional[str] = None,
        original_email_language: str = "auto",
    ) -> tuple[str, Optional[str]]:
        """Generate a proposal email.

        Returns: (plain_text, html_text)
        """

        plain_text = generate_proposal_plain_text(
            client_name=client_name,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            return_location=return_location or pickup_location,
            vehicle_type=vehicle_type,
            partner_name=partner_name,
            price=price,
        )

        html_text = generate_proposal_html(
            client_name=client_name,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            return_location=return_location or pickup_location,
            vehicle_type=vehicle_type,
            partner_name=partner_name,
            price=price,
        )

        return plain_text, html_text

    def generate_confirmation_email(
        self,
        client_name: str,
        pickup_date: date,
        return_date: date,
        pickup_location: str,
        return_location: str,
        vehicle_type: str,
        partner_name: str,
        price: float,
        invoice_number: Optional[str] = None,
    ) -> tuple[str, Optional[str]]:
        """Generate a booking confirmation email.

        Returns: (plain_text, html_text)
        """

        plain_text = generate_confirmation_plain_text(
            client_name=client_name,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            return_location=return_location or pickup_location,
            vehicle_type=vehicle_type,
            partner_name=partner_name,
            price=price,
        )

        html_text = generate_confirmation_html(
            client_name=client_name,
            pickup_date=pickup_date,
            return_date=return_date,
            pickup_location=pickup_location,
            return_location=return_location or pickup_location,
            vehicle_type=vehicle_type,
            partner_name=partner_name,
            price=price,
        )

        return plain_text, html_text
