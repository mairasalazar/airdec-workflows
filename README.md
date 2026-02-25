# Workflow

## Run it locally

1. Fork and clone this repository.

```bash
git clone git@github.com:<your-username>/airdec-workflows.git
cd airdec-workflows
```

2. Spin up the database and Temporal

```bash
docker compose up -d
```

3. Create the workflow table

```bash
make migrate
```

4. Start backend
```bash
make dev
```

5. In a separate terminal, start the worker

```bash
make worker
```

6. Try out the backend with `http://127.0.0.1:8000/docs` and the Temporal UI with `http://localhost:8080/`