#!/bin/bash
# Email sender wrapper for aventadorvr@gmail.com
# Usage: ./send-email.sh "recipient@example.com" "Subject line" "Email body text"

RECIPIENT=$1
SUBJECT=$2
BODY=$3

if [ -z "$RECIPIENT" ] || [ -z "$SUBJECT" ] || [ -z "$BODY" ]; then
    echo "Usage: $0 \"recipient@example.com\" \"Subject\" \"Body text\""
    exit 1
fi

if [ -z "$MSMTP_PASSWORD" ]; then
    echo "Error: MSMTP_PASSWORD environment variable not set"
    echo "Set it with: export MSMTP_PASSWORD='your_gmail_app_password'"
    exit 1
fi

echo "$BODY" | mail -s "$SUBJECT" "$RECIPIENT"

if [ $? -eq 0 ]; then
    echo "✅ Email sent successfully to $RECIPIENT"
else
    echo "❌ Failed to send email"
    echo "Check logs: ~/.msmtp.log"
fi
