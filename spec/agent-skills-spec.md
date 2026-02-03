# Agent Skills Spec

The official specification is now located at:

## https://agentskills.io/specification

### Quick Reference

**Required fields in SKILL.md:**

```yaml
---
name: skill-name              # Required: lowercase with hyphens
description: Brief description # Required: when to use this skill
---
```

**Optional fields:**

- `license`: License terms for the skill
- `version`: Skill version (recommended)

### Key Concepts

1. **Skills** are folders of instructions, scripts, and resources
2. **SKILL.md** contains YAML frontmatter and markdown instructions
3. Skills can include scripts, templates, and reference documentation
4. Claude loads skills dynamically when relevant keywords are detected
