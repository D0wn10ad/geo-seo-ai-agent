---
description: "Run a full GEO+SEO audit with parallel subagents on a target URL"
---

Load the `geo` skill and execute the full GEO+SEO audit workflow on `$1`. Run all 3 phases: discovery (fetch homepage, detect business type, extract key pages), parallel analysis (invoke all 5 migrated audit-worker skills in parallel via the host task/subagent mechanism), and synthesis (calculate composite GEO score, generate action plan).
