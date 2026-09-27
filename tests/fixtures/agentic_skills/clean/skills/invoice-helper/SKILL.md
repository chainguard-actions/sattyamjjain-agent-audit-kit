---
name: invoice-helper
description: Formats invoices and posts a summary to the team channel.
risk_tier: L1
allowed-tools: [Read]
egress: [hooks.example.com]
signature: sha256:9f2b1c4a7e5d3b8f0a6c2e4d7b9f1a3c5e7d9b1f3a5c7e9d1b3f5a7c9e1d3b5f
---

# Invoice Helper

Setup installs the formatter at a recorded version:

```bash
npm install invoice-fmt@2.4.1
```

Then it formats the invoice and posts the summary.
