# Setup

Everything runs in Docker: you do **not** need Python, dbt or Postgres installed locally. You need four things:

| Tool | Why |
|---|---|
| Git | Clone the repository, commit your work |
| Docker (Docker Desktop or equivalent) | Postgres, dbt and the API run in containers |
| `make` | Short commands (`make up`, `make test`…). Optional: every command has a plain `docker compose` equivalent below |
| A SQL client | Query the database on `localhost:5432`. We suggest [pgAdmin](https://www.pgadmin.org/download/); any PostgreSQL client works |

Plan for about 4 GB of free disk space. The first `make check` downloads ~1 GB of images and packages.

---

## macOS

With [Homebrew](https://brew.sh):

```bash
# Git and make (also shipped with the Xcode command line tools: xcode-select --install)
brew install git make

# Docker Desktop (alternatives: OrbStack `brew install --cask orbstack`, or Colima)
brew install --cask docker
open -a Docker   # start it once and accept the licence

# SQL client: pgAdmin (suggested; installer also at https://www.pgadmin.org/download/pgadmin-4-macos/)
brew install --cask pgadmin4
# alternatives: brew install --cask dbeaver-community (GUI), or psql in the terminal:
brew install libpq && brew link --force libpq
```

## Windows 10 / 11

Use **WSL 2** (Ubuntu): Docker Desktop relies on it, and `make` works natively there. Run in PowerShell **as administrator**:

```powershell
wsl --install -d Ubuntu          # reboot when asked, then open "Ubuntu" once to create a user
winget install -e --id Docker.DockerDesktop
winget install -e --id Git.Git
winget install -e --id PostgreSQL.pgAdmin   # SQL client (installer also at https://www.pgadmin.org/download/pgadmin-4-windows/)
```

Then in Docker Desktop: **Settings → Resources → WSL integration → enable Ubuntu**.

In the **Ubuntu** terminal:

```bash
sudo apt-get update && sudo apt-get install -y git make postgresql-client
```

> Clone the repository **inside** the WSL filesystem (e.g. `~/code`), not under `/mnt/c/...`: it avoids line-ending issues and very slow Docker volumes.

## Linux

Install Docker Engine with the Compose plugin ([docs](https://docs.docker.com/engine/install/)), then `sudo apt-get install -y git make postgresql-client` (or your distribution's equivalent).

---

## Check your environment

```bash
git --version
docker --version
docker compose version
make --version
```

Then, from the repository root:

```bash
make check   # builds the images; ends with "Environment OK"
make up      # starts Postgres, loads the data with dbt, starts the API (≈ 1 min)
make test
```

Open http://localhost:8000/docs: you should see the API.

## Connect a SQL client

| Setting | Value |
|---|---|
| Host | `localhost` |
| Port | `5432` |
| Database | `rdp` |
| User / password | `rdp` / `rdp` |

Schemas: `raw` (data loaded by dbt seeds) and `analytics` (dbt models).

- pgAdmin: **Object Explorer → right-click Servers → Register → Server…**. Under *General*, name it `rdp`. Under *Connection*, fill in the table above and tick *Save password*, then **Save**. Open a SQL editor with **Tools → Query Tool**. On Windows, install pgAdmin on Windows itself (not inside WSL): `localhost:5432` reaches the Docker container.
- DBeaver: **New connection → PostgreSQL**, fill in the table above, then **Test connection**. DBeaver offers to download the driver on first use: accept.
- psql: `psql postgresql://rdp:rdp@localhost:5432/rdp`
- No local client at all: `make psql` opens a SQL shell inside the container.

Smoke query:

```sql
select study_code, count(*) from raw.participants group by study_code;
```

## Without `make`

| make | docker compose |
|---|---|
| `make check` | `docker compose build` |
| `make up` | `docker compose up -d postgres && docker compose run --rm dbt build && docker compose up -d api` |
| `make test` | `docker compose run --rm --no-deps api pytest -q` |
| `make token STUDIES="ONC-101"` | `docker compose run --rm --no-deps api python scripts/make_token.py --sub researcher@example.org --studies ONC-101` |
| `make dbt CMD="build"` | `docker compose run --rm dbt build` |
| `make psql` | `docker compose exec postgres psql -U rdp -d rdp` |
| `make down` | `docker compose down -v` |

## Troubleshooting

| Symptom | Fix |
|---|---|
| `port is already allocated` on 5432 | Another Postgres runs locally. Stop it, or start with another port: `PG_PORT=5433 make up`, then connect your SQL client to port 5433. |
| Port 8000 already in use | Stop the other service, or change the `api` port mapping in `docker-compose.yml`. |
| `Cannot connect to the Docker daemon` | Docker Desktop is not running: start it and wait for the whale icon to settle. |
| Windows: `make: command not found` | You are in PowerShell. Run the commands from the Ubuntu (WSL) terminal. |
| Apple Silicon: slow first build | Expected the first time; later runs reuse the cached images. |

If the stack still does not start, **do not spend your hour on it**: the code, [`docs/data_model.md`](docs/data_model.md) and [`outputs/`](outputs/) are enough to do the exercise, and you can write SQL without running it.

## Optional: local Python environment for your IDE

**Not required**: everything already runs in Docker. A local environment only helps your IDE (autocompletion, navigation, resolved imports) and lets you run the tests without Docker. Use Python 3.12, the version of the containers.

Install Python 3.12:

```bash
brew install python@3.12                                   # macOS
sudo apt-get install -y python3.12 python3.12-venv         # Windows (Ubuntu 24.04 in WSL) / Linux
```

From the repository root:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements.txt
pip install dbt-core==1.10.15 dbt-postgres==1.9.1          # optional: dbt outside Docker
```

Check:

```bash
(cd api && pytest -q)                                      # no database needed
(cd dbt && DBT_PROFILES_DIR=. dbt build)                   # needs `make up` (Postgres on localhost:5432)
```

Point your IDE to `.venv/bin/python`:

- PyCharm: **Settings → Project → Python Interpreter → Add Interpreter → Add Local Interpreter → Existing**, select `.venv/bin/python`. Then right-click `api` → **Mark Directory as → Sources Root**, since imports start from `api/` (`from app.main import …`).
- VS Code: `Cmd/Ctrl+Shift+P` → **Python: Select Interpreter** → `.venv`. If imports are not resolved, add `"python.analysis.extraPaths": ["api"]` to the workspace settings.
