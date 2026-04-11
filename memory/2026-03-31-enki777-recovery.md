# 2026-03-31 Enki_777 recovery status

## Instance
- Live EC2 instance name: Enki_777

## Fixes completed today
- Restored and repaired live NEMO backend on 127.0.0.1:8000
- Fixed market_intel missing hooks by adding working fallback implementations for:
  - predict_sale_price(...)
  - analyze_market(...)
- Verified market_intel CMA path works live
- Verified market_intel trends path works live
- Fixed /api/v1/enki/content/generate route mismatch so property_description works again
- Verified /api/v1/enki/leads/process works live
- Verified /api/v1/enki/content/generate works live
- Verified /api/v1/enki/content/recent reflects newly generated content
- Verified /api/v1/enki/overseer/check and /api/v1/enki/overseer/report work live
- Verified generic /api/v1/agents/{agent_name}/process wrapper works live
- Removed live legacy restart-path references to ~/nz-realestate-ai from runtime ENKI scripts
- Updated live runtime restart logic to use:
  systemctl --user restart nemo-backend.service

## Live scripts cleaned
- enki_control_bot.py
- enki_telegram_bot.py
- agen_ovaca.py
- enki_alarm_system.py

## OpenClaw / Telegram state
- OpenClaw gateway healthy and running under systemd user service
- Telegram channel ON/OK for @Enki_controlbot
- Live Telegram message from user produced new OpenClaw log activity, confirming active control path

## Memory state
- Main chat model remains OpenRouter moonshotai/kimi-k2.5
- Memory embeddings/search restored with OpenAI
- openclaw memory status --deep showed embeddings ready, vector ready, indexed files active

## Backup state
- New snapshot/AMI created and available
- Older snapshot retained as fallback

## Important note
- Core recovery verified live on Enki_777 on 2026-03-31
- Custom ENKI bot scripts were cleaned on disk, but OpenClaw Telegram is the primary confirmed live control path
