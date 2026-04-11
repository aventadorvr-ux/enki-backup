# Frontend ↔ Backend Contract

## Backend base URL
http://127.0.0.1:8000/api/v1/agents

## Available endpoints

### market_intel
POST /market_intel/process
Payload:
{
  "action": "trends",
  "suburb": "Auckland Central"
}

### content
POST /content/process
Payload:
{
  "action": "description_ai",
  "bedrooms": number,
  "bathrooms": number,
  "location": string,
  "features": []
}

### lead
POST /lead/process

### transaction
POST /transaction/process

### scheduling
POST /scheduling/process

## Integration goal

Frontend must:
- call backend endpoints
- display results in UI
- handle loading + error states

## First integration target

Connect:
- homepage OR dashboard
→ content agent endpoint

Display:
- generated property description
