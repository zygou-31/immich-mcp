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

- **Functional tests workflow usage & safety:** The workflow is intended for manual triggering only. Provide `immich_url` and `immich_key` at dispatch or store them as repository secrets named `IMMICH_BASE_URL` and `IMMICH_API_KEY`. Do not store credentials in the repository. Avoid running the workflow against production servers and be aware that uploaded logs may contain sensitive information; restrict access to workflow artifacts as appropriate.

## Commit & Pull Request Guidelines
- **Commit messages:** follow Conventional Commits (`feat:`, `fix:`, `chore:`). Example: `feat(auth): add token refresh`.
- **PR checklist:** description, linked issue, test coverage, screenshots (UI changes), and at least one reviewer.

## Security & Config Tips
- Keep secrets out of the repo. Use `.env.example` to document required env vars.
- Run `git-secrets` or similar pre-commit hooks if available.

If anything here conflicts with project-specific tooling, follow existing configs (e.g., `.eslintrc`, `Makefile`).

## MCP Server Development

When implementing MCP resources, be aware of the following subtlety regarding context injection:

- **Tools**: For tools, the `Context` object is injected as a parameter in the function signature.
  ```python
  from mcp.server.fastmcp import Context

  @mcp.tool()
  async def my_tool(ctx: Context, ...):
      ...
  ```

- **Resources**: For resources, the `Context` object is **NOT** passed as a parameter. Instead, you must call `mcp.ctx()` inside the function to get the context.
  ```python
  from mcp.server.fastmcp import FastMCP

  mcp = FastMCP(...)

  @mcp.resource("my-resource://...")
  async def my_resource(...) -> ...:
      ctx = mcp.get_context()
      # ... use ctx
  ```

Failure to follow this pattern for resources will result in a `ValueError: Mismatch between URI parameters and function parameters` during server startup.
