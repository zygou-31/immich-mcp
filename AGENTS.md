# Repository Guidelines

This document is a concise contributor guide for this repository. Follow the examples and commands below when working locally.

## Project Structure & Module Organization
- **`src/`**: primary source code. Example: `src/services`, `src/controllers`.
- **`tests/`**: unit and integration tests (`*.spec.*` or `*_test.*`).
- **`assets/`**: static files, images, and fixtures.
- **`docker/` or `deploy/`**: container and deployment manifests.
- **`scripts/`**: helper scripts and tooling.

## Build, Test, and Development Commands
- **Install deps:** `npm install` or `yarn` — installs project dependencies.
- **Dev server:** `npm run dev` — starts local development server with hot reload.
- **Build:** `npm run build` or `make build` — compiles production artifacts.
- **Test:** `npm test` or `make test` — runs unit and integration tests.
- **Docker:** `docker-compose up --build` — containerized local environment.

## Coding Style & Naming Conventions
- **Indentation:** 2 spaces for JS/TS, 4 spaces for Python.
- **Files:** `kebab-case` for filenames (e.g., `user-service.ts`).
- **Variables/Functions:** `camelCase`; **Classes/Components:** `PascalCase`.
- **Formatting/Linting:** use `prettier` and `eslint` where configured. Example: `npm run lint` and `npm run format`.

## Testing Guidelines
- **Frameworks:** project uses standard test runners (Jest, Mocha, or Pytest depending on language).
- **Naming:** unit tests `*.spec.*` or `*_test.*`; integration under `tests/integration/`.
- **Coverage:** aim for meaningful coverage around core logic; run `npm test -- --coverage`.

- **Functional tests:** Tests that require a running Immich instance (real-world integration) are documented in `tests/functional/README.md`. An optional, manually-triggered CI workflow is provided at `.github/workflows/functional-tests.yml` for running these tests in an environment where an Immich instance and credentials are available.

## Commit & Pull Request Guidelines
- **Commit messages:** follow Conventional Commits (`feat:`, `fix:`, `chore:`). Example: `feat(auth): add token refresh`.
- **PR checklist:** description, linked issue, test coverage, screenshots (UI changes), and at least one reviewer.

## Security & Config Tips
- Keep secrets out of the repo. Use `.env.example` to document required env vars.
- Run `git-secrets` or similar pre-commit hooks if available.

If anything here conflicts with project-specific tooling, follow existing configs (e.g., `.eslintrc`, `Makefile`).
