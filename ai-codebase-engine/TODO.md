# TODO

## Code audit & fix
- [x] Fix backend/core/code_parser.py entity defaults + dependency extraction robustness
- [x] Fix backend/core/graph_builder.py edge target resolution (cross-file) correctness
- [x] Fix backend/core/llm_client.py context formatting key mismatch (document vs input)
- [x] Fix backend/utils/repo_loader.py syntax error / broken exception string
- [x] Fix backend/api integration issues if any uncovered by running tests
- [ ] Run unit tests (`pytest`)
- [x] Build & run via Docker Compose (`docker compose up --build`), then verify `/health`

