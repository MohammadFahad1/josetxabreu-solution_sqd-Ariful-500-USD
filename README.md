# Van Rental Automation

Automated email processing system for van rental requests with human-in-the-loop partner selection.

## Features

- **Email Processing**: Automatically reads incoming rental requests from Gmail
- **AI Parsing**: Uses LangChain + GPT to extract rental details from emails
- **Missing Info Detection**: Auto-replies to request missing information
- **Human-in-the-Loop**: Staff selects rent-a-car partner via dashboard
- **Proposal Generation**: Creates professional HTML proposals
- **Acceptance Detection**: AI detects when clients accept proposals
- **Logging**: Tracks all requests in Google Sheets

## Setup

### 1. Prerequisites

- Python 3.11+
- Node.js 20+
- Docker (optional)

### 2. Gmail App Password

1. Go to Google Account → Security → 2-Step Verification
2. At the bottom, click "App passwords"
3. Create a new app password for "Mail"
4. Copy the 16-character password

### 3. Google Sheets (Optional)

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account
4. Download the JSON key file
5. Share your spreadsheet with the service account email

### 4. Environment Variables

Copy `.env.example` to `.env` and fill in:

```bash
cp .env.example .env
```

Required variables:
- `GMAIL_ADDRESS` - Your Gmail address
- `GMAIL_APP_PASSWORD` - Gmail app password (16 chars)
- `OPENAI_API_KEY` - OpenAI API key

## Running

### With Docker

```bash
docker-compose up --build
```

### Without Docker

Backend:
```bash
cd backend
pip install -r requirements.txt
uvicorn backend.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Open dashboard: http://localhost:3000
2. Click "Check Emails" to process new requests
3. Click on a request to view details
4. Select a rent-a-car partner and set price
5. Click "Send Proposal"
6. When client accepts, click "Mark as Accepted"
7. Click "Confirm Booking"

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/requests` | GET | List all requests |
| `/api/requests/{id}` | GET | Get request details |
| `/api/requests/{id}/select-partner` | POST | Select rent-a-car partner |
| `/api/requests/{id}/send-proposal` | POST | Send proposal email |
| `/api/requests/{id}/mark-accepted` | POST | Mark as accepted |
| `/api/requests/{id}/confirm` | POST | Confirm booking |
| `/api/partners` | GET | List rent-a-car partners |
| `/api/process-emails` | POST | Process unread emails |
| `/api/check-acceptances` | POST | Check for acceptance emails |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          Gmail Inbox                              │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI Backend                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ Gmail       │  │ LangChain   │  │ Proposal    │              │
│  │ Service     │  │ Agent       │  │ Generator   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐                                                  │
│  │ Sheets      │                                                  │
│  │ Service     │                                                  │
│  └─────────────┘                                                  │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  Next.js Dashboard (Human-in-the-Loop)                           │
│  - View requests                                                  │
│  - Select rent-a-car partner                                      │
│  - Send proposals                                                 │
│  - Confirm bookings                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Workflow

1. **Email Arrives** → Agent parses, extracts info
2. **Missing Info?** → Auto-reply asking for details
3. **Complete Info** → Request appears in dashboard
4. **Staff Selects Partner** → Sets price, chooses rent-a-car
5. **Send Proposal** → Professional HTML email sent
6. **Client Accepts** → Agent detects acceptance
7. **Staff Confirms** → Booking finalized
8. **Confirmation Sent** → Client receives booking details
# automation-agent
