# SMT INTEL Engine v5.0 — Discord Webhook Receiver

Flask app that receives TradingView webhooks and sends Discord embeds.

## 1. Files

- `bot.py` — Flask app, `/alert` route, Discord embed sender
- `requirements.txt` — Python deps
- `Procfile` — Railway process definition
- `.env.example` — env var template

## 2. Deploy to Railway

1. Push this folder to a GitHub repo (e.g. `smt-intel-engine-v5`).
2. Go to Railway → **New Project** → **Deploy from GitHub** → choose the repo.
3. After deploy, open **Variables** tab and add:

   ```
   DISCORD_WEBHOOK=YOUR_DISCORD_WEBHOOK_URL_HERE
   ```

4. Railway gives you a URL like:

   ```
   https://smt-engine-yourid.up.railway.app
   ```

5. Your TradingView webhook URL is:

   ```
   https://smt-engine-yourid.up.railway.app/alert
   ```

## 3. Run Command

Railway will use this from `Procfile`:

```bash
web: gunicorn bot:app --timeout 120 --worker-tmp-dir /dev/shm
```

## 4. TradingView Setup (Quick)

- In Alerts, set **Webhook URL** to your `/alert` endpoint.
- Use the JSON templates you defined for:
  - ENTRY
  - TARGET
  - STOP
  - SMT_BULL
  - SMT_BEAR

The bot will auto-color embeds and add footer: `SMT INTEL Engine v5.0`.
