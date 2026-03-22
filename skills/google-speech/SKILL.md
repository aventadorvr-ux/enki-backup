# Google Speech-to-Text Skill

Transcribe audio files using Google Cloud Speech-to-Text API.

## Usage

Configure in `openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "google-speech": {
        "apiKey": "YOUR_GOOGLE_API_KEY",
        "languageCode": "en-US"
      }
    }
  }
}
```

## API

### Transcribe Audio

The skill automatically processes incoming audio messages from Telegram.

**Supported formats:**
- `.ogg` (Telegram voice messages)
- `.mp3`
- `.wav`
- `.flac`

## Response Format

Returns transcribed text or error message.

## Error Handling

- Invalid API key → "Speech API authentication failed"
- Unsupported format → "Audio format not supported"
- API quota exceeded → "Speech API quota exceeded"
- Network error → "Transcription service unavailable"

## Privacy Note

Audio files are sent to Google Cloud for transcription. Do not use for sensitive/private content unless you trust Google's privacy policies.
