# Architecture

TALENOVA is split into a Next.js 15 frontend and FastAPI backend. The backend will follow Router → Service → Repository → SQLAlchemy model. PostgreSQL is the source of truth and Supabase Storage stores media; only public media URLs are persisted in PostgreSQL.

During local development Docker Compose exposes the frontend on port 3000, API on port 8000, and PostgreSQL on port 5432. The backend container applies the Alembic head before starting FastAPI. Public pages provide editorial content immediately and the CMS APIs remain the source of truth for managed records, media, and contact enquiries.
