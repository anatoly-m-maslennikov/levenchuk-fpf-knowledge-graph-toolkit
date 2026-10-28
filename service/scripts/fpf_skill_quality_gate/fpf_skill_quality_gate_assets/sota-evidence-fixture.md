# Bounded SOTA evidence fixture

This checked-in packet exists only for the deterministic local FPF quality-gate case `sota-harvest-fixture-analysis`. It is a fixed input, not a claim that the cited works form the current external frontier. The case must not browse or infer source content beyond these records.

Fixture freshness boundary: **2026-08-01**.

## Source records

### S1 — Reflexion

- Identity: Noah Shinn et al., *Reflexion: Language Agents with Verbal Reinforcement Learning*, arXiv:2303.11366, 2023.
- Admitted role: retained research evidence about storing natural-language feedback from prior attempts.
- Fixture claim: an agent can use explicit verbal feedback and episodic memory to change later attempts without updating model weights.
- Limit: the reported tasks and harnesses do not establish universal improvement, production reliability, or release readiness for a skill package.

### S2 — Self-Refine

- Identity: Aman Madaan et al., *Self-Refine: Iterative Refinement with Self-Feedback*, arXiv:2303.17651, 2023.
- Admitted role: retained research evidence about iterative generation, feedback, and revision.
- Fixture claim: repeated feedback-and-revision passes can improve selected task outputs when the evaluation and stopping conditions fit the task.
- Limit: iteration alone does not prove convergence, independent validation, or artifact integrity.

### S3 — SWE-agent

- Identity: John Yang et al., *SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering*, arXiv:2405.15793, 2024.
- Admitted role: retained research evidence about constraining an agent through a purpose-built interface and execution feedback.
- Fixture claim: interface and tool design can materially affect software-agent performance on the evaluated benchmark.
- Limit: benchmark performance does not transfer automatically to analytical-skill routing, cross-provider portability, or release decisions.

## Required synthesis boundary

The packet supports a bounded comparison of three mechanisms: feedback memory, iterative self-revision, and purpose-built tool interfaces. It does not establish which mechanism is best, whether they compose safely, or what is current after the fixture freshness boundary.
