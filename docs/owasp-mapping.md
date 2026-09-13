# OWASP Mapping

> **This page moved.** It used to carry a hand-maintained copy of the OWASP
> coverage tables, and it drifted badly: every MCP slot understated its real
> count by roughly four times (MCP01 said 14 against a live 78, MCP05 said 10
> against 55) and MCP08 was missing altogether. Hand-copying a number the
> registry already knows is how that happens, so the copy is gone rather than
> corrected.

Coverage is generated from the live rule registry by `scripts/gen_coverage.py`,
which CI regenerates and fails on staleness:

- **[OWASP Agentic Top 10 (ASI01-ASI10) → AAK rules](coverage/owasp-agentic-top10.md)**
- **[OWASP MCP Top 10 (MCP01-MCP10) → AAK rules](coverage/owasp-mcp-top10.md)**
- **[OWASP Agentic Skills Top 10 (AST01-AST10)](../README.md#owasp-agentic-skills-top-10-ast10)** — partial by design; the README states which categories are covered and which are not.

For a scan-time view of your own project, run:

```bash
agent-audit-kit scan . --owasp-report
```
