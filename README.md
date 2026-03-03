# AIRDEC Workflows [Temporary]

Backend service for AIRDEC AI extraction, built with **FastAPI**, **Temporal**, and **PostgreSQL**.

## Prerequisites

- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Python ≥ 3.14

## Local Setup

### 1. Install dependencies

```bash
uv sync
```

### 2. Start infrastructure (PostgreSQL + Temporal)

```bash
uv run airdec services start
```

### 3. Create database tables

```bash
uv run airdec init-db
```

### 4. Start the application

```bash
# Start both server and worker
uv run airdec run

# Or start them individually
uv run airdec run server     # FastAPI dev server
uv run airdec run workers    # Temporal worker
```

## Authentication

The API uses **RS256 (asymmetric) signed JWTs**. The client signs tokens with a private key; the server verifies them with the corresponding public key.

### Generating RSA Keys

```bash
# Generate a 2048-bit RSA private key
openssl genpkey -algorithm RSA -out private_key.pem -pkeyopt rsa_keygen_bits:2048

# Extract the public key
openssl rsa -pubout -in private_key.pem -out public_key.pem
```

> ⚠️ **Never commit `.pem` files** — they are already in `.gitignore`.

### Configuration

| Variable         | Description                        | Required    |
| ---------------- | ---------------------------------- | ----------- |
| `JWT_PUBLIC_KEY`  | PEM-encoded RSA public key         | Production  |
| `JWT_ALGORITHM`   | Signing algorithm (default: RS256) | No          |
| `AUTH_DISABLED`   | Set to `true` to skip auth         | Development |

**Production** — set the public key:

```bash
export JWT_PUBLIC_KEY="$(cat public_key.pem)"
```

**Local development** — bypass authentication entirely:

```bash
export AUTH_DISABLED=true
```

### Creating a Test Token (Client-Side)

```python
import jwt
from datetime import datetime, timedelta, timezone

private_key = open("private_key.pem").read()

token = jwt.encode(
    {"sub": "user123", "exp": datetime.now(timezone.utc) + timedelta(hours=1)},
    private_key,
    algorithm="RS256",
)
print(token)
```

Use the token:

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/
```

## CLI Reference

| Command                      | Description                              |
| ---------------------------- | ---------------------------------------- |
| `airdec services start`     | Start PostgreSQL + Temporal via Docker   |
| `airdec services stop`      | Stop all Docker services                 |
| `airdec init-db`            | Create database tables from models       |
| `airdec run`                | Start both server and worker             |
| `airdec run server`         | Start FastAPI dev server only            |
| `airdec run workers`        | Start Temporal worker only               |

## Useful Commands

```bash
# Stop and remove volumes (reset databases)
docker compose down -v

# View Docker service logs
docker compose logs -f

# Open Temporal UI
open http://localhost:8080
```

