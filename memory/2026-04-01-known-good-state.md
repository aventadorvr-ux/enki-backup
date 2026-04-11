# 2026-04-01 Known Good State

## Instance
- Live EC2 instance: Enki_777

## OpenClaw state
- OpenClaw gateway healthy and running under systemd user service
- Telegram channel ON/OK for @Enki_controlbot
- Main model remains OpenRouter moonshotai/kimi-k2.5
- tools.exec configured for gateway with security=full and ask=off to restore trusted single-user Telegram exec behavior

## NEMO / ENKI runtime
- nemo-backend.service active
- nemo-frontend.service active
- openclaw-gateway.service active
- /health returns healthy
- /api/v1/enki/status returns all agents active:
  - lead_terminator
  - content_forge
  - market_intel
  - scheduler
  - transaction

## Memory
- openclaw memory status --deep shows:
  - Indexed 38/38 files
  - Dirty: no
  - Embeddings ready
  - Vector ready
  - FTS ready

## Bot behavior
- Telegram bot now executes simple bounded read-only commands again
- Verified real file read from /tmp/enki_read_test.txt
- Response-length/output-fidelity edge cases may still exist, but core trusted exec path is substantially improved

## Cleanup done
- Temporary HTTP server on port 8001 stopped
- Temporary probe files removed
- Temporary AWS security-group rule for port 8001 removed

## Hermes
- Hermes installed on separate fresh EC2 test instance
- Parallel migration test intentionally paused for later continuation
- No cutover performed

## Tomorrow priority
- Continue OpenClaw hardening and validation
- Resume Hermes parallel migration only from clean staged checkpoint, not by disrupting Enki_777
