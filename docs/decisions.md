# Architecture decisions

## 2026-07-18 — Local development defaults

Local development uses Dockerized PostgreSQL. Production is expected to use Supabase PostgreSQL and Storage; no Supabase project identifier or secret is assumed or committed.

## 2026-07-18 — Build sequence

The platform will be built in the requested dependency order. A module is completed only after its migration, API layers, tests, admin UI, public rendering, verification, and commit are complete.

## 2026-07-18 — Development verification environment

Docker Compose verification is deferred until deployment because the Docker Desktop engine is unavailable in the development environment. Local PostgreSQL will be used for backend verification instead. Docker Compose must be revisited and verified end-to-end before production deployment.
