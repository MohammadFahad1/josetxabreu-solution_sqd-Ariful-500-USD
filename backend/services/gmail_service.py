import imaplib
import smtplib
import email
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import decode_header
from typing import Optional
from dataclasses import dataclass
import re

# Set default timeout for IMAP/SMTP connections
socket.setdefaulttimeout(30)


@dataclass
class EmailMessage:
    id: str
    from_address: str
    from_name: str
    to_address: str
    subject: str
    body: str
    html_body: Optional[str]
    date: str
    thread_id: Optional[str] = None


class GmailService:
    def __init__(self, email_address: str, app_password: str):
        self.email_address = email_address
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

    def _decode_header_value(self, value: str) -> str:
        """Decode email header value."""
        if value is None:
            return ""
        decoded_parts = decode_header(value)
        result = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                result.append(part.decode(encoding or "utf-8", errors="replace"))
            else:
                result.append(part)
        return "".join(result)

    def _extract_email_address(self, from_header: str) -> tuple[str, str]:
        """Extract name and email from From header."""
        from_header = self._decode_header_value(from_header)
        match = re.search(r"<(.+?)>", from_header)
        if match:
            email_addr = match.group(1)
            name = from_header.replace(f"<{email_addr}>", "").strip().strip('"')
            return name, email_addr
        return "", from_header.strip()

    def _get_email_body(self, msg: email.message.Message) -> tuple[str, Optional[str]]:
        """Extract plain text and HTML body from email."""
        plain_body = ""
        html_body = None

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                if "attachment" in content_disposition:
                    continue

                try:
                    body = part.get_payload(decode=True)
                    if body:
                        charset = part.get_content_charset() or "utf-8"
                        body_text = body.decode(charset, errors="replace")

                        if content_type == "text/plain":
                            plain_body = body_text
                        elif content_type == "text/html":
                            html_body = body_text
                except Exception:
                    continue
        else:
            content_type = msg.get_content_type()
            try:
                body = msg.get_payload(decode=True)
                if body:
                    charset = msg.get_content_charset() or "utf-8"
                    body_text = body.decode(charset, errors="replace")
                    if content_type == "text/plain":
                        plain_body = body_text
                    elif content_type == "text/html":
                        html_body = body_text
            except Exception:
                pass

        return plain_body, html_body

    def fetch_unread_emails(self, mark_as_read: bool = False) -> list[EmailMessage]:
        """Fetch unread emails from inbox. Uses Gmail X-GM-THRID for thread tracking."""
        emails = []

        try:
            imap = imaplib.IMAP4_SSL(self.imap_server)
            imap.login(self.email_address, self.app_password)
            imap.select("INBOX")

            status, messages = imap.search(None, "UNSEEN")
            if status != "OK":
                return emails

            email_ids = messages[0].split()

            for i, email_id in enumerate(email_ids):
                # Fetch RFC822 + Gmail thread ID
                status, msg_data = imap.fetch(email_id, "(X-GM-THRID RFC822)")
                if status != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Parse X-GM-THRID from the IMAP response header
                        header_part = response_part[0]
                        if isinstance(header_part, bytes):
                            header_part = header_part.decode("utf-8", errors="replace")
                        thrid_match = re.search(r"X-GM-THRID (\d+)", header_part)
                        gmail_thread_id = thrid_match.group(1) if thrid_match else None

                        msg = email.message_from_bytes(response_part[1])

                        from_name, from_address = self._extract_email_address(
                            msg.get("From", "")
                        )
                        to_address = self._decode_header_value(msg.get("To", ""))
                        subject = self._decode_header_value(msg.get("Subject", ""))
                        date_str = msg.get("Date", "")
                        message_id = msg.get("Message-ID", str(email_id.decode()))

                        plain_body, html_body = self._get_email_body(msg)

                        emails.append(
                            EmailMessage(
                                id=message_id,
                                from_address=from_address,
                                from_name=from_name,
                                to_address=to_address,
                                subject=subject,
                                body=plain_body,
                                html_body=html_body,
                                date=date_str,
                                thread_id=gmail_thread_id,
                            )
                        )

                        if not mark_as_read:
                            imap.store(email_id, "-FLAGS", "\\Seen")

            imap.logout()

        except Exception as e:
            print(f"❌ Error fetching emails: {e}")
            raise

        return emails

    def _find_all_mail_folder(self, imap) -> str:
        """Find the Gmail All Mail folder name (handles localization)."""
        try:
            status, folders = imap.list("", "[Gmail]/*")
            if status == "OK" and folders:
                for folder in folders:
                    if folder:
                        folder_str = folder.decode() if isinstance(folder, bytes) else str(folder)
                        if "\\All" in folder_str:
                            # Extract the quoted folder name
                            match = re.search(r'"([^"]*)"$', folder_str)
                            if match:
                                return match.group(1)
        except Exception:
            pass
        return "[Gmail]/All Mail"

    def fetch_thread_emails(self, subject: str, from_address: str, gmail_thread_id: str = None) -> list[EmailMessage]:
        """Fetch all emails in a thread using Gmail's X-GM-THRID.
        Falls back to subject search if X-GM-THRID is not available."""
        thread_emails = []

        try:
            imap = imaplib.IMAP4_SSL(self.imap_server)
            imap.login(self.email_address, self.app_password)

            email_ids = []

            # Primary: Use Gmail's X-GM-THRID for reliable thread fetching
            if gmail_thread_id:
                all_mail = self._find_all_mail_folder(imap)
                status, _ = imap.select(f'"{all_mail}"', readonly=True)
                if status == "OK":
                    status, messages = imap.search(None, f"X-GM-THRID {gmail_thread_id}")
                    if status == "OK" and messages[0]:
                        email_ids = messages[0].split()
                        print(f"  → X-GM-THRID {gmail_thread_id}: found {len(email_ids)} emails in thread")

            # Fallback: Subject-based search in INBOX
            if not email_ids:
                imap.select("INBOX", readonly=True)
                clean_subject = subject
                for prefix in ["Re:", "RE:", "Fwd:", "FWD:", "Fw:"]:
                    clean_subject = clean_subject.replace(prefix, "").strip()

                if clean_subject and clean_subject.lower() not in ["(no subject)", "no subject", ""]:
                    status, messages = imap.search(None, f'SUBJECT "{clean_subject}"')
                    if status == "OK" and messages[0]:
                        email_ids = messages[0].split()
                        print(f"  → Subject fallback: found {len(email_ids)} emails")

            for email_id in email_ids:
                status, msg_data = imap.fetch(email_id, "(RFC822)")
                if status != "OK":
                    continue

                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        from_name, email_from = self._extract_email_address(msg.get("From", ""))
                        to_address = self._decode_header_value(msg.get("To", ""))
                        subj = self._decode_header_value(msg.get("Subject", ""))
                        date_str = msg.get("Date", "")
                        message_id = msg.get("Message-ID", str(email_id.decode() if isinstance(email_id, bytes) else email_id))

                        plain_body, html_body = self._get_email_body(msg)

                        thread_emails.append(
                            EmailMessage(
                                id=message_id,
                                from_address=email_from,
                                from_name=from_name,
                                to_address=to_address,
                                subject=subj,
                                body=plain_body,
                                html_body=html_body,
                                date=date_str,
                                thread_id=gmail_thread_id,
                            )
                        )

            imap.logout()

        except Exception as e:
            print(f"❌ Error fetching thread: {e}")

        return thread_emails

    def send_email(
        self,
        to_address: str,
        subject: str,
        body_text: str,
        body_html: Optional[str] = None,
        reply_to_message_id: Optional[str] = None,
    ) -> bool:
        """Send an email."""
        try:
            msg = MIMEMultipart("alternative")
            msg["From"] = self.email_address
            msg["To"] = to_address
            msg["Subject"] = subject

            if reply_to_message_id:
                msg["In-Reply-To"] = reply_to_message_id
                msg["References"] = reply_to_message_id

            # Attach plain text
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            # Attach HTML if provided
            if body_html:
                msg.attach(MIMEText(body_html, "html", "utf-8"))

            # Send via SMTP SSL (port 465)
            with smtplib.SMTP_SSL(self.smtp_server, 465, timeout=60) as server:
                server.login(self.email_address, self.app_password)
                server.sendmail(self.email_address, to_address, msg.as_string())

            return True

        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def mark_as_read(self, email_id: str) -> bool:
        """Mark a specific email as read."""
        try:
            imap = imaplib.IMAP4_SSL(self.imap_server)
            imap.login(self.email_address, self.app_password)
            imap.select("INBOX")

            # Search for the email by Message-ID
            status, messages = imap.search(None, f'HEADER Message-ID "{email_id}"')
            if status == "OK" and messages[0]:
                for msg_id in messages[0].split():
                    imap.store(msg_id, "+FLAGS", "\\Seen")

            imap.logout()
            return True
        except Exception as e:
            print(f"Error marking email as read: {e}")
            return False
