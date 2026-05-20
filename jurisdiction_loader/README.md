# Jurisdiction Loader

Helper that each firm calls to load its corpus paths and jurisdiction config into agents.

## How it works

1. The firm's `config.toml` at `~/.ailawfirm_<country>/config.toml` defines jurisdiction-specific values
2. `loader.py` reads that config and resolves `{{JURISDICTION_*}}` placeholders in agent SKILL.md bodies
3. Each firm gets the same canonical agents, with their jurisdiction's values substituted at load time

## Usage

```python
from jurisdiction_loader import load_config, resolve_placeholders

config = load_config("uk")
with open("agents/citation_clerk/SKILL.md") as f:
    body = f.read()
resolved = resolve_placeholders(body, config)
```

## Config schema

See `examples/integrating-into-a-firm/` for the full `config.toml.template`.
