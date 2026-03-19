#!/data/data/com.termux/files/usr/bin/bash
# Quick voice-to-text for OpenClaw

echo "Recording for 5 seconds..."
termux-microphone-record -l 5 -f /sdcard/openclaw_voice.wav

echo "Transcribing..."
# Using OpenAI Whisper API or local fallback
if [ -n "$OPENAI_API_KEY" ]; then
  curl -s https://api.openai.com/v1/audio/transcriptions \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: multipart/form-data" \
    -F file="@/sdcard/openclaw_voice.wav" \
    -F model="whisper-1" | jq -r '.text'
else
  echo "Set OPENAI_API_KEY for transcription"
fi