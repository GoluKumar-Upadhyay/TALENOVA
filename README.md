# TALENOVA

TALENOVA is an AI-powered career transformation platform. It has a Next.js 15 frontend and a FastAPI backend. Secrets are supplied through git-ignored `.env` files only.

## Development

1. Copy `.env.example` to a local `.env` and supply environment-specific values.
2. Start a local PostgreSQL instance before database-backed modules are added.
3. In `backend`, run `py -m pip install -r requirements.txt`, then `alembic upgrade head` and `py -m uvicorn app.main:app --reload`.
4. In `frontend`, run `npm install`, then `npm run dev`.

Run `pytest -q` from `backend` for API tests, and `npm run lint && npm run build` from `frontend` for frontend verification. Docker Compose is supplied for deployment verification and will be validated before release.
