#!/usr/bin/env pwsh
# Google Speech-to-Text Transcription Script
# Usage: .\transcribe-audio.ps1 -AudioFile "path/to/audio.ogg"

param(
    [Parameter(Mandatory=$true)]
    [string]$AudioFile,
    
    [string]$ApiKey = $env:GOOGLE_SPEECH_API_KEY,
    [string]$LanguageCode = "en-US"
)

if (-not $ApiKey) {
    Write-Error "Google Speech API key not provided. Set GOOGLE_SPEECH_API_KEY environment variable or pass -ApiKey parameter."
    exit 1
}

if (-not (Test-Path $AudioFile)) {
    Write-Error "Audio file not found: $AudioFile"
    exit 1
}

# Read audio file and convert to base64
$audioBytes = [System.IO.File]::ReadAllBytes($AudioFile)
$audioBase64 = [Convert]::ToBase64String($audioBytes)

# Determine content type based on file extension
$ext = [System.IO.Path]::GetExtension($AudioFile).ToLower()
$contentType = switch ($ext) {
    ".ogg" { "OGG_OPUS" }
    ".mp3" { "MP3" }
    ".wav" { "LINEAR16" }
    ".flac" { "FLAC" }
    default { "OGG_OPUS" }
}

# Build request body
$requestBody = @{
    config = @{
        encoding = $contentType
        sampleRateHertz = 48000
        languageCode = $LanguageCode
        enableAutomaticPunctuation = $true
        model = "latest_long"
        useEnhanced = $true
    }
    audio = @{
        content = $audioBase64
    }
} | ConvertTo-Json -Depth 10

# Call Google Speech API
try {
    $uri = "https://speech.googleapis.com/v1/speech:recognize?key=$ApiKey"
    $response = Invoke-RestMethod -Uri $uri -Method POST -ContentType "application/json" -Body $requestBody
    
    if ($response.results) {
        $transcript = $response.results[0].alternatives[0].transcript
        $confidence = $response.results[0].alternatives[0].confidence
        
        Write-Output "TRANSCRIPT: $transcript"
        Write-Output "CONFIDENCE: $($confidence * 100)%"
    } else {
        Write-Output "No speech detected in audio file."
    }
} catch {
    Write-Error "Transcription failed: $($_.Exception.Message)"
    exit 1
}
