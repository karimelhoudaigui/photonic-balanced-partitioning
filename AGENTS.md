# Agent Guidelines

## Development Rules

1. **Tests before merge**: All changes must pass existing tests
2. **No QPU credentials in code**: Never hardcode QPU tokens or credentials
3. **Document assumptions**: Any scientific claim must have supporting evidence
4. **Preserve negative results**: Failed experiments are valuable data
5. **Reproducibility**: All experiments must be reproducible with fixed seeds

## Code Review Checklist

- [ ] Tests pass (`pytest tests/`)
- [ ] No hardcoded credentials
- [ ] Scientific claims have evidence
- [ ] Negative results documented
- [ ] Seeds are fixed for reproducibility
- [ ] Dependencies are pinned in pyproject.toml

## Scientific Integrity

- Never claim quantum advantage without proof
- Never hide collision effects
- Never invent results
- Never use favorable graph selection without disclosure
- Always compare fairly (same budget, same conditions)

## QPU Access

QPU experiments require explicit authorization. No automatic QPU calls.

## Data Management

- Raw QPU data is never modified
- Processed results are separate from raw data
- All experiments are logged with timestamps and git commits
