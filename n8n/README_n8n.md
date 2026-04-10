n8n local setup (Docker)

Files added:
- n8n_workflows/*.json  (individual workflow JSON exports)
- docker-compose.n8n.yml

Quick setup (Docker required):
1) Ensure Docker Desktop / Docker Engine is installed and running on your machine.

2) From project root run:
   docker compose -f docker-compose.n8n.yml up -d

   This will:
   - start n8n on port 5678
   - persist n8n SQLite DB to ./n8n/data/n8n.sqlite on your PC
   - import all workflow JSON files from ./n8n_workflows (the importer runs once and exits)

3) Visit http://localhost:5678 to open the n8n UI. If you want to secure with basic auth, set N8N_BASIC_AUTH_ACTIVE=true and provide N8N_BASIC_AUTH_USER / N8N_BASIC_AUTH_PASSWORD in the environment.

Notes / Important details:
- Workflows are pre-configured to call your local Flask backend at http://host.docker.internal:5000 (this resolves from inside Docker to your host machine on Windows). If you run Flask inside Docker instead, change BASE_URL variable or update workflows.

- Main Orchestrator workflow ("Main Orchestrator") triggers other webhooks inside n8n. The subordinate workflows expose webhook paths such as:
  - /webhook/init-data-n8n
  - /webhook/api/discharged/chat
  - /webhook/run-script

  The orchestrator calls them internally so workflows remain decoupled.

- The importer service uses `n8n import:workflow` on container start. If you add workflows later, you can re-import them using the CLI or use the UI to import the JSON files.

Troubleshooting:
- If containers fail to start, run `docker compose -f docker-compose.n8n.yml logs` to inspect logs.
- If workflows don’t execute: in n8n UI ensure workflows are active (the JSON files are exported with `"active": true`), and verify the webhook URLs.

If you want, I can:
- Add a one-shot script (Windows PowerShell) that waits for n8n to be healthy and forces imports (handy if Docker Desktop doesn't support host.docker.internal), or
- Convert the main orchestrator to call the Flask app directly instead of internal webhooks.

Tell me which follow-up you'd like.