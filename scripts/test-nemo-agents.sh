#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:8000/api/v1/agents"

echo "== health =="
curl -fsS http://127.0.0.1:8000/health
echo
echo

echo "== agents =="
curl -fsS http://127.0.0.1:8000/api/v1/agents
echo
echo

echo "== market_intel =="
curl -fsS -X POST "$BASE/market_intel/process" \
  -H "Content-Type: application/json" \
  -d '{"action":"trends","suburb":"Auckland Central"}'
echo
echo

echo "== content =="
curl -fsS -X POST "$BASE/content/process" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"description_ai",
    "bedrooms":4,
    "bathrooms":2,
    "location":"Parnell, Auckland",
    "features":["modern kitchen","garage","city views"]
  }'
echo
echo

echo "== lead =="
curl -fsS -X POST "$BASE/lead/process" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"qualify_ai",
    "budget":850000,
    "timeline":"3 months",
    "pre_approved":true,
    "notes":"Looking for a 3 bedroom family home in Auckland",
    "lead_id":"test_001"
  }'
echo
echo

echo "== transaction =="
curl -fsS -X POST "$BASE/transaction/process" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"risk_assessment",
    "transaction_id":"txn_001",
    "days_to_settlement":14,
    "finance_approved":false,
    "building_report_complete":false,
    "lawyer_assigned":true
  }'
echo
echo

echo "== scheduling =="
curl -fsS -X POST "$BASE/scheduling/process" \
  -H "Content-Type: application/json" \
  -d '{
    "action":"availability",
    "date":"2026-04-06"
  }'
echo
echo

echo "ALL REQUESTS COMPLETED"
