# VS Code Extension — AgentAuditKit

<!-- AUTO-MANAGED: module-description -->
## Purpose

VS Code extension providing in-editor security scanning for MCP configuration files. Activates on JSON, YAML, and JSONC files and shells out to the `agent-audit-kit` CLI, surfacing findings as editor diagnostics.

Versioned independently of the Python package (its own `version` in `package.json`), and not yet published to the Marketplace.

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: architecture -->
## Module Architecture

```
vscode-extension/
  src/
    extension.ts       # Entry point — activate/deactivate, runs the CLI, publishes diagnostics
    sarifReader.ts     # SARIF → diagnostics + rule-doc hovers. NOT WIRED UP (see below)
  package.json         # Manifest — contributes.configuration only; no commands declared
  tsconfig.json        # TypeScript config
  README.md            # Marketplace-facing readme
  .vscodeignore        # Package exclusions
  out/                 # Compiled JS output (generated, untracked)
```

- **Activation**: `onLanguage:json`, `onLanguage:yaml`, `onLanguage:jsonc`
- **Settings**: `agent-audit-kit.enable`, `agent-audit-kit.severity`, `agent-audit-kit.autoScanOnSave`
- **Output**: `./out/extension.js` (`main` in the manifest)
- **Scan path**: `extension.ts` invokes the CLI via `child_process.execFile` — the extension carries no scanning logic of its own, so in-editor results always match `agent-audit-kit scan`.

**`sarifReader.ts` is dead code.** It exports `loadSarif`, `applySarifToDiagnostics` and `registerSarifCommands`, but `extension.ts` imports only `vscode`, `child_process` and `path` and never calls any of them, and `package.json` declares no `contributes.commands` — so nothing can reach it from the UI either. Its header describes a second workflow ("open a SARIF file → this reader surfaces the same diagnostics") that does not currently run; the file itself notes it was scaffolded with a full publish deferred. Treat the described behaviour as unimplemented, not as a feature to document. Wiring it up means importing and calling `registerSarifCommands(context)` from `activate()` **and** declaring the commands in the manifest; doing only one of those leaves it unreachable.

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: conventions -->
## Module-Specific Conventions

- **Language**: TypeScript, compiled with `tsc` (no bundler)
- **Build**: `npm run compile` (`tsc -p ./`)
- **Watch**: `npm run watch` (`tsc -watch -p ./`)
- **Lint**: `npm run lint` (`eslint src --ext ts`) — note `eslint` is not in `devDependencies`, so this script needs it installed separately
- **Package**: `npx @vscode/vsce package`
- **Engine**: VS Code `^1.85.0`
- **Category**: `Linters`
- Not covered by the root `pytest` / `ruff` / `mypy` targets — this subtree has no test suite, and CI does not build it. Verify changes with `npm run compile` locally.

<!-- END AUTO-MANAGED -->

<!-- AUTO-MANAGED: dependencies -->
## Key Dependencies

Everything is a devDependency; `dependencies` is empty.

- `@types/vscode` — VS Code API types (pinned to the same minor as `engines.vscode`)
- `@types/node` — Node.js types
- `typescript` — compiler
- `@vscode/vsce` — extension packaging

No runtime dependencies beyond the VS Code API itself. The extension relies on the `agent-audit-kit` CLI being installed and on `PATH`, which is a runtime prerequisite rather than a package dependency.

<!-- END AUTO-MANAGED -->

<!-- MANUAL -->
## Notes

Add extension-specific notes here. This section is never auto-modified.

<!-- END MANUAL -->
