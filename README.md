# ITAC Arena tests

1. Keep the repository **Public**.
2. In **Settings → Secrets and variables → Actions**, add secrets `FAN_EMAIL`, `FAN_PASSWORD`, and `ORGANIZATION_API_KEY`.
3. Optional: `FAN_API_KEY`, `BASE_URL`, `API_BASE`, `API_KEY_HEADER` (secrets or variables). Defaults are `https://arena.itac.co.il` and `X-API-Key`.

# Instructions
Create a `.env` with the same required values as the secrets, then `pip install -r requirements.txt` and `python -m playwright install chromium`. Run everything with `pytest`, backend with `pytest tests/backend`, or frontend with `pytest tests/frontend --browser chromium`.

Run everything with `pytest`, or filter with `-m`: `be` / `fe`, `events` / `admin` / `orders`, `sanity`, `live_api`, `component` (for example `pytest -m sanity` or `pytest -m "fe and admin"`).
