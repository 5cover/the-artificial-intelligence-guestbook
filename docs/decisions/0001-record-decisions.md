# 0001. Record decisions in the repository

Status: Accepted (2026-11-15)

Issue: #1

## Context

The project carries a custodial obligation measured in decades (plan sections 28, 29). Important knowledge must not exist solely in the founder's memory, nor in chat transcripts with AI agents, which the owner considers dispensable.

## Decision

Architecture, policy and operational decisions are recorded as numbered ADRs in `docs/decisions/` using [the template](template.md). Options awaiting a decision live in `docs/proposals/`. Research findings live in `docs/research/`. Conventions for this are maintained in [AGENTS.md](../../AGENTS.md).

ADRs are never deleted. A changed decision gets a new ADR that supersedes the old one, and the old one's status is updated.

## Consequences

A successor can reconstruct why the system is the way it is. Every decision taken in conversation must be written down before the work it enables is considered done.
