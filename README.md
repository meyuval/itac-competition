# ITAC Arena tests

1. Keep the repository **Public**.
2. In **Settings → Secrets and variables → Actions**, add secrets `FAN_EMAIL`, `FAN_PASSWORD`, and `ORGANIZATION_API_KEY`.
3. Do not commit `.env`; CI reads credentials from those secrets only.
4. Optional: `FAN_API_KEY`, `BASE_URL`, `API_BASE`, `API_KEY_HEADER` (secrets or variables). Defaults are `https://arena.itac.co.il` and `X-API-Key`.
5. Push to `main` (or run **Actions → Tests → Run workflow**) to execute the suite; JUnit/Playwright output is on the run’s **Artifacts**.
