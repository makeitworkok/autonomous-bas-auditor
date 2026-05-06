# Documentation Package

This folder is the central knowledge base for the Autonomous BAS Auditor project.

## Audience
- Builders and maintainers of the codebase
- Operators deploying to Lightsail and Raspberry Pi
- ClawComp judges/reviewers who need a concise but complete technical package

## Document Index
- [Project Overview](project-overview.md)
- [System Architecture](architecture.md)
- [Cloud API Setup (Lightsail)](setup-lightsail.md)
- [Edge Collector Setup (MVP)](setup-edge-collector.md)
- [API Reference](api-reference.md)
- [Operations Runbook](operations-runbook.md)
- [Development Roadmap](development-roadmap.md)
- [ClawComp Submission Notes](clawcomp-submission-notes.md)
- [Decision Log](decision-log.md)

## Maintenance Rules
- Keep docs aligned with code changes in the same PR whenever possible.
- Record meaningful architecture/product decisions in the decision log.
- Update roadmap status when a phase milestone changes.
- Keep deployment docs free of secrets; never commit live credentials.
