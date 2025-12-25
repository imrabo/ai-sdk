# SDK Principles (frozen)

1. Invocation over execution
2. Capabilities over promises
3. Streaming first
4. URL-first, kernel-second
5. Adapters adapt — core never bends
6. Additive evolution only

Non-goals:
- Not a runtime
- Not a process manager
- Not a chat UI
- Not an agent framework
- Not a memory store

Enforcement: these principles are normative and must be tested and referenced by PR reviewers.

---

## Quick checklist for reviewers
- Does core contain provider logic? (No)
- Do providers mutate requests? (No)
- Are capabilities validated before use? (Yes)
- Does sdk export exactly `generate` and `stream`? (Yes)
