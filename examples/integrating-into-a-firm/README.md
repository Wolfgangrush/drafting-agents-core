# Integrating drafting-agents-core into a new firm

3-step quickstart for any future firm builder.

## Step 1 — Clone as sibling

```bash
cd ~/Desktop/AIO/
git clone https://github.com/Wolfgangrush/drafting-agents-core
```

Your firm and drafting-agents-core should be siblings:
```
~/Desktop/AIO/
├── ai-law-firm/
│   └── your-country/
└── drafting-agents-core/
```

## Step 2 — Run setup

```bash
cd ~/Desktop/AIO/ai-law-firm/your-country/
./setup.sh
```

This auto-creates `~/.ailawfirm_<country>/config.toml` from the template and verifies drafting-agents-core is reachable.

## Step 3 — Configure your jurisdiction

Edit `~/.ailawfirm_<country>/config.toml`:

```toml
[jurisdiction]
country = "YourCountry"
citation_format = "Your citation format"
court_hierarchy = "../your-country/_court_hierarchy.json"
bar_rules = "../your-country/_bar_rules.md"
timezone = "Your/Timezone"

[paths]
statute_corpus = "../your-country/_statute_corpus/"
drafting_corpus = "../your-country/_drafting_data/"
audit_log_dir = "~/.ailawfirm_yourcountry/audit_logs/"
matter_root = "~/.ailawfirm_yourcountry/matters/"

[llm]
provider = "claude"
```

The jurisdiction loader resolves `{{JURISDICTION_*}}` placeholders from these values at load time.

## That's it

Your firm now has all 10 canonical agents, resolved for your jurisdiction. Start Claude Code from your firm directory:

```bash
cd ~/Desktop/AIO/ai-law-firm/your-country/
claude
```
